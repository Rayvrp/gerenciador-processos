import streamlit as st
import pandas as pd
from io import BytesIO

# Inicializando os dados
if "processos" not in st.session_state:
    st.session_state["processos"] = []

# Função para resetar os campos do formulário
def reset_campos():
    st.session_state["numero_processo"] = ""
    st.session_state["tipo_recurso_1"] = "Nenhum"
    st.session_state["tipo_recurso_2"] = "Nenhum"
    st.session_state["tipo_recurso_3"] = "Nenhum"
    st.session_state["preliminares_1"] = 0
    st.session_state["preliminares_2"] = 0
    st.session_state["preliminares_3"] = 0
    st.session_state["prejudiciais_1"] = 0
    st.session_state["prejudiciais_2"] = 0
    st.session_state["prejudiciais_3"] = 0
    st.session_state["merito_1"] = 1
    st.session_state["merito_2"] = 1
    st.session_state["merito_3"] = 1

# Inicializar os valores na primeira execução
if "numero_processo" not in st.session_state:
    reset_campos()

# Título do Aplicativo
st.title("Gerenciador de Processos e Recursos")

# Formulário para adicionar dados do processo
st.subheader("Adicionar Dados do Processo")
numero_processo = st.text_input("Número do Processo:", key="numero_processo")
tipo_recurso_1 = st.selectbox("Recurso 1:", ["Nenhum", "Recurso Ordinário", "Agravo de Instrumento", "Agravo de Petição"], key="tipo_recurso_1")
tipo_recurso_2 = st.selectbox("Recurso 2:", ["Nenhum", "Recurso Ordinário", "Agravo de Instrumento", "Agravo de Petição"], key="tipo_recurso_2")
tipo_recurso_3 = st.selectbox("Recurso 3:", ["Nenhum", "Recurso Ordinário", "Agravo de Instrumento", "Agravo de Petição"], key="tipo_recurso_3")

st.markdown("### Tópicos por Recurso")

# Seleção de tópicos para cada recurso
col1, col2, col3 = st.columns(3)
preliminares_1 = col1.selectbox("Preliminares R1:", range(0, 7), key="preliminares_1")
prejudiciais_1 = col2.selectbox("Prejudiciais R1:", range(0, 7), key="prejudiciais_1")
merito_1 = col3.selectbox("Tópicos Mérito R1:", range(1, 36), key="merito_1")

preliminares_2 = col1.selectbox("Preliminares R2:", range(0, 7), key="preliminares_2")
prejudiciais_2 = col2.selectbox("Prejudiciais R2:", range(0, 7), key="prejudiciais_2")
merito_2 = col3.selectbox("Tópicos Mérito R2:", range(1, 36), key="merito_2")

preliminares_3 = col1.selectbox("Preliminares R3:", range(0, 7), key="preliminares_3")
prejudiciais_3 = col2.selectbox("Prejudiciais R3:", range(0, 7), key="prejudiciais_3")
merito_3 = col3.selectbox("Tópicos Mérito R3:", range(1, 36), key="merito_3")

# Botão para adicionar os dados do processo
if st.button("Adicionar Processo"):
    if numero_processo:
        total_topicos = (
            preliminares_1 + prejudiciais_1 + merito_1 +
            preliminares_2 + prejudiciais_2 + merito_2 +
            preliminares_3 + prejudiciais_3 + merito_3
        )
        st.session_state["processos"].append({
            "Número do Processo": numero_processo,
            "Recurso 1": tipo_recurso_1 if tipo_recurso_1 != "Nenhum" else "",
            "Tópicos R1": preliminares_1 + prejudiciais_1 + merito_1,
            "Recurso 2": tipo_recurso_2 if tipo_recurso_2 != "Nenhum" else "",
            "Tópicos R2": preliminares_2 + prejudiciais_2 + merito_2,
            "Recurso 3": tipo_recurso_3 if tipo_recurso_3 != "Nenhum" else "",
            "Tópicos R3": preliminares_3 + prejudiciais_3 + merito_3,
            "Total de Tópicos": total_topicos
        })
        st.success(f"Processo {numero_processo} adicionado com sucesso!")
        reset_campos()
    else:
        st.error("Por favor, insira o número do processo.")

# Exibir processos adicionados
if st.session_state["processos"]:
    st.subheader("Processos Adicionados")
    df = pd.DataFrame(st.session_state["processos"])
    st.dataframe(df)
