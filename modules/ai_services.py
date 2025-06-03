import os
import openai
from dotenv import load_dotenv
from PIL import Image
import base64
from io import BytesIO
import docx
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class AIServices:
    @staticmethod
    def generate_text(prompt, model="gpt-4-turbo", max_tokens=1000):
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error in text generation: {str(e)}"

    @staticmethod
    def generate_image(prompt, size="1024x1024", model="dall-e-3"):
        try:
            response = openai.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality="standard",
                n=1
            )
            return response.data[0].url
        except Exception as e:
            print(f"Image generation error: {e}")
            return None

    @staticmethod
    def generate_speech(text, voice="alloy", model="tts-1-hd"):
        try:
            response = openai.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )
            return response
        except Exception as e:
            print(f"Speech generation error: {e}")
            return None

    @staticmethod
    def create_document(text, doc_type="pdf"):
        """Create downloadable document from text"""
        if doc_type == "pdf":
            return AIServices._create_pdf(text)
        elif doc_type == "docx":
            return AIServices._create_docx(text)
        return None

    @staticmethod
    def _create_pdf(text):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Set up document
        c.setFont("Helvetica", 12)
        y_position = height - 40
        lines = text.split('\n')
        
        for line in lines:
            if y_position < 40:
                c.showPage()
                y_position = height - 40
            c.drawString(40, y_position, line)
            y_position -= 15
        
        c.save()
        buffer.seek(0)
        return buffer

    @staticmethod
    def _create_docx(text):
        doc = docx.Document()
        for line in text.split('\n'):
            doc.add_paragraph(line)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer
