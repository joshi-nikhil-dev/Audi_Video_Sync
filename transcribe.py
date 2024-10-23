import os
import io
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "brilliant-forge-438817-q1-b9cd6eebfc19.json"

def split_audio(audio_file_path, chunk_length_ms=30000):
    audio = AudioSegment.from_wav(audio_file_path)
    chunks = []
    for i, chunk in enumerate(audio[::chunk_length_ms]):
        chunk_path = f"chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks

def transcribe_audio_with_timestamps(audio_file_path):
    client = speech.SpeechClient()

    audio_chunks = split_audio(audio_file_path)

    transcription = ""
    timestamps = []

    for chunk_path in audio_chunks:
        with io.open(chunk_path, "rb") as audio_file:
            content = audio_file.read()

        audio_segment = AudioSegment.from_wav(chunk_path)
        audio_segment = audio_segment.set_channels(1)
        mono_chunk_path = f"mono_{os.path.basename(chunk_path)}"
        audio_segment.export(mono_chunk_path, format="wav")

        audio = speech.RecognitionAudio(content=open(mono_chunk_path, "rb").read())
        
        sample_rate = audio_segment.frame_rate

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code="en-US",
            enable_word_time_offsets=True  # Enable timestamps
        )

        operation = client.long_running_recognize(config=config, audio=audio)
        print(f"Processing chunk: {mono_chunk_path}")
        response = operation.result(timeout=300)

        for result in response.results:
            for alternative in result.alternatives:
                transcription += alternative.transcript
                for word_info in alternative.words:
                    word = word_info.word
                    start_time = word_info.start_time.total_seconds()
                    end_time = word_info.end_time.total_seconds()
                    timestamps.append({
                        'word': word,
                        'start_time': start_time,
                        'end_time': end_time
                    })

        os.remove(chunk_path)
        os.remove(mono_chunk_path)

    return transcription, timestamps
