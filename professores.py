import streamlit as st
import base64
import pandas as pd
from DB_GDME import (
    cadastrar_professor, listar_professores, atualizar_professor,
    remover_professor, buscar_professores, gerar_proximo_codigo_professor
)


def professores_page():
    st.title("👨‍🏫 Gestão de Professores")
    if st.session_state.nivel == "admin":
        #menu = st.radio("Menu", ["Cadastrar", "Selecionar/Editar/Remover", "Informações do Professor"])
        tab1, tab2, tab3, tab4 = st.tabs([" ➕ CADASTRAR", " 📋 LISTAR/EDITAR/REMOVER", "👤 INFORMAÇÕES do PROFESSOR", "📚  DISCIPLINAS LECIONADAS"])
        with tab1:
            if st.session_state.nivel == "admin":
                # --- Cadastro ---
                st.subheader("➕ Cadastrar Professor")
                # Inserção dos dados no formulário:
                with st.form("form_cadastro"):
                    codigo = gerar_proximo_codigo_professor()
                    nome = st.text_input("Nome do Professor")
                    grau = st.selectbox("Grau Académico", ["Licenciado(a)", "Mestre", "Doutor(a)", "Outro"])
                    email = st.text_input("Email (opcional)", value="")
                    resumo = st.text_area("Resumo de Investigação", placeholder="Digite um parágrafo sobre a investigação do professor")
                    foto_file = st.file_uploader("Foto do professor (opcional)", type=["jpg", "png", "jpeg"])
                    # Mensagem a ser apresentada, caso o email não for informado:
                    if not email and nome:
                        email = f"email não definido"
                    # Clique no botão cadastrar
                    enviar = st.form_submit_button("Cadastrar")
                    if enviar:
                        # Tratamento da foto
                        foto_path = ""
                        if foto_file:
                            import os
                            os.makedirs("fotos", exist_ok=True)
                            ext = os.path.splitext(foto_file.name)[1]
                            foto_path = f"fotos/{codigo}{ext}"
                            with open(foto_path, "wb") as f:
                                f.write(foto_file.read())
                        if codigo and nome:
                            # Efetivação do cadastro:
                            cadastrar_professor(codigo, nome, grau, email, resumo, foto_path)
                        else:
                            st.warning("Preencha os campos obrigatórios.")
        # --- Selecionar / Editar / Remover ---
        with tab2:
            st.subheader("📋 Professores Cadastrados")
            # Lista dos professores:
            professores = listar_professores()
            # Informação, caso nenhum professor tenha sido cadastrado:
            if not professores:
                st.info("Nenhum professor cadastrado.")
                return
            # Seleção/Edição/Remoção:
            for prof in professores:
                with st.expander(f"{prof[1]} ({prof[0]})"):
                    novo_nome = st.text_input("Nome", prof[1], key=f"nome_{prof[0]}")
                    novo_grau = st.selectbox(
                        "Grau",
                        ["Licenciado(a)", "Mestre", "Doutor(a)", "Outro"],
                        index=["Licenciado(a)", "Mestre", "Doutor(a)", "Outro"].index(prof[2]),
                        key=f"grau_{prof[0]}"
                    )
                    novo_email = st.text_input("Email", prof[3] or "", key=f"email_{prof[0]}")
                    novo_resumo = st.text_area("Resumo", prof[4] or "", key=f"resumo_{prof[0]}")
                    nova_foto = st.file_uploader("Nova foto (opcional)", type=["jpg", "jpeg", "png"], key=f"foto_file_{prof[0]}")
                    #novo_foto_file = st.file_uploader("Foto do professor (opcional)", prof[5] or "", key=f"foto_file_{prof[0]}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Salvar Alterações", key=f"salvar_{prof[0]}"):
                            novo_caminho_foto = None
                            if nova_foto:
                                import os
                                os.makedirs("fotos", exist_ok=True)
                                ext = os.path.splitext(nova_foto.name)[1]
                                novo_caminho_foto = f"fotos/{prof[0]}{ext}"
                                with open(novo_caminho_foto, "wb") as f:
                                    f.write(nova_foto.read())
                            #atualizar_professor(codigo, nome, grau, email, resumo, novo_caminho_foto)
                            #st.success("Informações do professor atualizadas com sucesso.")
                            atualizar_professor(prof[0], novo_nome, novo_grau, novo_email, novo_resumo, novo_caminho_foto)
                            st.success("Dados atualizados.")                 
                    with col2:
                        if st.button("Remover Professor", key=f"remover_{prof[0]}"):
                            remover_professor(prof[0])
                            st.warning(f"Professor {prof[1]} removido.")
                            st.rerun()  # pode ser substituído se preferir evitar

            # --- Pesquisa ---
            #elif menu == "Pesquisar":
            #    st.subheader("🔍 Pesquisar Professor")
            #    termo = st.text_input("Digite nome ou código:")

            #    if termo:
            #        resultados = buscar_professores(termo)
            #        if resultados:
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

                #        n = 0
                #        for i in resultados:
                #            lista = ["Código", "Professor", "Grau", "Email", "Investigação"]
                #            k = 0                    
                #            for j in resultados[n]:
                #                st.markdown(f"## {lista[k]}: {j}")
                #                k = k + 1
                #            n = n + 1
                #    else:
                #        st.info("Nenhum professor encontrado.")

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
        with tab3:
            st.subheader("👤 Informações do Professor")
            st.rerun
            professores = listar_professores()
            if not professores:
                st.info("Nenhum professor cadastrado.")
                st.stop()

            nomes = [p[1] for p in professores]
            nome_escolhido = st.selectbox("Selecione o professor", nomes)

            # Obter o professor selecionado
            prof = next(p for p in professores if p[1] == nome_escolhido)

            colp1, colp2 = st.columns([1, 3])
            with colp2:
                st.markdown(f"### 📌 Professor(a): {prof[1]}")
            with colp1:
                import os
                #if prof[5] and os.path.exists(prof[5]):
                #    st.image(prof[5], width=100)
                #else:
                #    st.image("fotos/default.png", width=150)  # imagem padrão

                imagem = prof[5] if prof[5] and os.path.exists(prof[5]) else "fotos/default.jpg"
                st.markdown(
                    f"""
                    <div style='width:150px; height:150px; border:1px solid #ddd; border-radius:8px; overflow:hidden; display:flex; align-items:center; justify-content:center; background-color:#f9f9f9;'>
                        <img src='data:image/png;base64,{base64.b64encode(open(imagem, "rb").read()).decode()}' style='max-width: 100%; max-height: 100%;'>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.markdown(f"**🆔 Código:** `{prof[0]}`")
            with col2:
                st.markdown(f"**🎓 Grau:** `{prof[2]}`")
            with col3:
                st.markdown(f"**📧 Email:** {prof[3] or '*não informado*'}")
                
            st.markdown("**📝 Área de Investigação:**")
            st.info(prof[4] or "Sem resumo disponível.")

    else:
        #menu = st.radio("Menu", ["Informações do Professor"]) 
        tab1, tab2 = st.tabs(["👤 INFORMAÇÕES do PROFESSOR", "📚  DISCIPLINAS LECIONADAS"])
        with tab1:
            st.subheader("👤 Informações do Professor")
            st.rerun
            professores = listar_professores()
            if not professores:
                st.info("Nenhum professor cadastrado.")
                st.stop()

            nomes = [p[1] for p in professores]
            nome_escolhido = st.selectbox("👨‍🏫 :blue[**Selecione o professor:**]", nomes)
            
            # Obter o professor selecionado
            prof = next(p for p in professores if p[1] == nome_escolhido)

            colp1, colp2 = st.columns([1, 3])
            with colp2:
                st.markdown(f"### 📌 Professor(a): {prof[1]}")
            with colp1:
                import os
                #if prof[5] and os.path.exists(prof[5]):
                #    st.image(prof[5], width=100)
                #else:
                #    st.image("fotos/default.png", width=150)  # imagem padrão

                imagem = prof[5] if prof[5] and os.path.exists(prof[5]) else "fotos/default.jpg"
                st.markdown(
                    f"""
                    <div style='width:150px; height:150px; border:1px solid #ddd; border-radius:8px; overflow:hidden; display:flex; align-items:center; justify-content:center; background-color:#f9f9f9;'>
                        <img src='data:image/png;base64,{base64.b64encode(open(imagem, "rb").read()).decode()}' style='max-width: 100%; max-height: 100%;'>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.markdown(f"**🆔 Código:** `{prof[0]}`")
            with col2:
                st.markdown(f"**🎓 Grau:** `{prof[2]}`")
            with col3:
                st.markdown(f"**📧 Email:** {prof[3] or '*não informado*'}")
                
            st.markdown("**📝 Área de Investigação:**")
            st.info(prof[4] or "Sem resumo disponível.")
   
        

