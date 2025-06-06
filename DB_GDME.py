import sqlite3
import streamlit as st


def conectar_db():
    return sqlite3.connect("Dados_GDME.db", check_same_thread=False)

def criar_tabela_professores():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            codigo TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            grau TEXT NOT NULL,
            email TEXT,
            resumo TEXT,
            foto TEXT 
        );
    """)
    conn.commit()
    conn.close()

def cadastrar_professor(codigo, nome, grau, email, resumo, foto):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO professores (codigo, nome, grau, email, resumo, foto) VALUES (?, ?, ?, ?, ?, ?)", (codigo, nome, grau, email, resumo))
        conn.commit()
        st.success("Professor cadastrado.")
    except:
        st.error("Erro: código já existe.")
    conn.close()

def listar_professores():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nome, grau, email, resumo, foto FROM professores")
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_professor(codigo, nome, grau, email, resumo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE professores
        SET nome = ?, grau = ?, email = ?, resumo = ?
        WHERE codigo = ?
    """, (nome, grau, email, resumo, codigo))
    conn.commit()
    conn.close()

def buscar_professores(termo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nome, grau, email, resumo FROM professores WHERE nome LIKE ? OR codigo LIKE ?", (f"%{termo}%", f"%{termo}%"))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def remover_professor(codigo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM professores WHERE codigo = ?", (codigo,))
    conn.commit()
    conn.close()

# FUNÇÕES DE DISCIPLINAS

def criar_tabela_disciplinas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            codigo TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            horas_teoricas INTEGER,
            horas_praticas INTEGER
        );
    """)
    conn.commit()
    conn.close()

def cadastrar_disciplina(codigo, nome, horas_teoricas, horas_praticas):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO disciplinas (codigo, nome, horas_teoricas, horas_praticas) VALUES (?, ?, ?, ?)",
            (codigo, nome, horas_teoricas, horas_praticas)
        )
        conn.commit()
        st.success("Disciplina cadastrada com sucesso.")
    except sqlite3.IntegrityError:
        st.error("Erro: código já existe.")
    conn.close()

def listar_disciplinas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nome, horas_teoricas, horas_praticas FROM disciplinas")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def buscar_disciplinas(termo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disciplinas WHERE nome LIKE ? OR codigo LIKE ?", (f"%{termo}%", f"%{termo}%"))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def atualizar_disciplina(codigo, nome, horas_teoricas, horas_praticas):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE disciplinas SET nome = ?, horas_teoricas = ?, horas_praticas = ? WHERE codigo = ?",
        (nome, horas_teoricas, horas_praticas, codigo)
    )
    conn.commit()
    conn.close()

def remover_disciplina(codigo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM disciplinas WHERE codigo = ?", (codigo,))
    conn.commit()
    conn.close()

# FUNÇÕES PARA CURSO

def criar_tabela_cursos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cursos (
            codigo TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            nivel TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def cadastrar_curso(codigo, nome, nivel):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cursos (codigo, nome, nivel) VALUES (?, ?, ?)", (codigo, nome, nivel))
        conn.commit()
        st.success("Curso cadastrado com sucesso.")
    except sqlite3.IntegrityError:
        st.error("Erro: código já existe.")
    conn.close()

def listar_cursos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nome, nivel FROM cursos")
    dados = cursor.fetchall()
    conn.close()
    return dados

def buscar_cursos(termo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cursos WHERE nome LIKE ? OR codigo LIKE ?", (f"%{termo}%", f"%{termo}%"))
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_curso(codigo, nome, nivel):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cursos SET nome = ?, nivel = ? WHERE codigo = ?", (nome, nivel, codigo))
    conn.commit()
    conn.close()

def remover_curso(codigo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cursos WHERE codigo = ?", (codigo,))
    conn.commit()
    conn.close()

# FUNÇÕES PARA AULAS

def criar_tabela_aulas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professor_codigo TEXT NOT NULL,
            disciplina_codigo TEXT NOT NULL,
            curso_codigo TEXT NOT NULL,
            tipo TEXT CHECK(tipo IN ('teorica', 'pratica')) NOT NULL,
            UNIQUE (disciplina_codigo, curso_codigo, tipo),
            FOREIGN KEY (professor_codigo) REFERENCES professores(codigo),
            FOREIGN KEY (disciplina_codigo) REFERENCES disciplinas(codigo),
            FOREIGN KEY (curso_codigo) REFERENCES cursos(codigo)
        );
    """)
    conn.commit()
    conn.close()

def cadastrar_aula(professor, disciplina, curso, tipo):
    conn = conectar_db()
    cursor = conn.cursor()

    # Verifica se já existe uma aula com mesmo disciplina/curso/tipo
    cursor.execute("""
        SELECT * FROM aulas
        WHERE disciplina_codigo = ? AND curso_codigo = ? AND tipo = ?
    """, (disciplina, curso, tipo))
    existente = cursor.fetchone()

    if existente:
        st.error(f"Já existe uma aula {tipo} dessa disciplina nesse curso.")
    else:
        cursor.execute("""
            INSERT INTO aulas (professor_codigo, disciplina_codigo, curso_codigo, tipo)
            VALUES (?, ?, ?, ?)
        """, (professor, disciplina, curso, tipo))
        conn.commit()
        st.success("Aula cadastrada com sucesso.")

    conn.close()

def listar_aulas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, p.nome, d.nome, c.nome, a.tipo
        FROM aulas a
        JOIN professores p ON a.professor_codigo = p.codigo
        JOIN disciplinas d ON a.disciplina_codigo = d.codigo
        JOIN cursos c ON a.curso_codigo = c.codigo
        ORDER BY c.nome, d.nome, a.tipo
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado
