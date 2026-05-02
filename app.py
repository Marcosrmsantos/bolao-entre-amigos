import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Bolão entre Amigos", page_icon="🏆")

# Conexão com a Planilha Google
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🎟️ Bolão entre Amigos")

# Criação das abas
aba1, aba2, aba3 = st.tabs(["📌 Registrar", "📊 Ranking", "📲 Convite"])

with aba1:
    st.header("Cadastrar Palpite")
    nome = st.text_input("Seu Nome")
    palpite = st.text_input("Sua Centena (000-999)", max_chars=3)

    if st.button("Confirmar Palpite"):
        if len(palpite) == 3 and palpite.isdigit():
            try:
                # 1. Lê os dados atuais da Página1
                df_atual = conn.read(worksheet="Dados")
                
                # 2. Prepara o novo dado (usando 'Nomes' como está na sua planilha)
                novo_dado = pd.DataFrame([{"Nomes": nome, "Palpite": palpite}])
                
                # 3. Junta o antigo com o novo
                df_final = pd.concat([df_atual, novo_dado], ignore_index=True)
                
                # 4. Escrita Direta (O disjuntor reforçado)
                spreadsheet_id = st.secrets["connections"]["gsheets"]["spreadsheet"]
                conn.client.update(
                    spreadsheet=spreadsheet_id, 
                    worksheet="Página1", 
                    data=[df_final.columns.values.tolist()] + df_final.values.tolist()
                )
                
                st.success(f"Sorte lançada, {nome}!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.error("Insira exatamente 3 números!")

with aba2:
    st.header("🏆 Ranking")
    vencedor = st.text_input("Centena Sorteada", max_chars=3)
    
    try:
        df = conn.read(worksheet="Dados")
        if not df.empty:
            def destacar(row):
                return ['background-color: gold; color: black'] * len(row) if row['Palpite'] == vencedor else [''] * len(row)
            st.table(df.style.apply(destarar, axis=1))
    except:
        st.info("Ainda não temos palpites registrados.")

with aba3:
    st.header("📨 Enviar Convite")
    link_app = "https://bolao-entre-amigos.streamlit.app"
    texto_convite = f"Participe do nosso Bolão! Acesse: {link_app}"
    st.code(texto_convite)
    st.write("Copie o texto acima e envie para seus amigos!")
