import streamlit as st
from login import login_page
from DB_GDME import criar_tabela_professores, criar_tabela_disciplinas, criar_tabela_cursos, criar_tabela_aulas
from disciplinas import disciplinas_page
from professores import professores_page
from cursos import cursos_page
from DB_GDME import criar_tabela_aulas
from aulas import aulas_page



criar_tabela_professores()
criar_tabela_disciplinas()
criar_tabela_cursos()
criar_tabela_aulas()
criar_tabela_aulas_cursos()




if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario = ""
    st.session_state.nivel = ""

if not st.session_state.autenticado:
    login_page()
    st.stop()

st.sidebar.markdown(f"""
    <p style='font-size:20px; color:green;'>
         👤 <strong>USUÁRIO: </strong>  <strong>{st.session_state.usuario}</strong>
    </p>
""", unsafe_allow_html=True)
st.sidebar.markdown(f"""
    <p style='font-size:20px; color:blue;'>
         🔐 <strong>NÍVEL: </strong>  <strong>{st.session_state.nivel}</strong>
    </p>
""", unsafe_allow_html=True)

paginas = {
    "👨‍🏫  PROFESSORES": professores_page,
    "📚  DISCIPLINAS": disciplinas_page,
    "🏫  CURSOS": cursos_page,
    "📝  AULAS": aulas_page,
    # outras páginas futuras...
}

# Botão de logout
if st.sidebar.button("🔒 Logout"):
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]
    st.rerun()


st.sidebar.markdown("<h3>📌 Selecione uma das Opções:</h3>", unsafe_allow_html=True)
selecao = st.sidebar.radio("",list(paginas.keys()))
paginas[selecao]()
