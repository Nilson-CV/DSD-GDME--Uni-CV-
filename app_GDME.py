from login import login_page
from DB_GDME import criar_tabela_professores, criar_tabela_disciplinas
from disciplinas import disciplinas_page
from professores import professores_page
from cursos import cursos_page
from DB_GDME import criar_tabela_aulas


criar_tabela_professores()
criar_tabela_disciplinas()
criar_tabela_cursos()
criar_tabela_aulas()


if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario = ""
    st.session_state.nivel = ""

if not st.session_state.autenticado:
    login_page()
    st.stop()


paginas = {
    "Professores": professores_page,
    "Disciplinas": disciplinas_page,
    "Cursos": cursos_page,
    "Aulas": aulas_page,
    # outras páginas futuras...
}

selecao = st.sidebar.radio("Navegar para:", list(paginas.keys()))
paginas[selecao]()