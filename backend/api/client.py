import os
from django.core.mail import EmailMessage
from email.utils import formataddr
from email.mime.image import MIMEImage

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Prefetch
from api.models import *
from django.db import transaction
from api.serializer import *
from api.utils import log_error, use_pusher, send_prompt_to_gemini

import json
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
import traceback
import imghdr


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def client_data(request):
    user = request.user
    if request.method == 'GET':
        client = Client.objects.get(user=request.user)
        consultations = Consultation.objects.filter(client=client)
        consultations_data = ConsultationSerializerOne(consultations, many=True).data
        drugs_data = DrugSerializerOne(Drug.objects.all(), many=True).data
        order_data = OrderSerializerOne(Order.objects.filter(client=client), many=True).data
        message_data = MessageSerializerOne(Message.objects.filter(client=client).order_by('id'), many=True).data
        diet_plans = DietPlanSerializerOne(DietPlan.objects.filter(client=client), many=True).data

        
        return Response({
            'consultations': consultations_data,
            'drugs': drugs_data,
            'orders': order_data,
            'messages': message_data,
            'diet_plans': diet_plans
        })
    
    elif request.method == 'POST':
        data = request.data
        if data['type'] == 'createConsultation':
            data_obj = json.loads(data['dataObj'])
            date, time, purpose = data_obj.get('date'), data_obj.get('time'), data_obj.get('purpose')
            try:
                client = Client.objects.get(user=request.user)
                client_data = ClientSerializer(client).data
                staff_data = StaffSerializer(Staff.objects.all(), many=True).data
                prompt = f"Give me a name(maximum 50 characters) i can use based on the consultation booking purpose: {purpose}.\nI will show the name as the name of a consultation to the user so choose an appropriate one. Return only the name and nothing else."
                name = send_prompt_to_gemini(prompt)
                message = f"""
                    Based on the following client information and the purpose of their consultation, please select the most suitable staff member from the list below who can best handle their request.
                    Client Data:
                    {client_data}
                    Consultation Description:
                    "{purpose}"
                    Available Staff:
                    {staff_data}
                    Consider factors like area of specialization, experience, and any other relevant fields available in the staff data. Return only the best match and explain why they were chosen.
                    Return only the id of the staff if a match is found else return 0. Don't add any other text.
                    """
                try:
                    match_staff_id = int(send_prompt_to_gemini(message))
                    match_staff_obj = Staff.objects.select_related('user').filter(id=match_staff_id).first()
                    if not match_staff_obj:
                        raise Exception
                    consultation = Consultation.objects.create(client=client, staff=match_staff_obj, date=date, time=time, name=name, purpose=purpose, type='new')
                    return Response(ConsultationSerializerOne(consultation).data)
                except Exception:
                    log_error(traceback.format_exc())
                    return Response({'message': 'There are no available Doctors that can handle this consultation now. Please try again later.'}, status=400)

            except Exception:
                log_error(traceback.format_exc())
                return Response({'message': 'Something went wrong'}, status=400)
            
        elif data['type'] == 'deleteConsultation':
            consultation = Consultation.objects.get(id=int(data['itemId']))
            consultation.delete()
            return Response(status=204)

        if data['type'] == 'createDietPlan':
            client = Client.objects.get(user=request.user)
            data_obj = json.loads(data['dataObj'])
            goal = data_obj.get('goal')
            diet_type = data_obj.get('diet_type')
            duration_days = data_obj.get('duration_days')
            meal_types = data_obj.get('meal_types', [])
            activity_level = data_obj.get('activity_level')
            preferred_foods = data_obj.get('preferred_foods').split(',') if data_obj.get('preferred_foods') and data_obj.get('preferred_foods') != 'null' else []
            end_date = (datetime.strptime(timezone.now().date().strftime('%Y-%m-%d'), '%Y-%m-%d') + timedelta(days=duration_days - 1)).strftime('%Y-%m-%d')
            try:
                client_data = json.dumps(ClientSerializer(client).data, indent=2)
                prompt = f"""
                Generate a detailed {duration_days}-day diet plan based on the following user profile:

                User Profile:
                {client_data}

                Diet Plan Details:
                - Goal: {goal}
                - Diet type: {diet_type}
                - Duration: {duration_days} days
                - Meal types per day: {meal_types}
                - Activity level: {activity_level}
                - Preferred foods: {preferred_foods}

                **Important**
                Consider foods from the user's country or nationality

                Return the diet plan as a JSON list with the following structure:

                [
                    {{
                        "day": 1,
                        "date": "2025-06-01",
                        "meals": {{
                            "breakfast": ["Oatmeal with berries", "Green tea"],
                            "lunch": ["Grilled chicken salad", "Quinoa"],
                            "dinner": ["Baked salmon", "Steamed vegetables"],
                            "snacks": ["Almonds", "Apple"]
                        }},
                        "notes": "Drink at least 8 glasses of water."
                    }},
                    {{
                        "day": 2,
                        "date": "2025-06-02",
                        "meals": {{
                            "breakfast": ["Greek yogurt with honey", "Orange juice"],
                            "lunch": ["Turkey sandwich", "Carrot sticks"],
                            "dinner": ["Stir-fried tofu", "Brown rice"],
                            "snacks": ["Mixed nuts", "Banana"]
                        }},
                        "notes": "Include light exercise."
                    }}
                ]

                **Important**
                Return only JSON, no code blocks, no explanations, no markdown, just raw JSON text
                """
                raw_response = send_prompt_to_gemini(prompt)
                cleaned_response = re.sub(r"^```json|```$", "", raw_response.strip(), flags=re.IGNORECASE).strip()
                cleaned_response = cleaned_response.strip("` \n")
                try:
                    diet_plan_json = json.loads(cleaned_response)
                except json.JSONDecodeError as e:
                    raise e
                
                diet_plan = DietPlan.objects.create(
                    client=client,
                    goal=goal,
                    diet_type=diet_type,
                    duration_days=duration_days,
                    meal_types=meal_types,
                    activity_level=activity_level,
                    preferred_foods=[x.strip() for x in preferred_foods],
                    end_date=end_date,
                    plans=diet_plan_json,
                )
                return Response(DietPlanSerializerOne(diet_plan).data)
                
            except Exception:
                log_error(traceback.format_exc())
                return Response({'message': 'Connection Error'}, status=400)
            
        elif data['type'] == 'deleteDietPlan':
            item_to_delete = DietPlan.objects.get(id=int(data['itemId']))
            item_to_delete.delete()
            return Response(status=204)

        elif data['type'] == 'sendMessage':
            client = Client.objects.get(user=request.user)
            client_data, history, user_message = json.dumps(json.loads(data['clientData']), indent=2), data['history'], data['message']
            intro = """
                You are Cassandra, an AI assistant for Aivise Health.

                Aivise Health is a digital healthcare platform that offers a range of services, including:
                - In-person consultations
                - E-pharmacy (medicine ordering and delivery)
                - Diet and nutrition advice
                - Mental health support and psychological counseling
                - Herbal and alternative medicine guidance

                Facility working ours: 
                Monday - Friday : 8:30am - 730pm

                As Cassandra, you assist users by:
                - Answering health-related questions
                - Recommending appropriate services or products
                - Clearly communicating that you are part of Aivise Health
                """

            instructions = """
            Avoid repeating greetings, or reintroducing yourself (e.g., don't say "Hi, I'm Cassandra" if you've already said it in previous conversations).
            Just continue the conversation naturally.
            **Important**
            Be concise and professional
            Only mention the user's name if they ask for it, or once at the start of a conversation. Avoid repeating it in every message.
            """
            prompt_histry = f"""
            **History of passed conversations with the user**:
            {history}
            """

            print(prompt_histry)
            message_categories = """
            1. In-person consultation (consultation booking and scheduling)
            2. E-pharmacy (medicine ordering and delivery)
            3. Diet and nutrition advice
            4. Mental health support and psychological counseling
            5. Herbal and alternative medicine guidance
            6. Other
            """
            prompt_1 = f"""
            {intro}

            User message: {user_message}

            Available services:
            {message_categories}

            Based on the user message, which of the above services is it most related to?
            Return the **service number only** (e.g., 2). Do not include any extra text.
            """
            message_intent = send_prompt_to_gemini(prompt_1)
            try:
                category_number = int(str(message_intent).split('.')[0].strip())
                profile_history_message = f"User Profile: {client_data}\n\n{prompt_histry}\nuser: {user_message}\ncassandra: "
                additional_data = ''
                if category_number == 1:
                    staff_data = json.dumps(StaffSerializerOne(Staff.objects.all(), many=True).data, indent=2)
                    additional_data = f"Available staff: {staff_data}"
                elif category_number == 2:
                    drugs_data = json.dumps(DrugStockSerializerOne(DrugStock.objects.all(), many=True).data, indent=2)
                    additional_data = f"Available drugs: {drugs_data}"
                prompt_2 = f"{intro}\n{instructions}\n\n{additional_data}\n\n{profile_history_message}"
                gemini_message = send_prompt_to_gemini(prompt_2)
                user_message_obj = Message.objects.create(client=client, sender='user', message=user_message)
                gemini_message_obj = Message.objects.create(client=client, sender='cassandra', message=gemini_message)
                user_message_data = {'id': user_message_obj.id,'sender': user_message_obj.sender,'message': user_message_obj.message}
                gemini_message_data = {'id': gemini_message_obj.id,'sender': gemini_message_obj.sender,'message': gemini_message_obj.message}
                return Response([user_message_data, gemini_message_data])

            except Exception:
                log_error(traceback.format_exc())
                return Response({'message': "Connection Error"}, status=400)

        elif data['type'] == 'placeOrder':
            order_items = json.loads(data['orderItems'])
            client = Client.objects.get(user=request.user)
            with transaction.atomic():
                try:
                    order_obj = Order.objects.create(client=client, address=client.address, date=timezone.now().date())
                    for _item_ in order_items:
                        if not int(_item_['quantity'] == 0):
                            drug_obj = DrugStock.objects.get(id=int(_item_['id']))
                            order_item_obj = OrderItem.objects.create(order=order_obj, drug=drug_obj, quantity=_item_['order_quantity'])
                            drug_obj.quantity -= int(order_item_obj.quantity)
                            drug_obj.save(update_fields=['quantity'])
                            order_item_obj.update_fields()

                    order_obj.update_fields()
                    order_data = OrderSerializerOne(order_obj).data
                    return Response(order_data)
                except Exception:
                    transaction.set_rollback(True)
                    log_error(traceback.format_exc())
                    return Response({'message': "Connection Error"}, status=400)
        
        elif data['type'] == 'deleteOrder':
            order_item = Order.objects.prefetch_related(Prefetch('items', queryset=OrderItem.objects.select_related('drug'))).get(id=int(data['itemId']))
            items = order_item.items.all()
            items_instances = []
            for item in items:
                item.drug.quantity += item.quantity
                items_instances.append(item)
            OrderItem.objects.bulk_update(items_instances, ['quantity'])
            order_item.delete()
            return Response(status=204)
