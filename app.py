# Sistema de Requisição e Controle de EPIs
# Desenvolvido em Streamlit com persistência em CSV

import streamlit as st
import pandas as pd
import os
from datetime import datetime

def initialize_csv_files():
    if not os.path.exists('colaboradores.csv'):
        pd.DataFrame({
            'Nome': [
                'Alessandra da Silva Mendes',
                'Carla Aparecida De Almeida',
                'Pedro de Queiroz',
                'Rafaela Evangelista do Prado',
                'Alexander Gomes de Almeida'
            ],
            'Setor': ['MONTAGEM'] * 5
        }).to_csv('colaboradores.csv', index=False)

    if not os.path.exists('gestores.csv'):
        pd.DataFrame({
            'Nome': ['Igor Henrique Ferreira'],
            'Setor': ['MONTAGEM']
        }).to_csv('gestores.csv', index=False)

    if not os.path.exists('epis.csv'):
        pd.DataFrame({
            'Nome': [
                'MASCARA T-851 PFF3 (V)',
                'OCULOS DE SEGURANCA',
                'PROTETOR AUDITIVO DE SILICONE - TIPO PLUG'
            ],
            'Modelo': ['TAYCO', 'KALIPSO', 'PREVENT'],
            'Estoque': [100, 100, 100]
        }).to_csv('epis.csv', index=False)

    if not os.path.exists('solicitacoes.csv'):
        pd.DataFrame(columns=['ID', 'Data_Solicitacao', 'Colaborador', 'Gestor', 'EPI', 'Quantidade', 'Status'])          .to_csv('solicitacoes.csv', index=False)

    if not os.path.exists('entregas.csv'):
        pd.DataFrame(columns=['ID', 'Data_Solicitacao', 'Data_Entrega', 'Colaborador', 'EPI', 'Quantidade', 'Entregue_Por'])          .to_csv('entregas.csv', index=False)

def load_data():
    return (
        pd.read_csv('colaboradores.csv'),
        pd.read_csv('epis.csv'),
        pd.read_csv('solicitacoes.csv'),
        pd.read_csv('entregas.csv')
    )

def save_data(df, filename):
    df.to_csv(filename, index=False)

def login_screen():
    st.sidebar.title("Login / Selecao de Papel")
    role = st.sidebar.selectbox("Selecione seu papel:", ["Gestor", "Almoxarifado", "Administrador"])
    if role == "Administrador":
        password = st.sidebar.text_input("Senha:", type="password")
        if password != "1234":
            st.sidebar.error("Senha incorreta.")
            return None
    return role

def page_solicitacao():
    st.header("Solicitacao de EPIs")
    df_colab, df_epi, df_solicit, _ = load_data()
    with st.form("form_solicitacao"):
        colaborador = st.selectbox("Colaborador:", df_colab['Nome'])
        epi = st.selectbox("EPI:", df_epi['Nome'])
        quantidade = st.number_input("Quantidade:", min_value=1, step=1)
        gestor = st.selectbox("Gestor:", pd.read_csv('gestores.csv')['Nome'])
        submitted = st.form_submit_button("Enviar Solicitação")
        if submitted:
            novo = pd.DataFrame([{
                "ID": len(df_solicit) + 1,
                "Data_Solicitacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Colaborador": colaborador,
                "Gestor": gestor,
                "EPI": epi,
                "Quantidade": quantidade,
                "Status": "Pendente"
            }])
            df_solicit = pd.concat([df_solicit, novo], ignore_index=True)
            save_data(df_solicit, 'solicitacoes.csv')
            st.success("Solicitação registrada com sucesso!")

def page_almoxarifado():
    st.header("Painel do Almoxarifado")
    df_colab, df_epi, df_solicit, df_entrega = load_data()
    df_pendente = df_solicit[df_solicit["Status"] == "Pendente"]
    if df_pendente.empty:
        st.info("Nao ha solicitacoes pendentes.")
    else:
        for index, row in df_pendente.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"ID {row['ID']} | {row['Colaborador']} - {row['EPI']} ({row['Quantidade']})")
            with col2:
                if st.button(f"Confirmar {row['ID']}"):
                    df_solicit.loc[df_solicit['ID'] == row['ID'], 'Status'] = 'Entregue'
                    df_epi.loc[df_epi['Nome'] == row['EPI'], 'Estoque'] = df_epi.loc[df_epi['Nome'] == row['EPI']].astype({'Estoque': int})['Estoque'] - int(row['Quantidade'])
                    entrega = pd.DataFrame([{
                        "ID": row['ID'],
                        "Data_Solicitacao": row['Data_Solicitacao'],
                        "Data_Entrega": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Colaborador": row['Colaborador'],
                        "EPI": row['EPI'],
                        "Quantidade": row['Quantidade'],
                        "Entregue_Por": "Almoxarifado"
                    }])
                    df_entrega = pd.concat([df_entrega, entrega], ignore_index=True)
                    save_data(df_solicit, 'solicitacoes.csv')
                    save_data(df_epi, 'epis.csv')
                    save_data(df_entrega, 'entregas.csv')
                    st.success(f"Entrega do ID {row['ID']} confirmada.")

def page_administrador():
    st.header("Painel Administrativo")
    df_colab, df_epi, df_solicit, df_entrega = load_data()
    st.subheader("Solicitacoes Registradas")
    st.dataframe(df_solicit)
    st.subheader("Entregas Confirmadas")
    st.dataframe(df_entrega)
    st.subheader("Estoque Atual")
    st.dataframe(df_epi)
    with st.expander("Exportar Arquivos CSV"):
        st.download_button("Download Solicitações", df_solicit.to_csv(index=False), "solicitacoes.csv")
        st.download_button("Download Entregas", df_entrega.to_csv(index=False), "entregas.csv")
        st.download_button("Download Estoque", df_epi.to_csv(index=False), "estoque.csv")

def main():
    initialize_csv_files()
    st.title("Sistema de Controle de EPIs")
    role = login_screen()
    if role is None:
        st.stop()
    if role == "Gestor":
        page_solicitacao()
    elif role == "Almoxarifado":
        page_almoxarifado()
    elif role == "Administrador":
        page_administrador()

if __name__ == '__main__':
    main()
