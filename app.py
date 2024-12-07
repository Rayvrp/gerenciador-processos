import streamlit as st
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment

# Inicializando os dados
if "processos" not in st.session_state:
    st.session_state["processos"] = []
if "relatorio_gerado" not in st.session_state:
    st.session_state["relatorio_gerado"] = None

# Lista de votistas
VOTISTAS = ["Ana", "André", "Fernanda", "Luiz", "Mariana", "Mônica", "Raquel", "Rayssa", "Renata", "Novo"]

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

# Função para calcular a soma de tópicos
def calcular_total_topicos():
    return (
        st.session_state.preliminares_1 + st.session_state.prejudiciais_1 + st.session_state.merito_1 +
        st.session_state.preliminares_2 + st.session_state.prejudiciais_2 + st.session_state.merito_2 +
        st.session_state.preliminares_3 + st.session_state.prejudiciais_3 + st.session_state.merito_3
    )

# Função para adicionar processo
def adicionar_processo():
    if st.session_state.numero_processo:
        total_topicos = calcular_total_topicos()
        st.session_state["processos"].append({
            "Número do Processo": st.session_state.numero_processo,
            "Classe 1": st.session_state.tipo_recurso_1 if st.session_state.tipo_recurso_1 != "Nenhum" else "",
            "Tópicos Recurso 1": st.session_state.preliminares_1 + st.session_state.prejudiciais_1 + st.session_state.merito_1,
            "Classe 2": st.session_state.tipo_recurso_2 if st.session_state.tipo_recurso_2 != "Nenhum" else "",
            "Tópicos Recurso 2": st.session_state.preliminares_2 + st.session_state.prejudiciais_2 + st.session_state.merito_2,
            "Classe 3": st.session_state.tipo_recurso_3 if st.session_state.tipo_recurso_3 != "Nenhum" else "",
            "Tópicos Recurso 3": st.session_state.preliminares_3 + st.session_state.prejudiciais_3 + st.session_state.merito_3,
            "Total de Tópicos": total_topicos
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
    df_processos = pd.DataFrame(st.session_state["processos"])

    # Obter os votistas marcados
    votistas_selecionados = [v for v in VOTISTAS if st.session_state.get(f"votista_{v}", False)]
    if not votistas_selecionados:
        st.error("Por favor, selecione ao menos um votista.")
        return

    # Distribuição entre votistas
    votistas = {v: [] for v in votistas_selecionados}
    processos_ordenados = sorted(st.session_state["processos"], key=lambda x: x.get("Total de Tópicos", 0), reverse=True)

    for processo in processos_ordenados:
        votista = min(votistas, key=lambda v: sum(p.get("Total de Tópicos", 0) for p in votistas[v]))
        votistas[votista].append(processo)

    output = BytesIO()

    # Criar workbook
    wb = Workbook()
    ws_processos = wb.active
    ws_processos.title = "Todos os Processos"

    # Preencher a aba principal com todos os processos e novos títulos
    ws_processos.append(["Número do Processo", "Recurso 1", "Tópicos R1", "Recurso 2", "Tópicos R2", "Recurso 3", "Tópicos R3", "Total de Tópicos"])
    for processo in st.session_state["processos"]:
        ws_processos.append([
            processo.get("Número do Processo", ""),
            processo.get("Classe 1", ""), processo.get("Tópicos Recurso 1", 0),
            processo.get("Classe 2", ""), processo.get("Tópicos Recurso 2", 0),
            processo.get("Classe 3", ""), processo.get("Tópicos Recurso 3", 0),
            processo.get("Total de Tópicos", 0)
        ])
    ajustar_largura_colunas(ws_processos)

    # Criar aba para cada votista
    for votista, processos in votistas.items():
        ws = wb.create_sheet(title=votista)
        ws.append(["Número do Processo", "Classe 1", "Tópicos Recurso 1", "Classe 2", "Tópicos Recurso 2", "Classe 3", "Tópicos Recurso 3", "Total de Tópicos"])
        for processo in processos:
            ws.append([
                processo.get("Número do Processo", ""),
                processo.get("Classe 1", ""), processo.get("Tópicos Recurso 1", 0),
                processo.get("Classe 2", ""), processo.get("Tópicos Recurso 2", 0),
                processo.get("Classe 3", ""), processo.get("Tópicos Recurso 3", 0),
                processo.get("Total de Tópicos", 0)
            ])
        total_processos = len(processos)
        total_topicos = sum(p.get("Total de Tópicos", 0) for p in processos)
        ws.append([])
        ws.append(["Total de Processos", total_processos])
        ws.append(["Total de Tópicos", total_topicos])
        ajustar_largura_colunas(ws)

    # Salvar o Excel no estado da aplicação
    wb.save(output)
    output.seek(0)
    st.session_state["relatorio_gerado"] = output

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
st.button("Adicionar Processo", on_click=adicionar_processo, key="add_button")

# Botão para desfazer inclusão
if st.session_state["processos"]:
    st.button("Desfazer Inclusão", on_click=desfazer_inclusao, key="undo_button")

# Exibir processos adicionados
if st.session_state["processos"]:
    st.subheader("Processos Adicionados")
    df = pd.DataFrame(st.session_state["processos"])
    st.dataframe(df)

# Seleção dos votistas
st.subheader("Selecione os Votistas")
for votista in VOTISTAS:
    st.checkbox(votista, key=f"votista_{votista}")

# Botão de geração do relatório
if st.session_state["processos"]:
    if st.button("Gerar Relatório", key="generate_button"):
        gerar_relatorio()

# Botão de download do relatório
if st.session_state.get("relatorio_gerado"):
    st.download_button(
        label="Baixar Relatório",
        data=st.session_state["relatorio_gerado"],
        file_name="relatorio_processos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_button"
    )


