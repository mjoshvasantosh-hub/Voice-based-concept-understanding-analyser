import whisper

_model = None

def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model

def transcribe_audio(file_path):
    model = get_model()
    result = model.transcribe(file_path)
    return result["text"]

if __name__ == "__main__":
    text = transcribe_audio("sample.mp3")
    print("Transcript:", text)