import streamlit as st
import sqlite3
import pandas as pd
import base64

def create_table():
    # Conecta ao banco de dados
    conn = sqlite3.connect('dados_formulario.db')
    cursor = conn.cursor()

    # Cria a tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS formulario (
            id INTEGER PRIMARY KEY,
            numero_processo TEXT,
            data_na_cgsie DATE,
            data_ultima_modificacao DATE,
            data_finalizacao_do_processo DATE,
            data_retificacao DATE,
            data_atualizacao DATE,
            data_lancamento DATE,
            atribuicao TEXT,
            tipo TEXT,
            interesados TEXT,
            status1 TEXT,
            descricao_do_processo TEXT,
            obsservacao TEXT
        )
    ''')

    # Commita as mudanças e fecha a conexão
    conn.commit()
    conn.close()

def main():

    # Menu lateral
    menu_option = st.sidebar.selectbox("Menu", ["Cadastrar Processo", "Consultar Dados por Número de Processo", "Baixar Dados como CSV"])
        

    if menu_option == "Cadastrar Processo":
        st.markdown(f'<h1 style="text-align: center; width: 100%;">Cadastrar Processo SEI</h1>', unsafe_allow_html=True)
        # Dados do Formulário
        numero_processo = st.text_input("Número do Processo")
        data_na_cgsie = st.date_input("Data na CGSIE")
        data_ultima_modificacao = st.date_input("Data da Última Modificação")
        data_finalizacao_do_processo = st.date_input("Data de Finalização do Processo")
        data_retificacao = st.date_input("Data de Retificação")
        data_atualizacao = st.date_input("Data de Atualização")
        data_lancamento = st.date_input("Data de Lançamento")
        atribuicao = st.text_input("Atribuição")
        tipo = st.text_input("Tipo")
        interesados = st.text_input("Interessados")
        status1 = st.text_input("Status")
        descricao_do_processo = st.text_area("Descrição do Processo")
        obsservacao = st.text_area("Observação")

        if st.button("Enviar"):
            # Conecta ao banco de dados
            conn = sqlite3.connect('dados_formulario.db')
            cursor = conn.cursor()

            # Insere os dados do formulário na tabela
            cursor.execute('''
                INSERT INTO formulario (
                    numero_processo, data_na_cgsie, data_ultima_modificacao,
                    data_finalizacao_do_processo, data_retificacao, data_atualizacao,
                    data_lancamento, atribuicao, tipo, interesados, status1,
                    descricao_do_processo, obsservacao
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                numero_processo, data_na_cgsie, data_ultima_modificacao,
                data_finalizacao_do_processo, data_retificacao, data_atualizacao,
                data_lancamento, atribuicao, tipo, interesados, status1,
                descricao_do_processo, obsservacao
            ))

            # Commita as mudanças no banco de dados
            conn.commit()

            # Fecha a conexão
            conn.close()

            st.success("Dados enviados com sucesso!")

    elif menu_option == "Consultar Dados por Número de Processo":
        st.header("Consulta de Dados por Número de Processo")

        # Número do processo para consulta
        numero_processo_consulta = st.text_input("Digite o número do processo:")

        if st.button("Consultar"):
            # Conecta ao banco de dados
            conn = sqlite3.connect('dados_formulario.db')

            # Query para selecionar os dados do processo especificado
            query = f"SELECT * FROM formulario WHERE numero_processo = '{numero_processo_consulta}'"

            # Executa a query e obtém os dados
            df = pd.read_sql(query, conn)

            # Fecha a conexão
            conn.close()

            # Verifica se há resultados da consulta
            if df.empty:
                st.warning("Nenhum registro encontrado para o número de processo especificado.")
            else:
                # Exibe os dados com título e descrição
                for index, row in df.iterrows():
                    st.subheader(f"Número do Processo: {row['numero_processo']}")
                    st.write(f"**Atribuição:** {row['atribuicao']}")
                    st.write(f"**Tipo:** {row['tipo']}")
                    st.write(f"**Interessados:** {row['interesados']}")
                    st.write(f"**Status:** {row['status1']}")
                    st.write(f"**Descrição do Processo:** {row['descricao_do_processo']}")
                    st.write(f"**Observação:** {row['obsservacao']}")
                    st.markdown("---")

    elif menu_option == "Baixar Dados como CSV":
        st.title("Baixar Dados como CSV")

        # Conecta ao banco de dados
        conn = sqlite3.connect('dados_formulario.db')

        # Query para selecionar todos os dados da tabela
        query = "SELECT * FROM formulario"

        # Executa a query e obtém os dados
        df = pd.read_sql(query, conn)

        # Formatar as datas antes de salvar como CSV
        df['data_na_cgsie'] = pd.to_datetime(df['data_na_cgsie']).dt.strftime('%d/%m/%Y')
        df['data_ultima_modificacao'] = pd.to_datetime(df['data_ultima_modificacao']).dt.strftime('%d/%m/%Y')
        df['data_finalizacao_do_processo'] = pd.to_datetime(df['data_finalizacao_do_processo']).dt.strftime('%d/%m/%Y')
        df['data_retificacao'] = pd.to_datetime(df['data_retificacao']).dt.strftime('%d/%m/%Y')
        df['data_atualizacao'] = pd.to_datetime(df['data_atualizacao']).dt.strftime('%d/%m/%Y')
        df['data_lancamento'] = pd.to_datetime(df['data_lancamento']).dt.strftime('%d/%m/%Y')

        # Fecha a conexão
        conn.close()

        # Botão para baixar os dados como arquivo CSV
        if st.button("Baixar Dados como CSV"):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="dados_formulario.csv">Baixar CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    create_table()
    main()
