import streamlit as st
from DB_GDME import (
    listar_professores, listar_disciplinas, listar_cursos,
    cadastrar_aula, inserir_aula, buscar_aulas_por_professor
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
            horas = st.number_input("⏱️ Duração da aula (horas)", min_value=1, max_value=6, value=2)
            sala = st.text_input("🏫 Sala", value="A101")
            horario_inicio = st.time_input("🕒 Horário de Início")

            # Calcular horário de término
            inicio = datetime.strptime(str(horario_inicio), "%H:%M:%S")
            fim = inicio + timedelta(hours=horas)
            st.info(f"🕘 Horário previsto: {inicio.strftime('%H:%M')} - {fim.strftime('%H:%M')}")

            st.markdown("### 👥 Cursos e Semestre")
            cursos_selecionados = st.multiselect("Selecione os cursos:", cursos, format_func=lambda x: f"{x[1]} ({x[0]})")

            cursos_semestres = []
            for curso in cursos_selecionados:
                semestre = st.text_input(f"📅 Semestre para o curso {curso[1]}", key=f"sem_{curso[0]}")
                if semestre:
                    cursos_semestres.append((curso[0], semestre))

            if st.button("✅ Cadastrar Aula"):
                if not cursos_semestres:
                    st.warning("⚠️ Informe pelo menos um semestre para os cursos selecionados.")
                else:
                    inserir_aula(prof[0], disc[0], tipo, horas, sala, horario_inicio.strftime("%H:%M"), cursos_semestres)
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

                        with st.expander(f"📘 {aula['disciplina']} - {aula['tipo'].capitalize()}"):
                            st.markdown(f"""
                            <div style='background-color:#f1f1f1;padding:15px;border-left:5px solid #2e7d32;'>
                                <b>🧑‍🏫 Professor:</b> {selecionado[1]}<br>
                                <b>🧭 Tipo:</b> {aula['tipo'].capitalize()}<br>
                                <b>🏫 Sala:</b> {aula['sala']}<br>
                                <b>⏰ Horário:</b> {hora_inicio.strftime('%H:%M')} - {hora_fim.strftime('%H:%M')}<br>
                                <b>⏱️ Duração:</b> {aula['horas']}h<br>
                                <b>👥 Cursos:</b> {cursos_formatados}
                            </div>
                            """, unsafe_allow_html=True)