import streamlit as st
from datetime import datetime, timedelta, time
from DB_GDME import (
    listar_professores, listar_disciplinas, listar_cursos, inserir_aula, buscar_aulas_por_professor,
    atualizar_cursos_aula, remover_aula,  atualizar_aula, conectar_db
)

def aulas_page():
    st.title("📅 Cadastro de Aulas")

    menu = st.radio("Menu", ["Cadastrar Aula", "Listar Aulas"])

    if st.session_state.nivel == "admin":
        if menu == "Cadastrar Aula":

            st.subheader("➕ Cadastrar Aula ")

            professores = listar_professores()
            disciplinas = listar_disciplinas()
            cursos = listar_cursos()

            prof = st.selectbox("👨‍🏫 Professor", professores, format_func=lambda x: f"{x[1]} ({x[0]})")
            disc = st.selectbox("📘 Disciplina", disciplinas, format_func=lambda x: f"{x[1]} ({x[0]})")
            tipo = st.radio("📚 Tipo de Aula", ["teorica", "pratica"], horizontal=True)
            horas = st.number_input("⏱️ Duração da aula (horas)", min_value=1, max_value=5, value=2)
            sala = st.text_input("🏫 Sala", value="A101")
            horario_inicio = st.time_input("🕒 Horário de Início")

            # Calcular horário de término
            inicio = datetime.strptime(str(horario_inicio), "%H:%M:%S")
            fim = inicio + timedelta(hours=horas)
            st.info(f"🕘 Horário previsto: {inicio.strftime('%H:%M')} - {fim.strftime('%H:%M')}")

            st.markdown("### 👥 Cursos e Semestre")
            cursos_selecionados = st.multiselect("Selecione os cursos:", cursos, format_func=lambda x: f"{x[1]} ({x[0]})")

            cursos_semestres_ano = []
            for curso in cursos_selecionados:
                semestre = st.text_input(f"📅 Semestre para o curso {curso[1]}", key=f"sem_{curso[0]}")
                ano = st.text_input(f"Ano letivo para o curso {curso[1]}", key=f"ano_{curso[0]}")
                if semestre:
                    cursos_semestres_ano.append((curso[0], semestre, ano))

            for curso, semestre, ano in cursos_semestres_ano:
                cursor.execute("""
                                INSERT INTO aulas_cursos (id_aula, curso_codigo, semestre, ano)
                                VALUES (?, ?, ?, ?)
                                """, (id_aula, curso, semestre, ano))

            if st.button("✅ Cadastrar Aula"):
                if not cursos_semestres_ano:
                    st.warning("⚠️ Informe pelo menos um semestre para os cursos selecionados.")
                else:
                    inserir_aula(prof[0], disc[0], tipo, horas, sala, horario_inicio.strftime("%H:%M"), cursos_semestres_ano)
                    st.success("✅ Aula cadastrada com sucesso!")
        else:
            st.subheader("📚 Aulas Atribuídas ao Professor")

            professores = listar_professores()
            selecionado = st.selectbox("👨‍🏫 Selecione o professor", professores, format_func=lambda x: f"{x[1]} ({x[0]})")

            if selecionado:
                aulas = buscar_aulas_por_professor(selecionado[0])
                if not aulas:
                    st.info("❌ Nenhuma aula atribuída.")
                else:
                    for aula in aulas:
                        hora_inicio = datetime.strptime(aula["horario_inicio"], "%H:%M")
                        hora_fim = hora_inicio + timedelta(hours=aula["horas"])
                        cursos_formatados = ", ".join([f"{c[0]} ({c[1]})" for c in aula["cursos"]])

                        col1, col2 = st.columns([0.85, 0.15])
                        with col1:
                            expanded = st.expander(f"📘 {aula['disciplina']} - {aula['tipo'].capitalize()}", expanded=False)
                            with expanded:             
                                st.markdown(f"""
                                <div style='background-color:#f1f1f1;padding:15px;border-left:5px solid #2e7d32;'>
                                    <b>🧑‍🏫 Professor:</b> {selecionado[1]}<br>
                                    <b>🧭 Tipo:</b> {aula['tipo'].capitalize()}<br>
                                    <b>🏫 Sala:</b> {aula['sala']}<br>
                                    <b>⏰ Horário:</b> {hora_inicio.strftime('%H:%M')} - {hora_fim.strftime('%H:%M')}<br>
                                    <b>⏱️ Duração:</b> {aula['horas']}h<br>
                                    <b>📅 Dia da semana:</b> {aula['dia_semana'] if aula['dia_semana'] else "(não definido)"}<br>
                                    <b>👥 Cursos:</b> {cursos_formatados}
                                </div>
                                """, unsafe_allow_html=True)

                        with col2:
                            if st.button(f"✏️ Editar", key=f"edit_{aula['id']}"):
                                st.session_state[f"edit_mode_{aula['id']}"] = True
                            if st.button(f"🗑️ Remover", key=f"del_{aula['id']}"):
                                remover_aula(aula["id"])
                                st.rerun()      

                        # Se estiver em modo edição, mostrar formulário
                        if st.session_state.get(f"edit_mode_{aula['id']}", False):
                            st.markdown("---")
                            st.write(f"✏️ Editando aula: {aula['disciplina']}")

                            tipo_novo = st.radio("Tipo de aula", ["teorica", "pratica"], index=0 if aula["tipo"]=="teorica" else 1, key=f"tipo_{aula['id']}")
                            horas_nova = st.number_input("Duração (horas)", min_value=1, max_value=6, value=aula["horas"], key=f"horas_{aula['id']}")
                            sala_nova = st.text_input("Sala", value=aula["sala"], key=f"sala_{aula['id']}")
                            horario_inicio_novo = st.time_input("Horário de início", value=datetime.strptime(aula["horario_inicio"], "%H:%M").time(), key=f"hora_{aula['id']}")
                            dia_semana_novo = st.text_input("Dia da semana (opcional)", value=aula["dia_semana"] or "", key=f"dia_{aula['id']}")

                            # Cursos e semestre (multi)
                            cursos = []
                            conn = conectar_db()
                            cursor = conn.cursor()
                            cursor.execute("SELECT codigo, nome FROM cursos")
                            cursos = cursor.fetchall()
                            conn.close()

                            cursos_selecionados = [c[0] for c in aula["cursos"]]
                            cursos_semes_novo = []
                            st.markdown("### Cursos e Semestre")
                            for curso in cursos:
                                checked = curso[0] in cursos_selecionados
                                col_c, col_s = st.columns([3,1])
                                with col_c:
                                    selecionado = st.checkbox(f"{curso[1]} ({curso[0]})", value=checked, key=f"curso_{curso[0]}_{aula['id']}")
                                with col_s:
                                    semestre_val = ""
                                    for c in aula["cursos"]:
                                        if c[0] == curso[0]:
                                            semestre_val = c[2]
                                            break
                                    semestre_novo = st.text_input(f"Semestre", value=semestre_val, key=f"semestre_{curso[0]}_{aula['id']}")
                                if selecionado:
                                    cursos_semes_novo.append((curso[0], semestre_novo))

                            if st.button("💾 Salvar alterações", key=f"salvar_{aula['id']}"):
                                # Salvar no banco
                                atualizar_aula(aula["id"], tipo_novo, horas_nova, sala_nova, horario_inicio_novo.strftime("%H:%M"), dia_semana_novo)
                                atualizar_cursos_aula(aula["id"], cursos_semes_novo)
                                st.success("✅ Aula atualizada com sucesso!")
                                st.session_state[f"edit_mode_{aula['id']}"] = False
                                st.rerun()

                            if st.button("❌ Cancelar", key=f"cancelar_{aula['id']}"):
                                st.session_state[f"edit_mode_{aula['id']}"] = False
                                st.rerun()                          