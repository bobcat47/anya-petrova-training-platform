from modules.ai_services import AIServices
import random

class VoiceSynthesizer:
    VOICE_OPTIONS = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    
    def create_voice_profile(self, profile):
        gender_bias = {
            "male": ["onyx", "echo"],
            "female": ["nova", "shimmer"],
            "neutral": ["alloy", "fable"]
        }
        
        # Determine gender from name or random
        first_char = profile['name'][0].lower()
        gender = "female" if first_char in "aeiou" else "male"
        if random.random() > 0.7:
            gender = "neutral"
        
        # Select voice
        voice = random.choice(gender_bias[gender])
        
        voice_profile = {
            "gender": gender,
            "voice": voice,
            "stability": random.uniform(0.2, 0.8),
            "similarity_boost": random.uniform(0.5, 0.95)
        }
        profile['voice_profile'] = voice_profile
        return profile
    
    def generate_audio(self, text, profile):
        try:
            response = AIServices.generate_speech(
                text, 
                voice=profile['voice_profile']['voice']
            )
            return response
        except Exception as e:
            print(f"Voice generation error: {e}")
            return None
