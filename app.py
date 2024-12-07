import streamlit as st
import pandas as pd
from io import BytesIO

# Inicializando os dados
if "processos" not in st.session_state:
    st.session_state["processos"] = []

# Função para resetar os campos do formulário
def reset_campos():
    st.session_state.numero_processo = ""
    st.session_state.tipo_recurso_1 = "Nenhum"
    st.session_state.tipo_recurso_2 = "Nenhum"
    st.session_state.tipo_recurso_3 = "Nenhum"
    st.session_state.preliminares_1 = 0
    st.session_state.preliminares_2 = 0
    st.session_state.preliminares_3 = 0
    st.session_state.prejudiciais_1 = 0
    st.session_state.prejudiciais_2 = 0
    st.session_state.prejudiciais_3 = 0
    st.session_state.merito_1 = 0
    st.session_state.merito_2 = 0
    st.session_state.merito_3 = 0

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
merito_1 = col3.selectbox("Tópicos Mérito R1:", range(0, 36), key="merito_1")

preliminares_2 = col1.selectbox("Preliminares R2:", range(0, 7), key="preliminares_2")
prejudiciais_2 = col2.selectbox("Prejudiciais R2:", range(0, 7), key="prejudiciais_2")
merito_2 = col3.selectbox("Tópicos Mérito R2:", range(0, 36), key="merito_2")

preliminares_3 = col1.selectbox("Preliminares R3:", range(0, 7), key="preliminares_3")
prejudiciais_3 = col2.selectbox("Prejudiciais R3:", range(0, 7), key="prejudiciais_3")
merito_3 = col3.selectbox("Tópicos Mérito R3:", range(0, 36), key="merito_3")

# Função para adicionar processo
def adicionar_processo():
    if st.session_state.numero_processo:
        total_topicos = (
            st.session_state.preliminares_1 + st.session_state.prejudiciais_1 + st.session_state.merito_1 +
            st.session_state.preliminares_2 + st.session_state.prejudiciais_2 + st.session_state.merito_2 +
            st.session_state.preliminares_3 + st.session_state.prejudiciais_3 + st.session_state.merito_3
        )
        st.session_state["processos"].append({
            "Número do Processo": st.session_state.numero_processo,
            "Recurso 1": st.session_state.tipo_recurso_1 if st.session_state.tipo_recurso_1 != "Nenhum" else "",
            "Tópicos R1": st.session_state.preliminares_1 + st.session_state.prejudiciais_1 + st.session_state.merito_1,
            "Recurso 2": st.session_state.tipo_recurso_2 if st.session_state.tipo_recurso_2 != "Nenhum" else "",
            "Tópicos R2": st.session_state.preliminares_2 + st.session_state.prejudiciais_2 + st.session_state.merito_2,
            "Recurso 3": st.session_state.tipo_recurso_3 if st.session_state.tipo_recurso_3 != "Nenhum" else "",
            "Tópicos R3": st.session_state.preliminares_3 + st.session_state.prejudiciais_3 + st.session_state.merito_3,
            "Total de Tópicos": total_topicos
        })
        st.success(f"Processo {st.session_state.numero_processo} adicionado com sucesso!")
        reset_campos()
    else:
        st.error("Por favor, insira o número do processo.")

# Botão para adicionar os dados do processo
st.button("Adicionar Processo", on_click=adicionar_processo)

# Exibir processos adicionados
if st.session_state["processos"]:
    st.subheader("Processos Adicionados")
    df = pd.DataFrame(st.session_state["processos"])
    st.dataframe(df)

    # Número de votistas
    num_votistas = st.number_input("Número de Votistas:", min_value=1, step=1, key="num_votistas")

    # Botão para gerar relatório
    def gerar_relatorio():
        # Ordenar processos por tópicos
        processos_ordenados = sorted(st.session_state["processos"], key=lambda x: x["Total de Tópicos"], reverse=True)
        votistas = {f"Votista {i+1}": [] for i in range(num_votistas)}

        # Distribuição equitativa
        for processo in processos_ordenados:
            votista = min(votistas, key=lambda v: sum(p["Total de Tópicos"] for p in votistas[v]))
            votistas[votista].append(processo)

        # Gerar relatório em Excel
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine="openpyxl")
        pd.DataFrame(st.session_state["processos"]).to_excel(writer, index=False, sheet_name="Processos")
        for votista, processos_votista in votistas.items():
            pd.DataFrame(processos_votista).to_excel(writer, index=False, sheet_name=votista)
        writer.close()
        output.seek(0)

        # Botão para download do relatório
        st.download_button(
            label="Baixar Relatório",
            data=output,
            file_name="relatorio_processos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.success("Relatório gerado com sucesso!")

    st.button("Gerar Relatório", on_click=gerar_relatorio)


