import streamlit as st
import pandas as pd
import io
import re
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Extração LDR")

st.title("Extração LDR")

uploaded_file = st.file_uploader("📁 Envie seu arquivo", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Prévia dos dados recebidos")
    st.dataframe(df.head())

    # Criar coluna Nome e sobrenome
    df["Nome e sobrenome"] = df["First Name"].astype(str) + " " + df["Last Name"].astype(str)

    # Lista de colunas para manter
    colunas_para_manter = [
        "Nome e sobrenome",
        "Title",
        "Company Name",
        "Email",
        "Website",
        "Company Phone",
        "City",
        "State",
        "Country",
        "Industry",
        "# Employees",
        "Person Linkedin Url",
        "Company Linkedin Url",
        "Facebook Url",
        "Company Address"
    ]

    # Filtrar apenas colunas desejadas
    df_limpo = df[colunas_para_manter]

    df_limpo = df_limpo.rename(columns={
        "Nome e sobrenome": "Nome e sobrenome",
        "Title": "Cargo",
        "Company Name": "Nome da empresa",
        "Email": "Email",
        "Website": "Site",
        "Company Phone": "Telefone apollo",
        "City": "Cidade do contato",
        "State": "Estado do contato",
        "Country": "Pais do contato",
        "Industry": "Segmento",
        "# Employees": "Funcionarios",
        "Person Linkedin Url": "Perfil linkedin contato",
        "Company Linkedin Url": "Perfil likedin empresa",
        "Facebook Url": "Facebook",
        "Company Address": "Endereço"
    })

    # Remover http:// ou https:// do início dos valores na coluna "Site" e garantir que iniciem com www
    df_limpo["Site"] = df_limpo["Site"].apply(
        lambda x: "www." + re.sub(r"(http://|https://|www\.)", "", x) if pd.notnull(x) else x
    )

    # Lista de colunas que contêm links
    colunas_com_links = ["Perfil linkedin contato", "Perfil likedin empresa", "Facebook"]

    # Remover http:// ou https:// do início dos valores e garantir que iniciem com www
    for coluna in colunas_com_links:
        if coluna in df_limpo.columns:
            df_limpo[coluna] = df_limpo[coluna].apply(
                lambda x: "www." + x.split("www.")[-1] if pd.notnull(x) and ("http://" in x or "https://" in x or "www." in x) else x
            )

    # Função para limpar e formatar números de telefone
    def limpar_e_formatar_telefone(numero):
        if pd.notnull(numero):
            # Remove aspas simples ou duplas e espaços extras
            numero = str(numero).strip().replace("'", "").replace('"', "")
            if numero.startswith("+55"):
                # Remove o prefixo +55 e caracteres não numéricos
                numero = re.sub(r"[^\d]", "", numero[3:])
                # Formata no padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
                if len(numero) == 11:  # Celular com DDD
                    return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
                elif len(numero) == 10:  # Fixo com DDD
                    return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
        # Retorna o número original se não for válido para formatação
        return numero if pd.notnull(numero) else ""

    # Aplicar a limpeza e formatação na coluna "Telefone apollo"
    df_limpo["Telefone apollo"] = df_limpo["Telefone apollo"].apply(limpar_e_formatar_telefone)

    # Remover pontos da coluna Funcionarios
    df_limpo["Funcionarios"] = df_limpo["Funcionarios"].apply(
        lambda x: str(x).replace(".", "") if pd.notnull(x) else x
    )

     # Traduzir automaticamente os valores das colunas
    df_limpo["Pais do contato"] = df_limpo["Pais do contato"].apply(
        lambda x: GoogleTranslator(source='auto', target='pt').translate(x) if pd.notnull(x) else x
    )
    df_limpo["Segmento"] = df_limpo["Segmento"].apply(
        lambda x: GoogleTranslator(source='auto', target='pt').translate(x) if pd.notnull(x) else x
    )
    df_limpo["Estado do contato"] = df_limpo["Estado do contato"].apply(
        lambda x: GoogleTranslator(source='auto', target='pt').translate(x) if pd.notnull(x) else x
    )

    st.subheader("Prévia do arquivo limpo")
    st.dataframe(df_limpo.head())

    buffer = io.BytesIO()
    df_limpo.to_csv(buffer, index=False, encoding="utf-8")
    buffer.seek(0)

    # Botão de download
    st.download_button(
        "⬇️ Baixar arquivo",
        buffer,
        "leads_limpos.csv",
        "text/csv"
    )
