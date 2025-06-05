import streamlit as st
from DB_GDME import (
    cadastrar_professor, listar_professores, atualizar_professor,
    remover_professor, buscar_professores
)

import sqlite3

conn = sqlite3.connect("banco_disciplinas.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE professores ADD COLUMN email TEXT;")
except:
    print("Campo 'email' já existe.")

try:
    cursor.execute("ALTER TABLE professores ADD COLUMN resumo TEXT;")
except:
    print("Campo 'resumo' já existe.")

conn.commit()
conn.close()


def professores_page():
    st.title("📘 Gestão de Professores")

    if st.session_state.nivel == "admin":
        menu = st.radio("Menu", ["Cadastrar", "Listar/Editar/Remover", "Pesquisar"])
        # --- Cadastro ---
        if menu == "Cadastrar":
            st.subheader("➕ Cadastrar Professor")
            with st.form("form_cadastro"):
                codigo = st.text_input("Código do Professor")
                nome = st.text_input("Nome do Professor")
                grau = st.selectbox("Grau Acadêmico", ["Licenciado", "Mestre", "Doutor", "Outro"])
                email = st.text_input("Email (opcional)", value="")
                resumo = st.text_area("Resumo de Investigação", placeholder="Digite um parágrafo sobre a investigação do professor")

                if not email and nome:
                    email = f"{nome.lower().replace(' ', '')}@unicv.cv"

                enviar = st.form_submit_button("Cadastrar")

                if enviar:
                    if codigo and nome:
                        cadastrar_professor(codigo, nome, grau, email, resumo)
                        st.success("Professor cadastrado.")
                    else:
                        st.warning("Preencha os campos obrigatórios.")


        # --- Listar / Editar / Remover ---
        elif menu == "Listar/Editar/Remover":

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
                    novo_email = st.text_input("Email", prof[3] or "", key=f"email_{prof[0]}")
                    novo_resumo = st.text_area("Resumo", prof[4] or "", key=f"resumo_{prof[0]}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Salvar Alterações", key=f"salvar_{prof[0]}"):
                            atualizar_professor(prof[0], novo_nome, novo_grau, novo_email, novo_resumo)
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
    else:
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
