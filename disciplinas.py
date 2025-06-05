import streamlit as st
from DB_GDME import cadastrar_disciplina, listar_disciplinas, buscar_disciplinas

def disciplinas_page():
    st.title("📚 Gestão de Disciplinas")

    menu = st.radio("Menu", ["Cadastrar", "Listar/Editar/Remover", "Pesquisar"])

    if menu == "Cadastrar":
        if st.session_state.nivel != "admin":
            st.error("Acesso restrito.")
            return

        st.subheader("➕ Cadastrar Disciplina")
        with st.form("form_disciplina"):
            codigo = st.text_input("Código da Disciplina")
            nome = st.text_input("Nome da Disciplina")
            horas_teoricas = st.number_input("Horas Teóricas", min_value=0, step=1)
            horas_praticas = st.number_input("Horas Práticas", min_value=0, step=1)
            enviar = st.form_submit_button("Cadastrar")

            if enviar:
                if codigo and nome:
                    cadastrar_disciplina(codigo, nome, int(horas_teoricas), int(horas_praticas))
                else:
                    st.warning("Preencha todos os campos.")

    elif menu == "Listar":
        st.subheader("📋 Disciplinas Cadastradas")
        disciplinas = listar_disciplinas()

        if disciplinas:
            st.table({
                "Código": [d[0] for d in disciplinas],
                "Nome": [d[1] for d in disciplinas],
                "Horas Teóricas": [d[2] for d in disciplinas],
                "Horas Práticas": [d[3] for d in disciplinas],
            })
        else:
            st.info("Nenhuma disciplina cadastrada.")

    elif menu == "Pesquisar":
        st.subheader("🔍 Pesquisar Disciplina")
        termo = st.text_input("Digite nome ou código:")
        if termo:
            resultados = buscar_disciplinas(termo)
            if resultados:
                st.table({
                    "Código": [r[0] for r in resultados],
                    "Nome": [r[1] for r in resultados],
                    "Horas Teóricas": [r[2] for r in resultados],
                    "Horas Práticas": [r[3] for r in resultados]
                })
            else:
                st.info("Nenhuma disciplina encontrada.")
    elif menu == "Listar/Editar/Remover":
        if st.session_state.nivel != "admin":
            st.error("Acesso restrito.")
            return

        st.subheader("📋 Disciplinas Cadastradas")
        disciplinas = listar_disciplinas()

        if not disciplinas:
            st.info("Nenhuma disciplina cadastrada.")
            return

        for disc in disciplinas:
            with st.expander(f"{disc[1]} ({disc[0]})"):
                novo_nome = st.text_input("Nome", disc[1], key=f"nome_{disc[0]}")
                nova_teorica = st.number_input("Horas Teóricas", min_value=0, step=1, value=disc[2], key=f"ht_{disc[0]}")
                nova_pratica = st.number_input("Horas Práticas", min_value=0, step=1, value=disc[3], key=f"hp_{disc[0]}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Salvar Alterações", key=f"salvar_{disc[0]}"):
                        atualizar_disciplina(disc[0], novo_nome, nova_teorica, nova_pratica)
                        st.success("Disciplina atualizada.")
                with col2:
                    if st.button("Remover Disciplina", key=f"remover_{disc[0]}"):
                        remover_disciplina(disc[0])
                        st.warning("Disciplina removida.")
                        st.rerun()  # para atualizar a lista
