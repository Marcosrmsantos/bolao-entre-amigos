import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração inicial
st.set_page_config(page_title="Bolão entre Amigos", page_icon="🏆")
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🎟️ Bolão entre Amigos")

# 2. Criação das abas
aba1, aba2, aba3 = st.tabs(["📌 Registrar", "📊 Ranking", "📲 Convite"])

with aba1:
    st.header("Cadastrar Palpite")
    nome = st.text_input("Seu Nome")
    palpite = st.text_input("Sua Centena (000-999)", max_chars=3)

    if st.button("Confirmar Palpite"):
        if len(palpite) == 3 and palpite.isdigit():
            try:
                # Lê a aba que você renomeou para 'Dados'
                df_atual = conn.read(worksheet="Dados")
                
                novo_dado = pd.DataFrame([{"Nomes": nome, "Palpite": palpite}])
                df_final = pd.concat([df_atual, novo_dado], ignore_index=True)
                
                # Salva na planilha
                conn.update(worksheet="Dados", data=df_final)
                
                st.success(f"Sorte lançada, {nome}!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.error("Insira exatamente 3 números!")

with aba2:
    st.header("🏆 Ranking")
    try:
        df = conn.read(worksheet="Dados")
        st.table(df)
    except:
        st.info("Ainda não temos palpites.")

with aba3:
    st.header("📨 Enviar Convite")
    st.code("Participe do nosso Bolão! Acesse: https://bolao-entre-amigos.streamlit.app")
