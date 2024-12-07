import streamlit as st
import pandas as pd
from io import BytesIO

# Inicializando os dados
if "processos" not in st.session_state:
    st.session_state["processos"] = []

# Título do Aplicativo
st.title("Gerenciador de Processos e Recursos")

# Formulário para adicionar dados do processo
st.subheader("Adicionar Dados do Processo")
numero_processo = st.text_input("Número do Processo:")
tipo_recurso_1 = st.selectbox("Recurso 1:", ["Nenhum", "Recurso Ordinário", "Agravo de Instrumento", "Agravo de Petição"])
tipo_recurso_2 = st.selectbox("Recurso 2:", ["Nenhum", "Recurso Ordinário", "Agravo de Instrumento", "Agravo de Petição"])
tipo_recurso_3 = st.selectbox("Recurso 3:", ["Nenhum", "Recurso Ordinário", "Agravo de Instrumento", "Agravo de Petição"])

st.markdown("### Tópicos por Recurso")

# Seleção de tópicos para cada recurso
col1, col2, col3 = st.columns(3)
preliminares_1 = col1.selectbox("Preliminares R1:", range(0, 7))
prejudiciais_1 = col2.selectbox("Prejudiciais R1:", range(0, 7))
merito_1 = col3.selectbox("Tópicos Mérito R1:", range(1, 36))

preliminares_2 = col1.selectbox("Preliminares R2:", range(0, 7))
prejudiciais_2 = col2.selectbox("Prejudiciais R2:", range(0, 7))
merito_2 = col3.selectbox("Tópicos Mérito R2:", range(1, 36))

preliminares_3 = col1.selectbox("Preliminares R3:", range(0, 7))
prejudiciais_3 = col2.selectbox("Prejudiciais R3:", range(0, 7))
merito_3 = col3.selectbox("Tópicos Mérito R3:", range(1, 36))

# Botão para adicionar os dados do processo
if st.button("Adicionar Processo"):
    if numero_processo:
   
