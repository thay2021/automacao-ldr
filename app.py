import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Extração LDR")

st.title("Extração LDR")

uploaded_file = st.file_uploader("📁 Envie seu arquivo", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

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

    st.subheader("Prévia do arquivo limpo")
    st.dataframe(df_limpo.head())

    # Deixar links clicáveis no Excel
    link_cols = ["Site", "Perfil linkedin contato", "Perfil likedin empresa", "Facebook"]
    for col in link_cols:
        if col in df_limpo.columns:
            df_limpo[col] = df_limpo[col].apply(
                lambda x: f'=HYPERLINK("{x}", "{x}")' if pd.notnull(x) and str(x).startswith("http") else x
            )

    buffer = io.BytesIO()
    df_limpo.to_excel(buffer, index=False)
    buffer.seek(0)

    # Botão de download
    st.download_button(
        "⬇️ Baixar arquivo",
        buffer,
        "leads_limpos.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
