import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
import time

st.set_page_config(page_title="Deep Work Router", page_icon="🚀", layout="centered")

st.title("🚀 Deep Work Voice Router")
st.write("Click the mic below and say **'start focus'** or **'deep work'** to launch your environment!")

# Initialize session states to track if we are in focus mode
if "focus_active" not in st.session_state:
    st.session_state.focus_active = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0

# 1. The Browser Audio Recorder Component
audio_data = mic_recorder(
    start_prompt="🎙️ Click to Speak",
    stop_prompt="🛑 Click to Stop Recording",
    just_once=True,
    key="speaker"
)

# 2. Process the voice recording if it exists
if audio_data and not st.session_state.focus_active:
    # Convert raw browser audio bytes into a file-like object Python can read
    audio_bytes = audio_data['bytes']
    audio_file = io.BytesIO(audio_bytes)
    
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        # Load the recorded audio
        audio_recorded = recognizer.record(source)
        
        try:
            with st.spinner("🧠 Brain processing your voice..."):
                command = recognizer.recognize_google(audio_recorded).lower()
            
            st.success(f"Heard: \"{command}\"")
            
            # Check for our trigger phrases
            if "start focus" in command or "deep work" in command:
                st.session_state.focus_active = True
                st.session_state.start_time = time.time()
                st.rerun() # Refresh the page to start the timer
            else:
                st.warning("Trigger phrase not recognized. Try saying 'start focus'!")
                
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please speak clearly closer to the mic.")
        except sr.RequestError:
            st.error("Speech Recognition API service is down.")

# 3. Active Focus Mode UI
if st.session_state.focus_active:
    duration = 30 # 30-second test session
    elapsed = time.time() - st.session_state.start_time
    remaining = int(duration - elapsed)
    
    if remaining > 0:
        st.header("⏱️ Focus Mode Active!")
        st.progress(remaining / duration)
        st.metric(label="Time Remaining", value=f"{remaining} seconds")
        
        # Link routing for the user
        st.info("🔗 **Your Workspace is Ready:** [Click here to open Python Documentation](https://docs.python.org/3/)")
        
        # Cloud friendly distraction mitigation: Interactive Commitment Checklist
        st.subheader("🛡️ Focus Commitment Checklist")
        st.markdown("Since this app is running in the cloud, check these off to lock in your focus:")
        st.checkbox("I have closed my social media tabs.")
        st.checkbox("My phone is placed face down or in another room.")
        st.checkbox("I am committed to staying on the documentation page.")
        
        # Auto-refresh the Streamlit page every second to update the countdown
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.focus_active = False
        st.balloons()
        st.success("🎉 Session complete! Excellent deep work. Go take a break!")
