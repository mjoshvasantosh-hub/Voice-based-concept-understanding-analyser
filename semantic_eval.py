from sentence_transformers import SentenceTransformer, util

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def compute_similarity(transcript_text, reference_text):
    model = get_model()
    emb1 = model.encode(transcript_text, convert_to_tensor=True)
    emb2 = model.encode(reference_text, convert_to_tensor=True)
    raw_score= util.cos_sim(emb1, emb2).item()
    normalized_score = max(0.0,min(1.0, raw_score))
    return round(normalized_score, 3)