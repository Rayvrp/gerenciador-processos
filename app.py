def gerar_relatorio():
    # Certificar que todos os processos têm a coluna "Total de Tópicos do Processo"
    for processo in st.session_state["processos"]:
        processo["Total de Tópicos"] = (
            processo.get("Tópicos Recurso 1", 0) +
            processo.get("Tópicos Recurso 2", 0) +
            processo.get("Tópicos Recurso 3", 0)
        )

    df_processos = pd.DataFrame(st.session_state["processos"])

    # Obter os votistas marcados
    votistas_selecionados = [v for v in VOTISTAS if st.session_state.get(f"votista_{v}", False)]
    if not votistas_selecionados:
        st.error("Por favor, selecione ao menos um votista.")
        return

    # Distribuição entre votistas
    votistas = {v: [] for v in votistas_selecionados}
    processos_ordenados = sorted(st.session_state["processos"], key=lambda x: x["Total de Tópicos"], reverse=True)

    for processo in processos_ordenados:
        votista = min(votistas, key=lambda v: sum(p["Total de Tópicos"] for p in votistas[v]))
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
        "Total de Tópicos": "Total de Tópicos"
    }, inplace=True)

    # Escrever processos no Excel
    for row in dataframe_to_rows(df_processos, index=False, header=True):
        ws_processos.append(row)

    # Ajustar largura das colunas
    ajustar_largura_colunas(ws_processos)

    # Criar abas para cada votista
    for votista, processos in votistas.items():
        ws_votista = wb.create_sheet(title=votista)
        ws_votista.append(["Número do Processo", "Classe 1", "Tópicos Recurso 1",
                           "Classe 2", "Tópicos Recurso 2", "Classe 3", "Tópicos Recurso 3", "Total de Tópicos"])

        total_processos = len(processos)
        total_topicos = sum(p["Total de Tópicos"] for p in processos)

        # Adicionar processos do votista
        for processo in processos:
            ws_votista.append([
                processo["Número do Processo"],
                processo["Classe 1"], processo["Tópicos Recurso 1"],
                processo["Classe 2"], processo["Tópicos Recurso 2"],
                processo["Classe 3"], processo["Tópicos Recurso 3"],
                processo["Total de Tópicos"]
            ])

        # Adicionar totais ao final
        ws_votista.append([])
        ws_votista.append(["TOTAL", "", "", "", "", "", "", total_topicos])
        ws_votista.append(["Total de Processos", "", "", "", "", "", "", total_processos])

        ajustar_largura_colunas(ws_votista)

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
