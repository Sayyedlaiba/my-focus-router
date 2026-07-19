import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
import time

st.set_page_config(page_title="Deep Work Router", page_icon="🚀", layout="centered")

st.title("🚀 Deep Work Voice Router")
st.write("Click the mic below and say **'start focus'** or **'deep work'** to launch your environment!")

# Initialize session states to track focus sessions and warnings
if "focus_active" not in st.session_state:
    st.session_state.focus_active = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "warning_msg" not in st.session_state:
    st.session_state.warning_msg = ""

# 1. The Browser Audio Recorder Component
audio_data = mic_recorder(
    start_prompt="🎙️ Click to Speak",
    stop_prompt="🛑 Click to Stop Recording",
    just_once=True,
    format="wav",
    key="speaker"
)

# 2. Process the voice recording if it exists
if audio_data and not st.session_state.focus_active:
    audio_bytes = audio_data['bytes']
    audio_file = io.BytesIO(audio_bytes)
    
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio_recorded = recognizer.record(source)
        
        try:
            with st.spinner("🧠 Brain processing your voice..."):
                command = recognizer.recognize_google(audio_recorded).lower()
            
            st.success(f"Heard: \"{command}\"")
            
            if "start focus" in command or "deep work" in command:
                st.session_state.focus_active = True
                st.session_state.start_time = time.time()
                st.session_state.warning_msg = "" # Reset warnings
                st.rerun()
            else:
                st.warning("Trigger phrase not recognized. Try saying 'start focus'!")
                
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please speak clearly closer to the mic.")
        except sr.RequestError:
            st.error("Speech Recognition API service is down.")

# 3. Active Focus Mode UI
if st.session_state.focus_active:
    duration = 60 # Extended to 60 seconds to give you time to test it
    elapsed = time.time() - st.session_state.start_time
    remaining = int(duration - elapsed)
    
    if remaining > 0:
        st.header("⏱️ Focus Mode Active!")
        st.progress(remaining / duration)
        st.metric(label="Time Remaining", value=f"{remaining} seconds")
        
        st.info("🔗 **Your Workspace is Ready:** [Click here to open Python Documentation](https://docs.python.org/3/)")
        
        # --- NEW INTERACTIVE DISTRACTION TRAP FEATURE ---
        st.markdown("---")
        st.subheader("😈 The Distraction Trap")
        st.write("Test the router! If you feel an impulse to visit a distracting site, type it below:")
        
        # Text input acts as a honeypot trap
        user_impulse = st.text_input("Where do you want to go?", value="", placeholder="e.g., youtube.com, facebook.com", key="trap_input")
        
        # Check if the user typed a blacklisted site
        DISTRACTING_SITES = ["youtube.com", "facebook.com", "twitter.com", "instagram.com", "reddit.com"]
        if user_impulse:
            matched_site = [site for site in DISTRACTING_SITES if site in user_impulse.lower()]
            if matched_site:
                st.session_state.warning_msg = f"🛑 Intercepted! You tried to search for **{matched_site[0]}**. Stay focused on your documentation!"
                # Force an app rerun to clear the input text box text instantly
                st.rerun()
        
        # Display the warning if triggered
        if st.session_state.warning_msg:
            st.error(st.session_state.warning_msg)
        # ------------------------------------------------
        
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.focus_active = False
        st.session_state.warning_msg = ""
        st.balloons()
        st.success("🎉 Session complete! Excellent deep work. Go take a break!")
