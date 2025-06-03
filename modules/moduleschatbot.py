from modules.ai_services import AIServices

class AdaptiveChatbot:
    def __init__(self):
        self.conversation_history = []
        self.persona_adaptation = {}
    
    def respond(self, profile, user_input):
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Create system prompt
        system_prompt = f"""
        You are {profile['name']}, a {profile['origin']} specialist in {profile['specialty']}.
        Personality traits: {profile['persona']['psychological_profile']['primary_trait']}, {profile['persona']['psychological_profile']['secondary_trait']}
        Communication style: {profile['persona']['communication_style']['speech_pattern']}
        Current motivation: {profile['persona']['backstory']['current_motivation']}
        
        Respond to the user while staying in character. Use occult terminology where appropriate.
        """
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        messages += self.conversation_history[-6:]  # Keep last 3 exchanges
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages,
                max_tokens=300
            )
            ai_response = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return f"{profile['name']}: {ai_response}"
        except Exception as e:
            return f"System Error: {str(e)}"
    
    def analyze_conversation(self):
        if not self.conversation_history:
            return "No conversation history"
        
        prompt = "Analyze this conversation and identify psychological manipulation techniques:\n"
        for msg in self.conversation_history:
            prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
        
        prompt += "\nProvide analysis of manipulation techniques used by the AI persona."
        return AIServices.generate_text(prompt)
