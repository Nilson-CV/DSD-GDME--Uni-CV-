import sqlite3
import streamlit as st
from fpdf import FPDF
from io import BytesIO
import pandas as pd
from gerar_pdf import gerar_pdf_estilizado

# Conexão com banco
conn = sqlite3.connect('gdme_unicv.db', check_same_thread=False)
cursor = conn.cursor()

# Função para criar as tabelas (executar uma vez)
def criar_tabelas():
    with open("gdme_unicv.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    cursor.executescript(sql_script)
    conn.commit()

criar_tabelas()

st.title("📚 Gestão de Disciplinas - GDME Uni-CV")

menu = st.sidebar.radio("Menu", ["Cadastrar Professor", "Cadastrar Disciplina", "Cadastrar Curso", "Cadastrar Aula em Curso", "Relatório de Carga Horária"])

# CADASTRO DE PROFESSOR
if menu == "Cadastrar Professor":
    st.subheader("👨‍🏫 Cadastro de Professor")
    codigo = st.text_input(":blue[**Código do professor:**]")
    nome = st.text_input(":blue[**Nome do professor:**]")
    grau = st.selectbox(":blue[**Grau Acadêmico:**]", ["Licenciado", "Mestre", "Doutor"])
    if st.button("Salvar"):
        carga_horaria_max = 28 if grau in ['Licenciado', 'Mestre'] else 24
        cursor.execute("INSERT INTO professores (codigo, nome, grau, carga_horaria_max) VALUES (?, ?, ?, ?)", (codigo, nome, grau, carga_horaria_max))
        conn.commit()
        st.success(f"Professor **{nome.upper()}** cadastrado com sucesso!")

# CADASTRO DE DISCIPLINA
elif menu == "Cadastrar Disciplina":
    st.subheader("📘 Cadastro de Disciplina")
    codigo = st.text_input("Código da disciplina")
    nome = st.text_input("Nome da disciplina")
    teorica = st.number_input("Horas Teóricas", min_value=0, step=1)
    pratica = st.number_input("Horas Práticas", min_value=0, step=1)
    if st.button("Cadastrar"):
        total = teorica + pratica
        cursor.execute("INSERT INTO disciplinas (codigo, nome, carga_total, carga_teorica, carga_pratica) VALUES (?, ?, ?, ?, ?)", (codigo,nome, total, teorica, pratica))
        conn.commit()
        st.success("Disciplina cadastrada com sucesso!")

# CADASTRO DE CURSO
elif menu == "Cadastrar Curso":
    st.subheader("🏫 Cadastro de Curso")
    codigo = st.text_input("Código do curso")
    nome = st.text_input("Nome do curso")
    if st.button("Cadastrar Curso"):
        cursor.execute("INSERT INTO cursos (codigo, nome) VALUES (?, ?)", (codigo, nome))
        conn.commit()
        st.success("Curso cadastrado com sucesso!")

# ATRIBUIR PROFESSORES
#elif menu == "Atribuir Professores":
#    st.subheader("👨‍🏫 Atribuição de Professores às Disciplinas")
#
#    disciplinas = cursor.execute("SELECT codigo, nome FROM disciplinas").fetchall()
#    professores = cursor.execute("SELECT codigo, nome FROM professores").fetchall()
#    
#    disc_id = st.selectbox("Disciplina", disciplinas, format_func=lambda x: x[1])
#    tipo = st.radio("Tipo de aula", ["Teorica", "Pratica"])
#    prof_id = st.selectbox("Professor", professores, format_func=lambda x: x[1])
#    
#    if st.button("Atribuir"):
#        cursor.execute("INSERT INTO aula_responsavel (disciplina_id, professor_id, tipo) VALUES (?, ?, ?)", (disc_id[0], prof_id[0], tipo))
#        conn.commit()
#        st.success(f"Professor(a) **{prof_id[1]}** associado(a) à parte **{tipo}** da disciplina **{disc_id[1]}**.")

# Cadastrar Aula (Professor e Disciplina) em Curso
elif menu == "Cadastrar Aula em Curso":
    st.subheader("📚 Cadastro de Aula por Curso")

    disciplinas = cursor.execute("SELECT codigo, nome FROM disciplinas").fetchall()
    cursos = cursor.execute("SELECT codigo, nome FROM cursos").fetchall()
    professores = cursor.execute("SELECT codigo, nome FROM professores").fetchall()

    disc_id = st.selectbox("Disciplina", disciplinas, format_func=lambda x: x[1])
    curso_id = st.selectbox("Curso", cursos, format_func=lambda x: x[1])
    tipo = st.radio("Tipo de aula", ["Teorica", "Pratica"])
    prof_id = st.selectbox("Professor", professores, format_func=lambda x: x[1])

    if st.button("Cadastrar Aula"):
        # 1. Inserir aula
        # Verifique se já existe uma aula igual
        cursor.execute("""
            SELECT 1 FROM aulas
            WHERE disciplina_id = ? AND curso_id = ? AND tipo = ?
        """, (disc_id[0], curso_id[0], tipo))
        existe = cursor.fetchone()
        if existe:
            st.warning("Esta aula já foi cadastrada para este professor.")
        else:

            cursor.execute("""
                INSERT INTO aulas (disciplina_id, professor_id, tipo, carga_horaria)
                VALUES (?, ?, ?, ?)
            """, (disciplina_id, professor_id, tipo, carga_horaria))

            aula_id = cursor.lastrowid

            # Associar múltiplos cursos
            for curso_id in cursos_selecionados:
                cursor.execute("INSERT INTO aula_cursos (aula_id, curso_id) VALUES (?, ?)", (aula_id, curso_id))


            #cursor.execute("""
            #    INSERT INTO aulas (disciplina_id, curso_id, professor_id, tipo)
            #    VALUES (?, ?, ?, ?)
            #""", (disc_id[0], curso_id[0], prof_id[0], tipo))

            # 2. Buscar carga horária correspondente da disciplina
            if tipo == "Teorica":
                cursor.execute("SELECT carga_teorica FROM disciplinas WHERE codigo = ?", (disc_id[0],))
            else:
                cursor.execute("SELECT carga_pratica FROM disciplinas WHERE codigo = ?", (disc_id[0],))

            conn.commit()
            st.success("Aula cadastrada com sucesso!")

# RELATÓRIO DA CARGA HORÁRIA        
elif menu == "Relatório de Carga Horária":
    st.subheader("📊 Relatório de Carga Horária Detalhado")

    # Obter dados únicos para filtros
    cursos = cursor.execute("SELECT codigo, nome FROM cursos").fetchall()
    professores = cursor.execute("SELECT codigo, nome FROM professores").fetchall()
    tipos = ["Teorica", "Pratica"]

    # Transformar em listas
    cursos_nomes = [c[1] for c in cursos]
    professores_nomes = [p[1] for p in professores]

    # Layout de filtros
    st.subheader("🔎 Filtros do Relatório")


    def limpar_filtros():
        st.session_state["filtro_cursos"] = []
        st.session_state["filtro_profs"] = []
        st.session_state["filtro_tipos"] = []

    # Botão para limpar filtros
    if st.button("🧹 Limpar Filtros", on_click=limpar_filtros):
        st.session_state["filtro_cursos"] = []
        st.session_state["filtro_profs"] = []
        st.session_state["filtro_tipos"] = []

    col1, col2, col3 = st.columns(3)

    with col1:
        cursos_sel = st.multiselect("Cursos", options=cursos_nomes, default=[], key="filtro_cursos")
    with col2:
        profs_sel = st.multiselect("Professores", options=professores_nomes, default=[], key="filtro_profs")
    with col3:
        tipos_sel = st.multiselect("Tipo de Aula", options=tipos, default=[], key="filtro_tipos")

    # Construir query com filtros múltiplos
    query = """
        SELECT p.nome AS Professor, p.grau AS Grau, p.carga_horaria_max AS Max, p.carga_horaria AS Atual,
            d.nome AS Disciplina, c.nome AS Curso, a.tipo AS Tipo
        FROM aulas a
        JOIN professores p ON a.professor_id = p.codigo
        JOIN disciplinas d ON a.disciplina_id = d.codigo
        JOIN cursos c ON a.curso_id = c.codigo
        WHERE 1 = 1
    """

    params = []

    if cursos_sel:
        query += f" AND c.nome IN ({','.join(['?'] * len(cursos_sel))})"
        params.extend(cursos_sel)

    if profs_sel:
        query += f" AND p.nome IN ({','.join(['?'] * len(profs_sel))})"
        params.extend(profs_sel)

    if tipos_sel:
        query += f" AND a.tipo IN ({','.join(['?'] * len(tipos_sel))})"
        params.extend(tipos_sel)

    # Executar e exibir
    dados = cursor.execute(query, params).fetchall()
    df = pd.DataFrame(dados, columns=["Professor", "Grau", "Max", "Atual", "Disciplina", "Curso", "Tipo"])

    st.dataframe(df)

    # CSV + PDF (se quiser adicionar os botões aqui)
    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar CSV", data=csv, file_name="relatorio_carga.csv", mime="text/csv")

        pdf_bytes = gerar_pdf_estilizado(df)
        st.download_button("📄 Baixar PDF", data=pdf_bytes, file_name="relatorio_carga.pdf", mime="application/pdf")