from faker import Faker
from modules.ai_services import AIServices
from datetime import datetime, timedelta
import random

class KYCSimulator:
    def __init__(self):
        self.faker = Faker()
    
    def generate_fake_documents(self, profile):
        # Generate realistic documents using Faker
        docs = []
        
        # Passport
        docs.append({
            "type": "passport",
            "name": profile['name'],
            "id_number": self.faker.passport_number(),
            "nationality": self.faker.country(),
            "dob": self.faker.date_of_birth(minimum_age=21, maximum_age=70).strftime("%Y-%m-%d"),
            "issue_date": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            "expiry_date": (datetime.now() + timedelta(days=random.randint(365, 365*10))).strftime("%Y-%m-%d"),
            "photo": AIServices.generate_image(f"Passport photo of {profile['name']}, {profile['origin']} occult specialist")
        })
        
        # Utility bill
        docs.append({
            "type": "utility_bill",
            "name": profile['name'],
            "address": self.faker.address().replace('\n', ', '),
            "account_number": self.faker.bban(),
            "amount": f"${random.randint(50, 500)}.{random.randint(0,99):02d}",
            "due_date": (datetime.now() + timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d"),
            "service": random.choice(["Electricity", "Water", "Internet", "Gas"])
        })
        
        # Bank statement
        transactions = []
        for _ in range(10):
            transactions.append({
                "date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%m-%d"),
                "description": self.faker.catch_phrase(),
                "amount": f"{random.choice(['-','+'])}${random.randint(10, 500)}.{random.randint(0,99):02d}"
            })
        
        docs.append({
            "type": "bank_statement",
            "name": profile['name'],
            "account_number": self.faker.iban(),
            "balance": f"${random.randint(1000, 10000)}.{random.randint(0,99):02d}",
            "transactions": transactions
        })
        
        return docs
    
    def simulate_kyc_check(self, documents):
        # Use AI to analyze documents
        doc_text = "\n\n".join([str(doc) for doc in documents])
        prompt = f"""
        Analyze these fake identity documents for potential KYC verification issues:
        {doc_text}
        
        Identify 3-5 potential weaknesses that could be flagged during verification.
        Format as a JSON object with keys: 'score' (1-100), 'flags' (list of strings), 'verdict' (PASS/FAIL)
        """
        
        try:
            analysis = AIServices.generate_text(prompt)
            return eval(analysis)
        except:
            # Fallback analysis
            return {
                "score": random.randint(40, 90),
                "flags": ["Photo mismatch", "Inconsistent birth date", "Low-quality hologram"],
                "verdict": "PASS" if random.random() > 0.3 else "FAIL"
            }
