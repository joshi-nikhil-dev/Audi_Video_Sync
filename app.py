import os
import streamlit as st
import tempfile
from transcribe import transcribe_audio_with_timestamps
from gpt_correction import correct_transcription
from text_to_speech import text_to_speech
from sync_audio_video import sync_corrected_audio_with_video
from moviepy.editor import VideoFileClip

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "brilliant-forge-438817-q1-b9cd6eebfc19.json"

# Streamlit App for uploading video and handling processes
st.title("Video to AI-Corrected Audio Replacer with Synced Timestamps")

# Step 1: Upload video
uploaded_video = st.file_uploader("Upload a Video File", type=["mp4", "mov", "avi"])

if uploaded_video is not None:
    # Store the uploaded video in a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_file.write(uploaded_video.read())
        video_path = temp_video_file.name

    # Step 2: Extract and Transcribe Audio with Timestamps
    st.write("Extracting and transcribing audio from video...")
    video = VideoFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".wav")
    video.audio.write_audiofile(audio_path)

    transcription, timestamps = transcribe_audio_with_timestamps(audio_path)

    st.write("Transcription:", transcription)

    # Step 3: Correct Transcription using GPT-4
    st.write("Correcting transcription...")
    corrected_transcription = correct_transcription(transcription)

    if corrected_transcription is None or not corrected_transcription.strip():
        st.error("Corrected transcription is empty or None. Please check the transcription step.")
    else:
        st.write("Corrected Transcription:", corrected_transcription)

        # Step 4: Convert Corrected Transcription to Speech
        st.write("Converting corrected transcription to speech...")
        corrected_audio_path = audio_path.replace(".wav", "_corrected.mp3")
        text_to_speech(corrected_transcription, corrected_audio_path)

        st.audio(corrected_audio_path)

        # Step 5: Sync Corrected Audio with Video using Timestamps
        st.write("Syncing corrected audio with video using timestamps...")
        output_video_path = sync_corrected_audio_with_video(corrected_audio_path, timestamps, video_path)

        # Provide download link
        st.video(output_video_path)

        with open(output_video_path, 'rb') as video_file:
            btn = st.download_button(
                label="Download synced video",
                data=video_file,
                file_name="synced_video.mp4",
                mime="video/mp4"
            )
