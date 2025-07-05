import os
import streamlit as st
import pandas as pd
import tempfile
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.text_splitter import SentenceSplitter
from PyPDF2 import PdfReader
from pytube import YouTube

# Proteção por senha
st.set_page_config(page_title="RAG Técnico Telecom", layout="wide")
st.title("📡 Otimizador Técnico com IA (RAG)")
st.markdown("Envie arquivos (📄 PDF, CSV, TXT) ou link de vídeo 🎥 e pergunte sobre sua rede.")
if st.text_input("🔐 Digite a senha para acessar:", type="password") != os.getenv("APP_SENHA", "admin"):
    st.warning("Senha incorreta.")
    st.stop()

docs = []

# Função para detectar encoding e ler CSV
def read_csv_with_encoding(file):
    try:
        return pd.read_csv(file)
    except UnicodeDecodeError:
        file.seek(0)
        return pd.read_csv(file, encoding="ISO-8859-1")

# 📥 Upload de CSV
uploaded_csv = st.file_uploader("📈 Envie um CSV", type="csv")
if uploaded_csv:
    df = read_csv_with_encoding(uploaded_csv)
    st.success("CSV carregado!")
    st.dataframe(df.head())
    for _, row in df.iterrows():
        linha = " | ".join([f"{col}: {row[col]}" for col in df.columns])
        docs.append(linha)

# 📄 Upload de TXT ou PDF
uploaded_docs = st.file_uploader("📄 Envie arquivos TXT ou PDF", type=["txt", "pdf"], accept_multiple_files=True)
for file in uploaded_docs or []:
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = "
".join(page.extract_text() or "" for page in reader.pages)
    else:
        text = file.read().decode("utf-8", errors="ignore")
    docs.append(text)

# 🎥 Transcrição do YouTube sob demanda
youtube_url = st.text_input("🎬 Cole um link de vídeo do YouTube (opcional):")
if youtube_url:
    with st.spinner("Baixando e transcrevendo vídeo..."):
        try:
            import whisper
            model = whisper.load_model("tiny")
            yt = YouTube(youtube_url)
            stream = yt.streams.filter(only_audio=True).first()
            temp_audio = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            stream.download(filename=temp_audio.name)
            result = model.transcribe(temp_audio.name)
            docs.append(result["text"])
            st.success("Transcrição concluída!")
        except Exception as e:
            st.error(f"Erro: {e}")

# ✅ RAG e Pergunta
if docs:
    st.divider()
    st.subheader("🧠 Pergunta Técnica")
    question = st.text_input("Digite sua pergunta:")
    if question:
        with st.spinner("Consultando documentos..."):
            embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
            service_context = ServiceContext.from_defaults(
                embed_model=embed_model,
                text_splitter=SentenceSplitter(chunk_size=512, chunk_overlap=50)
            )
            index = VectorStoreIndex.from_documents(
                [SimpleDirectoryReader.from_text(doc).load_data()[0] for doc in docs],
                service_context=service_context
            )
            engine = index.as_query_engine()
            prompt = f"""
Você é um engenheiro especialista em redes móveis.

Considere os seguintes dados extraídos de documentos técnicos:
{question}

OBSERVAÇÃO:
Valores altos (ex: 10) em colunas como 'índice_taxa' e 'ue_medio' representam pior desempenho da rede.
Use esse conhecimento para recomendar ações de melhoria.
"""
            response = engine.query(prompt)
            st.markdown("### ✅ Resposta da IA:")
            st.success(str(response))
else:
    st.info("📥 Envie dados ou links para começar.")
