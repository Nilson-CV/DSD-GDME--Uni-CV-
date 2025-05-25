import sqlite3
import streamlit as st

# Conexão com banco
conn = sqlite3.connect('gdme_unicv.db', check_same_thread=False)
cursor = conn.cursor()

# Função para criar as tabelas (executar uma vez)
def criar_tabelas():
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS professores (
        codigo TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        grau TEXT CHECK (grau IN ('Licenciado', 'Mestre', 'Doutor')) NOT NULL,
        carga_horaria_max INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS disciplinas (
        codigo TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        carga_total INTEGER NOT NULL,
        carga_teorica INTEGER NOT NULL,
        carga_pratica INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS cursos (
        codigo TEXT PRIMARY KEY,
        nome TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS disciplina_curso (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        disciplina_id INTEGER,
        curso_id INTEGER,
        FOREIGN KEY (disciplina_id) REFERENCES disciplinas(codigo),
        FOREIGN KEY (curso_id) REFERENCES cursos(codigo)
    );

    CREATE TABLE IF NOT EXISTS aula_responsavel (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        disciplina_id INTEGER,
        professor_id INTEGER,
        tipo TEXT CHECK (tipo IN ('Teorica', 'Pratica')),
        FOREIGN KEY (disciplina_id) REFERENCES disciplinas(codigo),
        FOREIGN KEY (professor_id) REFERENCES professores(codigo)
    );
    """)
    conn.commit()

criar_tabelas()

st.title("📚 Gestão de Disciplinas - GDME Uni-CV")

menu = st.sidebar.selectbox("Menu", ["Cadastrar Professor", "Cadastrar Disciplina", "Cadastrar Curso", "Atribuir Professores", "Relatório de Carga Horária"])

# CADASTRO DE PROFESSOR
if menu == "Cadastrar Professor":
    st.subheader("👨‍🏫 Cadastro de Professor")
    codigo = st.text_input("Código do professor")
    nome = st.text_input("Nome do professor")
    grau = st.selectbox("Grau Acadêmico", ["Licenciado", "Mestre", "Doutor"])
    if st.button("Salvar"):
        carga_horaria_max = 28 if grau in ['Licenciado', 'Mestre'] else 24
        cursor.execute("INSERT INTO professores (codigo, nome, grau, carga_horaria_max) VALUES (?, ?, ?, ?)", (codigo, nome, grau, carga_horaria_max))
        conn.commit()
        st.success("Professor cadastrado com sucesso!")

# CADASTRO DE DISCIPLINA
elif menu == "Cadastrar Disciplina":
    st.subheader("📘 Cadastro de Disciplina")
    codigo = st.text_input("Códido da disciplina")
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
        cursor.execute("INSERT INTO cursos (codigo, nome) VALUES (?, ?)", (codigo,nome))
        conn.commit()
        st.success("Curso cadastrado com sucesso!")

# ATRIBUIR PROFESSORES
elif menu == "Atribuir Professores":
    st.subheader("👨‍🏫 Atribuição de Professores às Disciplinas")

    disciplinas = cursor.execute("SELECT codigo, nome FROM disciplinas").fetchall()
    professores = cursor.execute("SELECT codigo, nome FROM professores").fetchall()
    
    disc_id = st.selectbox("Disciplina", disciplinas, format_func=lambda x: x[1])
    tipo = st.radio("Tipo de aula", ["Teorica", "Pratica"])
    prof_id = st.selectbox("Professor", professores, format_func=lambda x: x[1])
    
    if st.button("Atribuir"):
        cursor.execute("INSERT INTO aula_responsavel (disciplina_id, professor_id, tipo) VALUES (?, ?, ?)", (disc_id[0], prof_id[0], tipo))
        conn.commit()
        st.success(f"Professor(a) {professores[0]}} associado(a) à parte {tipo.lower()} da disciplina.")

# RELATÓRIO
elif menu == "Relatório de Carga Horária":
    st.subheader("📊 Relatório de Carga Horária por Professor")

    dados = cursor.execute("""
    SELECT 
        p.nome,
        p.grau,
        p.carga_horaria_max,
        COALESCE(SUM(
            CASE a.tipo
                WHEN 'Teorica' THEN d.carga_teorica
                WHEN 'Pratica' THEN d.carga_pratica
            END
        ), 0) AS carga_atual
    FROM professores p
    LEFT JOIN aula_responsavel a ON p.codigo = a.professor_id
    LEFT JOIN disciplinas d ON a.disciplina_id = d.codigo
    GROUP BY p.codigo;
    """).fetchall()

    for nome, grau, maximo, atual in dados:
        st.write(f"**{nome}** ({grau}): {atual}h / {maximo}h")

