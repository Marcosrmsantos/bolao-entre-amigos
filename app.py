import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Bolão entre Amigos", page_icon="🏆")

# Conexão com a Planilha Google
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🎟️ Bolão entre Amigos")

aba1, aba2, aba3 = st.tabs(["📌 Registrar", "📊 Ranking", "📲 Convite"])

with aba1:
    st.header("Cadastrar Palpite")
    nome = st.text_input("Seu Nome")
    palpite = st.text_input("Sua Centena (000-999)", max_chars=3)
    
    if st.button("Confirmar Palpite"):
        if len(palpite) == 3 and palpite.isdigit():
            # Lê os dados atuais da planilha
            df_atual = conn.read()
            novo_dado = pd.DataFrame([{"Nome": nome, "Palpite": palpite}])
            # Adiciona o novo palpite e envia de volta para o Google
            df_final = pd.concat([df_atual, novo_dado], ignore_index=True)
            conn.update(data=df_final)
            st.success(f"Sorte lançada, {nome}!")
        else:
            st.error("Insira exatamente 3 números!")

with aba2:
    st.header("🏆 Ranking")
    vencedor = st.text_input("Centena Sorteada", max_chars=3)
    try:
        df = conn.read()
        if not df.empty:
            def destacar(row):
                return ['background-color: gold; color: black'] * len(row) if row['Palpite'] == vencedor else [''] * len(row)
            st.table(df.style.apply(destacar, axis=1))
    except:
        st.info("Aguardando dados da planilha...")

with aba3:
    st.header("Enviar Convite")
    # Link que você quer criar
    link_final = "https://bolao-entre-amigos.streamlit.app"
    msg = f"Participe do meu bolão! Acesse: {link_app}"
    st.markdown(f"[📲 Enviar para Amigos](https://wa.me/?text={msg.replace(' ', '%20')})")
