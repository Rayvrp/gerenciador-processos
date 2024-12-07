import streamlit as st
import pandas as pd

# Inicializando os dados
if "processos" not in st.session_state:
    st.session_state["processos"] = []

# Função para resetar os campos do formulário
def reset_campos():
    st.session_state["numero_processo"] = ""
  

# Exibir processos adicionados
if st.session_state["processos"]:
    st.subheader("Processos Adicionados")
    df = pd.DataFrame(st.session_state["processos"])
    st.dataframe(df)
