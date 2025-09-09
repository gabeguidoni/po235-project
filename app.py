import streamlit as st

st.set_page_config(page_title="Leitor de PDFs", page_icon="📄")

st.title("📄 Carregue aqui os relatórios")

arquivos = st.file_uploader(
    "Envie um ou mais relatórios em PDF", type=["pdf"], accept_multiple_files=True
)

if arquivos:
    st.subheader("Arquivos recebidos")
    for i, f in enumerate(arquivos, start=1):
        st.write(f"{i}. {f.name}")
else:
    st.info("Nenhum arquivo enviado.")
