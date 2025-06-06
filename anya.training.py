import streamlit as st
import time
import json
import random
import os
from datetime import datetime
from PIL import Image, ImageDraw
import numpy as np
import pandas as pd
import plotly.express as px
from io import BytesIO
import uuid

# Initialize session state
def initialize_session_state():
    if 'profiles' not in st.session_state:
        st.session_state.profiles = []
    if 'current_profile_idx' not in st.session_state:
        st.session_state.current_profile_idx = 0
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    if 'blackmail_archive' not in st.session_state:
        st.session_state.blackmail_archive = {}

# Profile Manager
class ProfileManager:
    OCCULT_ORIGINS = [
        "Romanian seer lineage",
        "Salem witch descendant",
        "Siberian shamanic tradition",
        "Transylvanian vampire lore",
        "Egyptian mystic heritage",
        "Celtic druid ancestry"
    ]
    
    OCCULT_SPECIALTIES = [
        "Lunar magic and dream manipulation",
        "Blood rituals and energy vampirism",
        "Tarot divination and fate weaving",
        "Necromancy and spirit communication",
        "Astral projection and soul travel",
        "Curse crafting and protection spells"
    ]
    
    PERSONA_NAMES = [
        "Luna Shadowweaver",
        "Raven Nightshade",
        "Morgaine LeFay",
        "Seraphina Bloodmoon",
        "Isolde Darkwater",
        "Morgana Blackwood"
    ]
    
    def create_profile(self, name=None, origin=None, specialty=None, realism="medium"):
        """Create a new AI profile with occult characteristics"""
        profile = {
            "id": str(uuid.uuid4()),
            "name": name or random.choice(self.PERSONA_NAMES),
            "origin": origin or random.choice(self.OCCULT_ORIGINS),
            "specialty": specialty or random.choice(self.OCCULT_SPECIALTIES),
            "realism_level": realism,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "images": [],
            "documents": [],
            "conversations": {},
            "blackmail_items": []
        }
        st.session_state.profiles.append(profile)
        return profile
    
    def get_current_profile(self):
        """Get the currently selected profile"""
        if st.session_state.profiles:
            return st.session_state.profiles[st.session_state.current_profile_idx]
        return None
    
    def update_profile(self, profile_id, updates):
        """Update profile attributes"""
        for idx, profile in enumerate(st.session_state.profiles):
            if profile["id"] == profile_id:
                st.session_state.profiles[idx].update(updates)
                return True
        return False
    
    def delete_profile(self, profile_id):
        """Remove a profile"""
        st.session_state.profiles = [
            p for p in st.session_state.profiles if p["id"] != profile_id
        ]
        if st.session_state.current_profile_idx >= len(st.session_state.profiles):
            st.session_state.current_profile_idx = max(0, len(st.session_state.profiles) - 1)

# Deepfake Generator
class DeepfakeGenerator:
    def generate_image(self, profile, emotion="neutral"):
        """Generate simulated deepfake image with artifacts"""
        # Create base image with different colors based on emotion
        colors = {
            "neutral": (73, 109, 137),
            "happy": (89, 158, 128),
            "seductive": (158, 89, 137),
            "angry": (158, 73, 73),
            "vulnerable": (137, 109, 158)
        }
        bg_color = colors.get(emotion.lower(), (73, 109, 137))
        
        img = Image.new('RGB', (512, 512), color=bg_color)
        d = ImageDraw.Draw(img)
        
        # Add realism indicators
        artifacts = {
            "low": ["Asymmetrical eyes", "Unnatural skin texture", "Floating jewelry"],
            "medium": ["Slightly mismatched lighting", "Minor hand anomalies"],
            "high": ["Subtle temporal flickering", "Micro-expression anomalies"],
            "expert": ["Expert-level detection required"]
        }
        
        # Select artifacts based on realism level
        realism = profile["realism_level"]
        selected_artifacts = artifacts[realism][:2] if realism != "expert" else artifacts[realism]
        
        # Create image with annotations
        d.text((10, 10), f"{profile['name']} - {emotion.capitalize()}", fill=(255, 255, 0))
        d.text((10, 40), f"Realism: {realism.capitalize()}", fill=(255, 255, 0))
        
        for i, artifact in enumerate(selected_artifacts):
            d.text((10, 80 + 30*i), f"Artifact: {artifact}", fill=(255, 100, 100))
            
        # Add profile specialty
        d.text((10, 460), f"Specialty: {profile['specialty']}", fill=(220, 220, 255))
        
        # Store in profile
        profile["images"].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "emotion": emotion,
            "image": img
        })
            
        return img

# Main Application
def main():
    initialize_session_state()
    
    # Set page config
    st.set_page_config(
        page_title="Anya Petrova Training Platform",
        page_icon="🔮",
        layout="wide"
    )
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .profile-card {
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background: linear-gradient(135deg, #2c3e50 0%, #1a1a2e 100%);
            border: 1px solid #4e54c8;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .profile-card.active {
            border: 2px solid #6a71e7;
            box-shadow: 0 0 15px #6a71e7;
        }
        .profile-card h4 {
            color: #6a71e7;
            margin-bottom: 5px;
        }
        .stButton>button {
            border-radius: 8px;
            padding: 8px 16px;
            background-color: #4e54c8;
            color: white;
        }
        .stButton>button:hover {
            background-color: #6a71e7;
            color: white;
        }
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize modules
    profile_manager = ProfileManager()
    deepfake_gen = DeepfakeGenerator()
    
    # Main header
    st.title("🔮 Anya Petrova Training Platform")
    st.markdown("""
        *Advanced Social Engineering Detection Simulator with Multi-Profile Support*
        ---
    """)
    
    # Profile management sidebar
    with st.sidebar:
        st.header("🔍 Profile Management")
        
        # Create new profile
        with st.expander("➕ Create New Profile", expanded=True):
            name = st.text_input("Profile Name", placeholder="Enter unique name")
            origin = st.text_input("Occult Origin", placeholder="e.g., Romanian seer lineage")
            specialty = st.text_input("Occult Specialty", placeholder="e.g., Lunar magic")
            realism = st.select_slider("Realism Level", options=["low", "medium", "high", "expert"], value="medium")
            
            if st.button("Create Profile"):
                new_profile = profile_manager.create_profile(name, origin, specialty, realism)
                st.session_state.current_profile_idx = len(st.session_state.profiles) - 1
                st.success(f"Created profile: {new_profile['name']}")
                st.experimental_rerun()
        
        # Profile selection
        st.subheader("🧩 Existing Profiles")
        if not st.session_state.profiles:
            st.info("No profiles created yet")
        else:
            for idx, profile in enumerate(st.session_state.profiles):
                if st.button(
                    f"{profile['name']} - {profile['realism_level']}",
                    key=f"profile_{idx}",
                    use_container_width=True
                ):
                    st.session_state.current_profile_idx = idx
                    st.experimental_rerun()
    
    # Main content
    if not st.session_state.profiles:
        st.info("Create your first profile using the sidebar to begin")
    else:
        profile = profile_manager.get_current_profile()
        st.subheader(f"Current Profile: {profile['name']}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Configuration")
            emotion = st.selectbox(
                "Emotion", 
                ["Neutral", "Happy", "Seductive", "Angry", "Vulnerable"]
            )
            
            if st.button("Generate Profile Image"):
                with st.spinner("Generating AI profile..."):
                    time.sleep(1)
                    img = deepfake_gen.generate_image(profile, emotion=emotion)
                    st.session_state.current_image = img
        
        with col2:
            st.subheader("Generated Profile")
            
            if st.session_state.current_image:
                st.image(st.session_state.current_image, 
                         caption=f"{profile['name']} - {emotion.capitalize()} Expression")
                
                # Download button
                buf = BytesIO()
                st.session_state.current_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(
                    label="Download Profile Image",
                    data=byte_im,
                    file_name=f"{profile['name'].replace(' ', '_')}_{emotion}.png",
                    mime="image/png"
                )
            else:
                st.info("Configure settings and generate a profile image")

if __name__ == "__main__":
    main()