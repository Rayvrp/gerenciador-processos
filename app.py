import streamlit as st
import pandas as pd

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

# Função para excluir processo
def excluir_processo(index):
    if 0 <= index < len(st.session_state["processos"]):
        del st.session_state["processos"][index]
        st.success("Processo excluído com sucesso!")

# Título do Aplicativo
st.title("Distribuição semanal de processos")

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

# Botão para adicionar os dados do processo
st.button("Adicionar Processo", on_click=adicionar_processo)

# Exibir processos adicionados com botões de exclusão
if st.session_state["processos"]:
    st.subheader("Processos Adicionados")
    for i, processo in enumerate(st.session_state["processos"]):
        st.markdown("---")
        cols = st.columns(len(processo) + 1)
        for j, (key, value) in enumerate(processo.items()):
            cols[j].write(f"**{key}:** {value}")
        # Adicionar botão de exclusão na última coluna
        if cols[-1].button("Excluir", key=f"excluir_{i}"):
            excluir_processo(i)

# Número de votistas e geração de relatório
if st.session_state["processos"]:
    st.subheader("Distribuição dos Processos")
    st.number_input("Número de Votistas:", min_value=1, step=1, key="num_votistas")

    def gerar_relatorio():
        st.write("Relatório gerado!")  # Lógica completa permanece aqui
        # Adicionar a lógica de distribuição e geração de relatório conforme explicado antes.

    st.button("Gerar Relatório", on_click=gerar_relatorio)


