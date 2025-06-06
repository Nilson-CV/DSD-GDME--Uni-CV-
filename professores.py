import streamlit as st
import pandas as pd
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
        menu = st.radio("Menu", ["Cadastrar", "Listar/Editar/Remover", "Pesquisar", "Visualizar Professor"])
        # --- Cadastro ---
        if menu == "Cadastrar":
            st.subheader("➕ Cadastrar Professor")
            with st.form("form_cadastro"):
                codigo = st.text_input("Código do Professor")
                nome = st.text_input("Nome do Professor")
                grau = st.selectbox("Grau Acadêmico", ["Licenciado", "Mestre", "Doutor", "Outro"])
                email = st.text_input("Email (opcional)", value="")
                resumo = st.text_area("Resumo de Investigação", placeholder="Digite um parágrafo sobre a investigação do professor")
                foto_file = st.file_uploader("Foto do professor (opcional)", type=["jpg", "png", "jpeg"])

                if not email and nome:
                    email = f"{nome.lower().replace(' ', '')}@unicv.cv"

                enviar = st.form_submit_button("Cadastrar")

                if enviar:
                    foto_path = ""
                    if foto_file:
                        import os
                        os.makedirs("fotos", exist_ok=True)
                        ext = os.path.splitext(foto_file.name)[1]
                        foto_path = f"fotos/{codigo}{ext}"
                        with open(foto_path, "wb") as f:
                            f.write(foto_file.read())
                    if codigo and nome:
                        cadastrar_professor(codigo, nome, grau, email, resumo, foto_path)
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
            termo = st.text_input("Digite nome ou código:")

            if termo:
                resultados = buscar_professores(termo)
                if resultados:
                    #if resultados:
                    #    df = pd.DataFrame(resultados, columns=["Código", "Nome", "Grau", "Email", "Investigaçãosds"])
                    #    st.dataframe(df, use_container_width=True, hide_index=True)

                    #st.table({
                    #    "Código": [r[0] for r in resultados],
                    #    "Nome": [r[1] for r in resultados],
                    #    "Grau": [r[2] for r in resultados],
                    #    "Email": [r[3] or "" for r in resultados],
                    #    "Investigação": [r[4] or "" for r in resultados],
                    #})

                    n = 0
                    for i in resultados:
                        lista = ["Código", "Professor", "Grau", "Email", "Investigação"]
                        k = 0                    
                        for j in resultados[n]:
                            st.markdown(f"## {lista[k]}: {j}")
                            k = k + 1
                        n = n + 1
                else:
                    st.info("Nenhum professor encontrado.")

    #else:
    #    st.subheader("🔍 Pesquisar Professor")
    #    termo = st.text_input("Digite o nome ou código:")
    #    if termo:
    #        resultados = buscar_professores(termo)
    #        if resultados:
    #            st.table({
    #                "Código": [r[0] for r in resultados],
    #                "Nome": [r[1] for r in resultados],
    #                "Grau": [r[2] for r in resultados]
    #            })
    #        else:
    #            st.info("Nenhum professor encontrado.")

        elif menu == "Visualizar Professor":
            st.subheader("👤 Informações do Professor")

            professores = listar_professores()
            if not professores:
                st.info("Nenhum professor cadastrado.")
                st.stop()

            nomes = [p[1] for p in professores]
            nome_escolhido = st.selectbox("Selecione o professor", nomes)

            # Obter o professor selecionado
            prof = next(p for p in professores if p[1] == nome_escolhido)

            st.markdown(f"### 📌 Professor: {prof[1]}")

            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.markdown(f"**🆔 Código:** `{prof[0]}`")
            with col2:
                st.markdown(f"**🎓 Grau:** `{prof[2]}`")
            with col3:
                st.markdown(f"**📧 Email:** {prof[3] or '*não informado*'}")
            
                

            st.markdown("**📝 Área de Investigação:**")
            st.info(prof[4] or "Sem resumo disponível.")

        #if prof[5] and os.path.exists(prof[5]):
        #    st.image(prof[5], width=150)
        #else:
        #    st.image("fotos/default.png", width=150)  # imagem padrão

