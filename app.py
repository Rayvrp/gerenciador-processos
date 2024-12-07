import streamlit as st
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment

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
            "Classe 1": st.session_state.tipo_recurso_1 if st.session_state.tipo_recurso_1 != "Nenhum" else "",
            "Tópicos Recurso 1": st.session_state.preliminares_1 + st.session_state.prejudiciais_1 + st.session_state.merito_1,
            "Classe 2": st.session_state.tipo_recurso_2 if st.session_state.tipo_recurso_2 != "Nenhum" else "",
            "Tópicos Recurso 2": st.session_state.preliminares_2 + st.session_state.prejudiciais_2 + st.session_state.merito_2,
            "Classe 3": st.session_state.tipo_recurso_3 if st.session_state.tipo_recurso_3 != "Nenhum" else "",
            "Tópicos Recurso 3": st.session_state.preliminares_3 + st.session_state.prejudiciais_3 + st.session_state.merito_3,
            "Total de Tópicos do Processo": total_topicos
        })
        st.success(f"Processo {st.session_state.numero_processo} adicionado com sucesso!")
        reset_campos()
    else:
        st.error("Por favor, insira o número do processo.")

# Função para desfazer inclusão
def desfazer_inclusao():
    if st.session_state["processos"]:
        st.session_state["processos"].pop()
        st.success("Último processo removido com sucesso!")

# Função para ajustar largura das colunas no Excel
def ajustar_largura_colunas(worksheet):
    for column_cells in worksheet.columns:
        max_length = 0
        col_letter = column_cells[0].column_letter  # Get the column name
        for cell in column_cells:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except Exception:
                pass
        worksheet.column_dimensions[col_letter].width = max_length + 2

# Função para gerar relatório
def gerar_relatorio():
    # Criar DataFrame com os processos
    df_processos = pd.DataFrame(st.session_state["processos"])

    # Certificar que "Total de Tópicos do Processo" está correto
    if "Total de Tópicos do Processo" not in df_processos.columns:
        st.error("Erro: A coluna 'Total de Tópicos do Processo' está ausente nos dados.")
        return

    # Distribuição entre votistas
    num_votistas = st.session_state["num_votistas"]
    votistas = {f"Votista {i+1}": [] for i in range(num_votistas)}
    processos_ordenados = sorted(st.session_state["processos"], key=lambda x: x["Total de Tópicos do Processo"], reverse=True)

    for processo in processos_ordenados:
        votista = min(votistas, key=lambda v: sum(p["Total de Tópicos do Processo"] for p in votistas[v]))
        votistas[votista].append(processo)

    output = BytesIO()

    # Criar workbook
    wb = Workbook()
    ws_processos = wb.active
    ws_processos.title = "Processos"

    # Renomear colunas do DataFrame
    df_processos.rename(columns={
        "Número do Processo": "Número do Processo",
        "Classe 1": "Classe",
        "Tópicos Recurso 1": "Tópicos Recurso 1",
        "Classe 2": "Classe",
        "Tópicos Recurso 2": "Tópicos Recurso 2",
        "Classe 3": "Classe",
        "Tópicos Recurso 3": "Tópicos Recurso 3",
        "Total de Tópicos do Processo": "Total de Tópicos do Processo"
    }, inplace=True)

    # Escrever processos no Excel
    for row in dataframe_to_rows(df_processos, index=False, header=True):
        ws_processos.append(row)

    # Ajustar largura das colunas
    ajustar_largura_colunas(ws_processos)

    # Criar aba para distribuição dos votistas
    ws_votistas = wb.create_sheet(title="Distribuição por Votista")
    ws_votistas.append(["Votista", "Número do Processo", "Total de Tópicos"])
    for votista, processos in votistas.items():
        for processo in processos:
            ws_votistas.append([votista, processo["Número do Processo"], processo["Total de Tópicos do Processo"]])

    ajustar_largura_colunas(ws_votistas)

    # Salvar o Excel
    wb.save(output)
    output.seek(0)

    # Botão para download do relatório
    st.download_button(
        label="Baixar Relatório",
        data=output,
        file_name="relatorio_processos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

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

# Botão para desfazer inclusão
if st.session_state["processos"]:
    st.button("Desfazer Inclusão", on_click=desfazer_inclusao)

# Exibir processos adicionados
if st.session_state["processos"]:
    st.subheader("Processos Adicionados")
    df = pd.DataFrame(st.session_state["processos"])
    st.dataframe(df)

# Número de votistas e botão de geração de relatório
if st.session_state["processos"]:
    st.number_input("Número de Votistas:", min_value=1, step=1, key="num_votistas")
    st.button("Gerar Relatório", on_click=gerar_relatorio)

