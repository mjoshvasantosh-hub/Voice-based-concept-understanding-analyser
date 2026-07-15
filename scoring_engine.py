def classify_understanding(similarity_score):
    if similarity_score >= 0.75:
        return "Strong Understanding"
    elif similarity_score >= 0.5:
        return "Moderate Understanding"
    else:
        return "Poor Understanding"

def get_filler_word_stats(transcript_text):
    fillers = ["um", "uh", "like", "you know", "actually"]
    words = transcript_text.lower().split()
    filler_count = sum(1 for w in words if w in fillers)
    total_words = len(words)
    ratio = round(filler_count / total_words, 3) if total_words else 0
    return {"filler_count": filler_count, "total_words": total_words, "filler_ratio": ratio}

def compute_final_score(similarity_score, audio_features):
    understanding_level = classify_understanding(similarity_score)
    overall_score = round(similarity_score * 100, 1)
    return {
        "overall_score": overall_score,
        "understanding_level": understanding_level,
        "pause_ratio": audio_features.get("pause_ratio"),
        "rms_energy": audio_features.get("rms_energy"),
    }
