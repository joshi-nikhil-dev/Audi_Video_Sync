from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip

def sync_corrected_audio_with_video(corrected_audio_path, timestamps, video_path):
    video = VideoFileClip(video_path)
    corrected_audio = AudioSegment.from_file(corrected_audio_path)
    
    # Create a silent audio track with the same length as the video's audio
    video_audio_duration_ms = video.audio.duration * 1000  # Convert video audio duration to milliseconds
    synced_audio = AudioSegment.silent(duration=video_audio_duration_ms)
    
    total_duration = 0  # To keep track of the current position in the corrected audio

    # Loop over each timestamp and place the corrected audio at the appropriate start time
    for i, timestamp in enumerate(timestamps):
        start_time_ms = timestamp['start_time'] * 1000  # Convert start time to milliseconds
        
        # Extract the corresponding audio segment from the corrected audio
        corrected_segment = corrected_audio[total_duration:]  # Get remaining corrected audio starting from total_duration
        
        # Overlay the corrected segment at the exact start time
        synced_audio = synced_audio.overlay(corrected_segment, position=start_time_ms)
        
        # Update total_duration to skip the used portion of corrected audio
        total_duration += len(corrected_segment)

    # Export the synced audio
    synced_audio_path = corrected_audio_path.replace(".mp3", "_synced.mp3")
    synced_audio.export(synced_audio_path, format="mp3")

    # Set this synced audio to the video
    new_audio = AudioFileClip(synced_audio_path)
    final_video = video.set_audio(new_audio)

    output_video_path = video_path.replace(".mp4", "_synced.mp4")
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

    return output_video_path
