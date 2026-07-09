""""
audio_utils.py
Audio loading and feature extraction utilities for the
Voice Based Concept Understanding Analyser (VBCUA).
"""

import librosa
import numpy as np


def load_audio(file_path, sr=16000):
    """
    Loads an audio file and returns the audio signal + sample rate.
    """
    audio, sample_rate = librosa.load(file_path, sr=sr)
    return audio, sample_rate


def get_duration(audio, sample_rate):
    """
    Returns the duration of the audio in seconds.
    """
    return librosa.get_duration(y=audio, sr=sample_rate)


def get_rms_energy(audio):
    """
    Returns the average RMS (loudness) energy of the audio.
    Higher value = louder/more energetic speech.
    """
    rms = librosa.feature.rms(y=audio)
    return float(np.mean(rms))


def get_zero_crossing_rate(audio):
    """
    Returns the average zero-crossing rate.
    Roughly indicates clarity/noisiness of the speech signal.
    """
    zcr = librosa.feature.zero_crossing_rate(y=audio)
    return float(np.mean(zcr))


def get_pause_ratio(audio, sample_rate, top_db=25):
    """
    Estimates how much of the audio is silence (pauses) vs speech.
    Returns a ratio between 0 and 1 (0 = no pauses, 1 = all silence).
    """
    intervals = librosa.effects.split(audio, top_db=top_db)
    speech_duration = sum((end - start) for start, end in intervals) / sample_rate
    total_duration = get_duration(audio, sample_rate)

    if total_duration == 0:
        return 0.0

    pause_duration = total_duration - speech_duration
    pause_ratio = pause_duration / total_duration
    return round(pause_ratio, 3)


def extract_all_features(file_path):
    """
    Loads an audio file and returns a dictionary of all extracted features.
    This is the main function other modules (like scoring_engine.py) will call.
    """
    audio, sample_rate = load_audio(file_path)

    features = {
        "duration_sec": round(get_duration(audio, sample_rate), 2),
        "rms_energy": round(get_rms_energy(audio), 5),
        "zero_crossing_rate": round(get_zero_crossing_rate(audio), 5),
        "pause_ratio": get_pause_ratio(audio, sample_rate),
    }

    return features


# Quick test — only runs if you execute this file directly
if __name__ == "__main__":
    test_file = "bagundu_poo.mp3"  # replace with your actual audio file name
    result = extract_all_features(test_file)
    print("Extracted Audio Features:")
    for key, value in result.items():
        print(f"  {key}: {value}")