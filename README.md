# Audio Transcription Correction with Azure OpenAI

This project extracts audio from a video, transcribes the audio, and corrects the transcription using the Azure OpenAI GPT-4 API. The corrected transcription is adjusted to match the original transcription's length to maintain synchronization with the video.

## Features

- Extracts and transcribes audio from a video.
- Corrects the transcription using Azure OpenAI API.
- Ensures the corrected transcription has the same length as the original transcription to avoid overlap.
- Syncs corrected audio with video based on timestamps.

- The basic idea that I had was to get a timestamo for each sentence for when it is being spoken in the video. Then according to those timestamps I append the audio to the video so that it syncs audio with the video. 
The other idea that I had was to use a CNN. I train a CNN foe detect when the person is speaking. Then I get the timestamps of when the person is speaking by the CNN and using those timestamps, I can append the corrected audio.

- I have not been able to sync the audio and the video perfectly, But I have done as much as I can.


# How to run it

- Clone the github repository.
- run "pip install -r requirements.txt"
- Have the gcloud .json key in the folder.
- rename the json key in text_to_speech.py, transcribe.py and app.py
- Now run the streamlit application using "streamlit run app.py"
- You can upload the video and then check the terminal to see how its working. After it has processed everything, The video will be displayed on the web where the streamlit application is open.
