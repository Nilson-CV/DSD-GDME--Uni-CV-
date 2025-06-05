import streamlit as st
from DB_GDME import (
    cadastrar_curso, listar_cursos, buscar_cursos,
    atualizar_curso, remover_curso
)

def cursos_page():
    st.title("🎓 Gestão de Cursos")

    menu = st.radio("Menu", ["Cadastrar", "Listar/Editar/Remover", "Pesquisar"])

    # --- Cadastro ---
    if menu == "Cadastrar":
        if st.session_state.nivel != "admin":
            st.error("Acesso restrito.")
            return

        st.subheader("➕ Cadastrar Curso")
        with st.form("form_curso"):
            codigo = st.text_input("Código do Curso")
            nome = st.text_input("Nome do Curso")
            nivel = st.selectbox("Nível", ["Licenciatura", "Mestrado", "Doutorado", "Técnico", "Outro"])
            enviar = st.form_submit_button("Cadastrar")

            if enviar:
                if codigo and nome:
                    cadastrar_curso(codigo, nome, nivel)
                else:
                    st.warning("Preencha todos os campos.")

    # --- Listar / Editar / Remover ---
    elif menu == "Listar/Editar/Remover":
        if st.session_state.nivel != "admin":
            st.error("Acesso restrito.")
            return

        st.subheader("📋 Cursos Cadastrados")
        cursos = listar_cursos()

        if not cursos:
            st.info("Nenhum curso cadastrado.")
            return

        for curso in cursos:
            with st.expander(f"{curso[1]} ({curso[0]})"):
                novo_nome = st.text_input("Nome", curso[1], key=f"nome_{curso[0]}")
                novo_nivel = st.selectbox("Nível",
                                          ["Licenciatura", "Mestrado", "Doutorado", "Técnico", "Outro"],
                                          index=["Licenciatura", "Mestrado", "Doutorado", "Técnico", "Outro"].index(curso[2]),
                                          key=f"nivel_{curso[0]}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Salvar Alterações", key=f"salvar_{curso[0]}"):
                        atualizar_curso(curso[0], novo_nome, novo_nivel)
                        st.success("Curso atualizado.")
                with col2:
                    if st.button("Remover Curso", key=f"remover_{curso[0]}"):
                        remover_curso(curso[0])
                        st.warning("Curso removido.")
                        st.experimental_rerun()

    # --- Pesquisa ---
    elif menu == "Pesquisar":
        st.subheader("🔍 Pesquisar Curso")
        termo = st.text_input("Digite nome ou código:")
        if termo:
            resultados = buscar_cursos(termo)
            if resultados:
                st.table({
                    "Código": [r[0] for r in resultados],
                    "Nome": [r[1] for r in resultados],
                    "Nível": [r[2] for r in resultados]
                })
            else:
                st.info("Nenhum curso encontrado.")
