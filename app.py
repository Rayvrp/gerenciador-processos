import streamlit as st
import pandas as pd
from io import BytesIO

# Inicializando os dados
if "processos" not in st.session_state:
    st.session_state["processos"] = []

# Formulário para adicionar processos
st.title("Gerenciador de Processos e Recursos")

# Entrada do número do processo
numero_processo = st.text_input("Número do Processo:")

# Seleção do tipo de recurso
tipo_recurso = st.selectbox("Tipo de Recurso:", ["Recurso Ordinário", "Agravo de Instrumento", "Agravo de Petição"])

# Quantidade de preliminares, prejudiciais e mérito
col1, col2, col3 = st.columns(3)
preliminares = col1.selectbox("Preliminares:", range(0, 7))
prejudiciais = col2.selectbox("Prejudiciais:", range(0, 7))
merito = col3.selectbox("Tópicos de Mérito:", range(1, 36))

# Botão para adicionar os dados
if st.button("Adicionar Processo"):
    if numero_processo:
        st.session_state["processos"].append({
            "Número do Processo": numero_processo,
            "Tipo de Recurso": tipo_recurso,
            "Preliminares": preliminares,
            "Prejudiciais": prejudiciais,
            "Mérito": merito,
            "Total de Tópicos": preliminares + prejudiciais + merito
        })
        st.success(f"Processo {numero_processo} adicionado com sucesso!")
    else:
        st.error("Por favor, insira o número do processo.")

# Exibir processos adicionados
if st.session_state["processos"]:
    st.write("### Processos Adicionados:")
    df = pd.DataFrame(st.session_state["processos"])
    st.dataframe(df)

    # Informar número de votistas
    num_votistas = st.number_input("Número de Votistas:", min_value=1, value=1)

    # Botão para gerar o relatório
    if st.button("Gerar Relatório"):
        # Distribuir processos por votistas
        processos = st.session_state["processos"]
        df = pd.DataFrame(processos)
        votistas = {f"Votista {i+1}": [] for i in range(num_votistas)}

        # Algoritmo para distribuição equilibrada
        for i, processo in enumerate(processos):
            votista = f"Votista {(i % num_votistas) + 1}"
            votistas[votista].append(processo)

        # Criar planilha de Excel
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine="openpyxl")
        df.to_excel(writer, index=False, sheet_name="Processos")
        distrib_df = pd.DataFrame([
            {"Votista": votista, "Total de Tópicos": sum(p["Total de Tópicos"] for p in processos)}
            for votista, processos in votistas.items()
        ])
        distrib_df.to_excel(writer, index=False, sheet_name="Distribuição")
        writer.save()
        output.seek(0)

        # Permitir download do relatório
        st.download_button(
            label="Baixar Relatório",
            data=output,
            file_name=f"relatorio_{pd.Timestamp.now().strftime('%Y-%m-%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success(f"Relatório gerado com {len(processos)} processos e {num_votistas} votistas.")
