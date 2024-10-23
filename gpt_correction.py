import requests
import os

# Azure OpenAI API credentials
api_key = "API-KEY"  # Use your actual API key
endpoint_url = "ENDPOINT-URL"

def correct_transcription(transcription):
    if not transcription.strip():
        raise ValueError("Transcription is empty or invalid.")
    
    # Define the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    # Define the payload for the request without the preamble
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": f"Correct the grammar and punctuation of the following text: \"{transcription}\""}
        ],
        "temperature": 0.7,
        "max_tokens": len(transcription)  # Set the max tokens based on transcription length
    }
    
    # Send the request to the Azure OpenAI API
    response = requests.post(endpoint_url, headers=headers, json=payload)

    # Check for a successful response
    if response.status_code == 200:
        # Parse the JSON response
        corrected_text = response.json()['choices'][0]['message']['content'].strip()
        
        # Match the length of the corrected transcription to the original transcription
        corrected_text = match_length(transcription, corrected_text)
        
        return corrected_text
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def match_length(original_text, corrected_text):
    """
    Adjusts the corrected_text to match the length of original_text.
    If the corrected_text is longer, it will be truncated.
    If it's shorter, spaces will be added to match the length.
    """
    original_length = len(original_text)
    corrected_length = len(corrected_text)
    
    # Truncate corrected_text if it's too long
    if corrected_length > original_length:
        return corrected_text[:original_length]
    
    # Pad corrected_text with spaces if it's too short
    elif corrected_length < original_length:
        return corrected_text.ljust(original_length)
    
    # Return the corrected_text if the lengths match
    return corrected_text
