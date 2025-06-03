import random
from datetime import datetime, timedelta
from modules.ai_services import AIServices

class PersonaGenerator:
    # ... [keep existing traits and backstory elements] ...
    
    def generate_complete_persona(self, profile):
        """Generate detailed persona using GPT"""
        prompt = f"""
        Create a detailed psychological profile for a fictional character named {profile['name']}:
        - Origin: {profile['origin']}
        - Specialty: {profile['specialty']}
        - Realism level: {profile['realism']}
        
        Include:
        1. Psychological traits (primary and secondary)
        2. Moral alignment
        3. IQ estimate
        4. Dark triad scores (narcissism, machiavellianism, psychopathy)
        5. Communication style
        6. Backstory with key events
        7. Current motivations
        
        Format as JSON with keys: psychological_profile, communication_style, backstory
        """
        
        response = AIServices.generate_text(prompt)
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            persona = eval(response[json_start:json_end])
            profile.update({"persona": persona})
        except:
            # Fallback to manual generation if AI fails
            profile = self._manual_persona(profile)
        return profile
    
    def _manual_persona(self, profile):
        # ... [keep existing manual generation as fallback] ...
        return profile

class ContentGenerator:
    def generate_communication_sample(self, profile, length="medium", format="email"):
        prompt = f"""
        Write a {length} {format} from {profile['name']}, a {profile['origin']} specialist in {profile['specialty']}.
        Character traits: {profile['persona']['psychological_profile']['primary_trait']}, {profile['persona']['psychological_profile']['secondary_trait']}
        Communication style: {profile['persona']['communication_style']['speech_pattern']}
        
        Make it sound authentic and in-character. Include occult references where appropriate.
        """
        return AIServices.generate_text(prompt)
    
    def generate_full_identity_package(self, profile):
        # Generate social media content
        social_prompt = f"""
        Create social media content for {profile['name']}:
        - 3 Twitter/X posts
        - 2 Facebook updates
        - 1 Instagram caption with hashtags
        
        Style: {profile['persona']['communication_style']['speech_pattern']}
        Interests: {profile['specialty']}, occult practices
        """
        
        # Generate documentation
        doc_prompt = f"""
        Create a realistic personal bio for {profile['name']} including:
        - Background story
        - Education
        - Professional experience related to {profile['specialty']}
        - Personal interests
        - Contact information (fictional)
        """
        
        return {
            "social_media": AIServices.generate_text(social_prompt),
            "documentation": AIServices.generate_text(doc_prompt),
            "communication_samples": [
                self.generate_communication_sample(profile, format="email"),
                self.generate_communication_sample(profile, format="text message"),
                self.generate_communication_sample(profile, format="diary entry")
            ]
        }
