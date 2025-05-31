from api.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
import requests
import json
import time
import random
from datetime import date, timedelta



def query(request):
   
    # # Drug names you want to search
    # drug_names = [
    #     "Lexapro", "Oxycodone", "Lisinopril", "Simvastatin", "Levothyroxine",
    #     "Amoxicillin", "Azithromycin", "Hydrochlorothiazide", "Amlodipine",
    #     "Alprazolam", "Metformin", "Atorvastatin", "Omeprazole", "Ciprofloxacin",
    #     "Ondansetron", "Clozapine", "Furosemide", "Vardenafil", "Tetracycline",
    #     "Heparin", "Valganciclovir"
    #     "Tofranil", "Reclast", "Zometa", "Glucotrol", "Generlac", "Constulose", "AcipHex", "Otrexup",
    #     "Cleocin", "Tylenol", "Feosol", "Relpax", "Carbacot", "Robaxin", "DiaBeta", "Celexa",
    #     "Benicar", "Coreg", "Spiriva", "Xolair", "NitroStat Sublingual", "Eliquis", "Neurontin",
    #     "Enbrel", "Herceptin", "Atripla", "Xarelto", "Stalevo 50", "Fioricet", "Levemir", "Lovenox",
    #     "Ritalin", "Concerta", "Crestor", "Xgeva", "Prolia", "Pradaxa", "Sensipar", "Vesicare",
    #     "Haldol", "Ala-Cort", "HumuLIN", "Isentress", "Stelara", "Mobic", "Remicade",
    #     "Night Time Cold and Flu", "Renvela", "Fragmin", "Zoloft", "Klonopin", "Avalide", "Ceftin",
    #     "Nizoral Topical", "Lyrica", "Nexium", "Combivent Respimat", "Niaspan", "Uroxatral", "Biaxin",
    #     "Zomig", "Invokana", "Saxenda", "Victoza", "Alimta", "Lotrimin", "FungiCURE Pump Spray",
    #     "Avastin", "Sovaldi", "Gilenya", "Epogen", "Seroquel", "Amaryl", "Percocet", "SandIMMUNE",
    #     "Neoral", "Lantus", "Cialis", "Endep", "Elavil", "Vanatrip", "Lopid", "Orapred", "Advil",
    #     "Aceon", "Desyrel", "Actos", "Proscar", "Inbrija", "Dopar", "Larodopa", "Actonel", "Ventolin",
    #     "ProAir", "Proventil", "Ultram", "Sonata", "Zebeta", "Zovirax", "Coumadin", "Luvox", "Plavix",
    #     "Vibramycin", "Adoxa", "Hyzaar", "Kytril", "Sancuso", "Restoril", "Prevacid", "Augmentin",
    #     "Mevacor", "Altoprev"
    # ]

    # # Simulated data for unit types
    # unit_types = ["tablet", "capsule", "injection", "syrup", "cream", "patch", "suppository"]

    # for drug_name in drug_names:
    #     unit_type = random.choice(unit_types)
    #     full_name = f"{drug_name} ({unit_type})"
    #     batch_number = f"BN{random.randint(10000, 99999)}"
    #     strength = f"{random.randint(5, 500)}mg"
    #     quantity = random.randint(10, 100)
    #     order_quantity = random.randint(1, 5)
    #     price = round(random.uniform(5.00, 100.00), 2)
    #     expiry = date.today() + timedelta(days=random.randint(180, 720))

    #     try:
    #         drug = Drug.objects.get(name=drug_name)
    #         DrugStock.objects.create(
    #             drug=drug,
    #             batch_number=batch_number,
    #             name=f"{drug_name} {strength} {unit_type} ({drug.brand})",
    #             strenght=strength,
    #             quantity=quantity,
    #             order_quantity=order_quantity,
    #             price=price,
    #             expiry_date=expiry
    #         )
    #         print(f"Drug '{drug_name}' stock created.")
    #     except Drug.DoesNotExist:
    #         print(f"Drug '{drug_name}' not found.")
    

    # drugs = []
    # with open("drugs_data.json", "r") as f:
    #     drugs = json.load(f)

    # drug_instances = []
    # for drug in drugs:
    #     existing_drug = Drug.objects.filter(name=drug['name']).first()
    #     if existing_drug:
    #         continue
    #     drug_obj = Drug(
    #         name=drug['name'],
    #         generic_name=drug['generic_name'],
    #         brand=drug['brand'],
    #         manufacturer=drug['manufacturer'],
    #         route=drug['route'],
    #         dosage_form=drug['dosage_form'],
    #         active_ingredients=drug['active_ingredients'],
    #         pharm_class=drug['pharm_class'],
    #         description=drug['description'],
    #         side_effects=drug['side_effects'],
    #         precautions=drug['precautions'],
    #         warnings=drug['warnings'],
    #         storage=drug['storage'],
    #         indications=drug['indications_and_usage'],
    #         is_prescription_required=drug['is_prescription_required'],
    #     )
    #     drug_instances.append(drug_obj)

    # Drug.objects.bulk_create(drug_instances)

    return HttpResponse("<h2>Operation successful</h2>")


staff_data = [
    {
        "user": {"first_name": "Ama", "last_name": "Boateng", "email": "ama.boateng@example.com"},
        "gender": "Female",
        "age": 34,
        "contact_one": "+233201234567",
        "contact_two": "+233541234567",
        "nationality": "Ghanaian",
        "specialization": "General Practitioner",
        "years_of_experience": 8,
        "languages": ["English", "Twi"],
        "bio": "Passionate about primary care and preventive medicine. Skilled in patient education and chronic disease management."
    },
    {
        "user": {"first_name": "Kwame", "last_name": "Mensah", "email": "kwame.mensah@example.com"},
        "gender": "Male",
        "age": 45,
        "contact_one": "+233208765432",
        "contact_two": "+233558765432",
        "nationality": "Ghanaian",
        "specialization": "Cardiologist",
        "years_of_experience": 15,
        "languages": ["English", "Ewe"],
        "bio": "Experienced cardiologist with a deep commitment to improving heart health through advanced diagnostics and patient care."
    },
    {
        "user": {"first_name": "Abena", "last_name": "Owusu", "email": "abena.owusu@example.com"},
        "gender": "Female",
        "age": 29,
        "contact_one": "+233240112233",
        "contact_two": None,
        "nationality": "Ghanaian",
        "specialization": "Pediatrician",
        "years_of_experience": 4,
        "languages": ["English", "Ga"],
        "bio": "Loves working with children and ensuring their healthy development. Focused on child-friendly communication."
    },
    {
        "user": {"first_name": "Kofi", "last_name": "Asare", "email": "kofi.asare@example.com"},
        "gender": "Male",
        "age": 38,
        "contact_one": "+233501234321",
        "contact_two": "+233551234321",
        "nationality": "Ghanaian",
        "specialization": "Dermatologist",
        "years_of_experience": 10,
        "languages": ["English"],
        "bio": "Specializes in skincare treatments and managing skin diseases. Promotes holistic skincare solutions."
    },
    {
        "user": {"first_name": "Linda", "last_name": "Darko", "email": "linda.darko@example.com"},
        "gender": "Female",
        "age": 32,
        "contact_one": "+233203339999",
        "contact_two": None,
        "nationality": "Ghanaian",
        "specialization": "Dietitian",
        "years_of_experience": 6,
        "languages": ["English", "Twi"],
        "bio": "Certified dietitian helping clients achieve nutritional goals through personalized meal plans and education."
    },
    {
        "user": {"first_name": "Yaw", "last_name": "Nkansah", "email": "yaw.nkansah@example.com"},
        "gender": "Male",
        "age": 41,
        "contact_one": "+233245556677",
        "contact_two": "+233545556677",
        "nationality": "Ghanaian",
        "specialization": "Psychologist",
        "years_of_experience": 13,
        "languages": ["English", "Twi"],
        "bio": "Experienced psychologist focused on mental health counseling and behavioral therapy for adults and teens."
    },
    {
        "user": {"first_name": "Esi", "last_name": "Bonsu", "email": "esi.bonsu@example.com"},
        "gender": "Female",
        "age": 36,
        "contact_one": "+233234567890",
        "contact_two": None,
        "nationality": "Ghanaian",
        "specialization": "Gynecologist",
        "years_of_experience": 12,
        "languages": ["English", "Fante"],
        "bio": "Dedicated to women's reproductive health and wellness. Known for compassionate care and patient advocacy."
    },
    {
        "user": {"first_name": "Nana", "last_name": "Addai", "email": "nana.addai@example.com"},
        "gender": "Other",
        "age": 30,
        "contact_one": "+233232323232",
        "contact_two": "+233542323232",
        "nationality": "Ghanaian",
        "specialization": "Neurologist",
        "years_of_experience": 7,
        "languages": ["English"],
        "bio": "Neurology expert providing care for patients with brain and nervous system disorders. Enthusiastic about brain research."
    },
    {
        "user": {"first_name": "Joseph", "last_name": "Antwi", "email": "joseph.antwi@example.com"},
        "gender": "Male",
        "age": 50,
        "contact_one": "+233209988776",
        "contact_two": None,
        "nationality": "Ghanaian",
        "specialization": "Oncologist",
        "years_of_experience": 20,
        "languages": ["English", "Twi"],
        "bio": "Veteran oncologist with two decades of experience in cancer treatment, research, and patient support."
    },
    {
        "user": {"first_name": "Akua", "last_name": "Mensima", "email": "akua.mensima@example.com"},
        "gender": "Female",
        "age": 27,
        "contact_one": "+233261122334",
        "contact_two": None,
        "nationality": "Ghanaian",
        "specialization": "Pharmacist",
        "years_of_experience": 3,
        "languages": ["English", "Twi"],
        "bio": "Friendly and knowledgeable pharmacist helping patients understand medications and stay safe with prescriptions."
    }
]
