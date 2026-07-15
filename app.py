import streamlit as st
import matplotlib.pyplot as plt
import librosa
import librosa.display
import os

from audio_utils import extract_all_features
from speech_to_text import transcribe_audio
from semantic_eval import compute_similarity
from scoring_engine import get_filler_word_stats, compute_final_score
from report_generator import generate_pdf_report

st.set_page_config(page_title="Voice Based Concept Understanding Analyser", layout="centered")
st.title("🎙️ Voice Based Concept Understanding Analyser")
st.write("Upload a voice explanation of a concept, and compare it against a reference answer.")

reference_text = st.text_area("Enter the reference/correct explanation of the concept:")
uploaded_file = st.file_uploader("Upload your audio explanation", type=["wav", "mp3"])

if uploaded_file is not None and reference_text.strip() != "":
    file_path = os.path.join("temp_audio", uploaded_file.name)
    os.makedirs("temp_audio", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.audio(file_path)

    if st.button("Analyze Concept Understanding"):
        with st.spinner("Processing and evaluating..."):
            audio_features = extract_all_features(file_path)
            transcript = transcribe_audio(file_path)
            similarity_score = compute_similarity(transcript, reference_text)
            filler_stats = get_filler_word_stats(transcript)
            final_result = compute_final_score(similarity_score, audio_features)

        st.success("Analysis Completed")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Transcribed Explanation")
            st.write(transcript)
        with col2:
            st.subheader("Final Evaluation")
            st.metric("Understanding Score", f"{final_result['overall_score']}/100")
            st.write(f"**{final_result['understanding_level']}**")

        m1, m2, m3 = st.columns(3)
        m1.metric("Semantic Similarity", similarity_score)
        m2.metric("Filler Word Ratio", filler_stats["filler_ratio"])
        m3.metric("Confidence (Energy)", audio_features["rms_energy"])

        st.subheader("Audio Visualization")
        audio_signal, sr = librosa.load(file_path, sr=16000)
        fig, ax = plt.subplots()
        librosa.display.waveshow(audio_signal, sr=sr, ax=ax)
        ax.set_title("Audio Waveform")
        st.pyplot(fig)

        pdf_buffer = generate_pdf_report(transcript, reference_text, final_result, filler_stats)
        st.download_button("Download PDF Report", data=pdf_buffer, file_name="evaluation_report.pdf", mime="application/pdf")

else:
    st.info("Please enter a reference explanation and upload an audio file to begin.")