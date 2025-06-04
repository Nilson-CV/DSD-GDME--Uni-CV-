import streamlit as st
from database import (
    cadastrar_professor, listar_professores, atualizar_professor,
    remover_professor, buscar_professores
)

def professores_page():
    st.title("📘 Gestão de Professores")

    menu = st.radio("Menu", ["Cadastrar", "Listar/Editar/Remover", "Pesquisar"])

    # --- Cadastro ---
    if menu == "Cadastrar":
        if st.session_state.nivel != "admin":
            st.error("Acesso restrito.")
            return

        st.subheader("➕ Cadastrar Professor")
        with st.form("form_cadastro"):
            codigo = st.text_input("Código do Professor")
            nome = st.text_input("Nome do Professor")
            grau = st.selectbox("Grau Acadêmico", ["Licenciado", "Mestre", "Doutor", "Outro"])
            enviar = st.form_submit_button("Cadastrar")

            if enviar:
                if codigo and nome:
                    cadastrar_professor(codigo, nome, grau)
                    st.success("Professor cadastrado.")
                else:
                    st.warning("Preencha todos os campos.")

    # --- Listar / Editar / Remover ---
    elif menu == "Listar/Editar/Remover":
        if st.session_state.nivel != "admin":
            st.error("Acesso restrito.")
            return

        st.subheader("📋 Professores Cadastrados")
        professores = listar_professores()

        if not professores:
            st.info("Nenhum professor cadastrado.")
            return

        for prof in professores:
            with st.expander(f"{prof[1]} ({prof[0]})"):
                novo_nome = st.text_input("Nome", prof[1], key=f"nome_{prof[0]}")
                novo_grau = st.selectbox(
                    "Grau",
                    ["Licenciado", "Mestre", "Doutor", "Outro"],
                    index=["Licenciado", "Mestre", "Doutor", "Outro"].index(prof[2]),
                    key=f"grau_{prof[0]}"
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Salvar Alterações", key=f"salvar_{prof[0]}"):
                        atualizar_professor(prof[0], novo_nome, novo_grau)
                        st.success("Dados atualizados.")
                
                with col2:
                    if st.button("Remover Professor", key=f"remover_{prof[0]}"):
                        remover_professor(prof[0])
                        st.warning(f"Professor {prof[1]} removido.")
                        st.rerun()  # pode ser substituído se preferir evitar

    # --- Pesquisa ---
    elif menu == "Pesquisar":
        st.subheader("🔍 Pesquisar Professor")
        termo = st.text_input("Digite o nome ou código:")
        if termo:
            resultados = buscar_professores(termo)
            if resultados:
                st.table({
                    "Código": [r[0] for r in resultados],
                    "Nome": [r[1] for r in resultados],
                    "Grau": [r[2] for r in resultados]
                })
            else:
                st.info("Nenhum professor encontrado.")
