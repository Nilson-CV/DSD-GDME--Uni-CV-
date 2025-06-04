import streamlit as st

def login_page():
    
    st.title("🔐 Acesso ao Sistema")

    usuarios = st.secrets["usuarios"]
    niveis = st.secrets["niveis"]

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario in usuarios and senha == usuarios[usuario]:
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.session_state.nivel = niveis.get(usuario, "usuario")
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")