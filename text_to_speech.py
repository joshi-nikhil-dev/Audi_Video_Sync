from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "brilliant-forge-438817-q1-b9cd6eebfc19.json"

def text_to_speech(text, output_audio_file):
    if not text:
        raise ValueError("Input text for speech synthesis is empty.")
        
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Replace with a valid voice name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_audio_file, "wb") as out:
        out.write(response.audio_content)
