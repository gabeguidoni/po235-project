import streamlit as st
from pdf_handler import pdf_handler

st.set_page_config(page_title="Leitor de PDFs", page_icon="📄")

st.title("📄 Carregue aqui o relatório")

arquivo = st.file_uploader(
    "Envie o relatório simplificado", type=["pdf"], accept_multiple_files=False
)

if arquivo:
    new_file = pdf_handler(arquivo, arquivo.name)
    st.subheader("Labels desse relatório")
    st.write(new_file)
else:
    st.info("Nenhum arquivo enviado.")

# --- Rodapé ---
st.markdown(
    """
    <hr>
    <div style='text-align: left; color: gray;'>
        Desenvolvido para a disciplina de Pós Graduação no ITA PO-235 por:
        <br>Gabriel Guidoni
        <br>Danilo Matos
        <br>Daniel Monteiro
    </div>
    """,
    unsafe_allow_html=True,
)
