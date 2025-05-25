import sqlite3
import streamlit as st

# Conexão com banco
conn = sqlite3.connect('gdme_unicv.db', check_same_thread=False)
cursor = conn.cursor()

# Função para criar as tabelas (executar uma vez)
def criar_tabelas():
    cursor.executescript(gdme_unicv.sql)
    conn.commit()

criar_tabelas()

st.title("📚 Gestão de Disciplinas - GDME Uni-CV")

menu = st.sidebar.selectbox("Menu", ["Cadastrar Professor", "Cadastrar Disciplina", "Cadastrar Curso", "Atribuir Professores", "Relatório de Carga Horária", "Cadastrar Aula em Curso"])

# CADASTRO DE PROFESSOR
if menu == "Cadastrar Professor":
    st.subheader("👨‍🏫 Cadastro de Professor")
    codigo = st.text_input("Código do professor")
    nome = st.text_input("Nome do professor")
    grau = st.selectbox("Grau Acadêmico", ["Licenciado", "Mestre", "Doutor"])
    if st.button("Salvar"):
        carga_horaria_max = 28 if grau in ['Licenciado', 'Mestre'] else 24
        cursor.execute("INSERT INTO professores (codigo, nome, grau, carga_horaria, carga_horaria_max) VALUES (?, ?, ?, ?, ?)", (codigo, nome, grau, carga_horaria, carga_horaria_max))
        conn.commit()
        st.success("Professor **{nome.upper()}** cadastrado com sucesso!")

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
        cursor.execute("INSERT INTO cursos (codigo, nome) VALUES (?, ?)", (codigo, nome))
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
        st.success(f"Professor(a) **{prof_id[1]}** associado(a) à parte **{tipo}** da disciplina **{disc_id[1]}**.")

# RELATÓRIO
elif menu == "Relatório de Carga Horária":
    st.subheader("📊 Relatório de Carga Horária por Professor")

    dados = cursor.execute("""
    SELECT 
        p.nome,
        p.grau,
        p.carga_horaria,
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
        cursor.execute("""
            INSERT INTO aulas (disciplina_id, curso_id, professor_id, tipo)
            VALUES (?, ?, ?, ?)
        """, (disc_id[0], curso_id[0], prof_id[0], tipo))
        # 2. Buscar carga horária correspondente da disciplina
        if tipo == "Teorica":
            cursor.execute("SELECT carga_teorica FROM disciplinas WHERE id = ?", (disc_id[0],))
        else:
            cursor.execute("SELECT carga_pratica FROM disciplinas WHERE id = ?", (disc_id[0],))

        carga_adicional = cursor.fetchone()[0]

        # 3. Atualizar carga do professor
        cursor.execute("""
            UPDATE professores
            SET carga_horaria = IFNULL(carga_horaria, 0) + ?
            WHERE id = ?
        """, (carga_adicional, prof_id[0]))

        conn.commit()
        st.success("Aula cadastrada com sucesso!")

