import streamlit as st
from DB_GDME import (
    listar_professores, listar_disciplinas, listar_cursos,
    cadastrar_aula, listar_aulas
)

def aulas_page():
    st.title("📅 Cadastro de Aulas")

    menu = st.radio("Menu", ["Cadastrar Aula", "Listar Aulas"])

    if menu == "Cadastrar Aula":
        if st.session_state.nivel != "admin":
            st.error("Acesso restrito.")
            return

        st.subheader("➕ Cadastrar Nova Aula")

        professores = listar_professores()
        disciplinas = listar_disciplinas()
        cursos = listar_cursos()

        if not professores or not disciplinas or not cursos:
            st.warning("Certifique-se de que há professores, disciplinas e cursos cadastrados.")
            return

        professor = st.selectbox("Professor", [f"{p[0]} - {p[1]}" for p in professores])
        disciplina = st.selectbox("Disciplina", [f"{d[0]} - {d[1]}" for d in disciplinas])
        curso = st.selectbox("Curso", [f"{c[0]} - {c[1]}" for c in cursos])
        tipo = st.radio("Tipo de Aula", ["teorica", "pratica"])

        if st.button("Cadastrar"):
            prof_cod = professor.split(" - ")[0]
            disc_cod = disciplina.split(" - ")[0]
            curso_cod = curso.split(" - ")[0]

            cadastrar_aula(prof_cod, disc_cod, curso_cod, tipo)

    elif menu == "Listar Aulas":
        st.subheader("📋 Aulas Cadastradas")
        aulas = listar_aulas()
        if aulas:
            st.table({
                "ID": [a[0] for a in aulas],
                "Professor": [a[1] for a in aulas],
                "Disciplina": [a[2] for a in aulas],
                "Curso": [a[3] for a in aulas],
                "Tipo": [a[4] for a in aulas],
            })
        else:
            st.info("Nenhuma aula cadastrada.")
