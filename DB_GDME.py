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
        cursor.execute("INSERT INTO professores (codigo, nome, grau, email, resumo, foto) VALUES (?, ?, ?, ?, ?, ?)", (codigo, nome, grau, email, resumo, foto))
        conn.commit()
        st.success("Professor cadastrado.")
    except:
        st.error("Erro: código já existe.")
    conn.close()

def gerar_proximo_codigo_professor():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo FROM professores WHERE codigo LIKE 'PME%' ORDER BY codigo DESC LIMIT 1")
    ultimo = cursor.fetchone()
    conn.close()

    if ultimo:
        num = int(ultimo[0][3:]) + 1  # extrai o número após "PME" e incrementa
    else:
        num = 1

    return f"PME{num:02d}"  # garante dois dígitos com zero à esquerda


def listar_professores():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nome, grau, email, resumo, foto FROM professores")
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_professor(codigo, nome, grau, email, resumo, foto=None):
    conn = conectar_db()
    cursor = conn.cursor()
    if foto:
        cursor.execute("""
            UPDATE professores
            SET nome = ?, grau = ?, email = ?, resumo = ?, foto = ?
            WHERE codigo = ?
        """, (nome, grau, email, resumo, foto, codigo))
    else:
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
            semestre TEXT NOT NULL,
            horas_teoricas INTEGER,
            horas_praticas INTEGER
        );
    """)
    conn.commit()
    conn.close()


def cadastrar_disciplina(codigo, nome, semestre, horas_teoricas, horas_praticas):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO disciplinas (codigo, nome, semestre, horas_teoricas, horas_praticas) VALUES (?, ?, ?, ?, ?)",
            (codigo, nome, semestre, horas_teoricas, horas_praticas)
        )
        conn.commit()
        st.success("Disciplina cadastrada com sucesso.")
    except sqlite3.IntegrityError:
        st.error("Erro: código já existe.")
    conn.close()

def listar_disciplinas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nome, semestre, horas_teoricas, horas_praticas FROM disciplinas")
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

def atualizar_disciplina(codigo, nome, semestre, horas_teoricas, horas_praticas):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE disciplinas SET nome = ?, semestre = ?, horas_teoricas = ?, horas_praticas = ? WHERE codigo = ?",
        (nome, semestre, horas_teoricas, horas_praticas, codigo)
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
            tipo TEXT CHECK(tipo IN ('teorica', 'pratica')) NOT NULL,
            horas INTEGER NOT NULL,
            sala TEXT,
            horario_inicio TEXT, -- Ex: '14:00'
            FOREIGN KEY (professor_codigo) REFERENCES professores(codigo),
            FOREIGN KEY (disciplina_codigo) REFERENCES disciplinas(codigo)
        );
    """)
    conn.commit()
    conn.close()

def criar_tabela_aulas_cursos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aulas_cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aula INTEGER NOT NULL,
            curso_codigo TEXT NOT NULL,
            semestre TEXT,
            FOREIGN KEY (id_aula) REFERENCES aulas(id),
            FOREIGN KEY (curso_codigo) REFERENCES cursos(codigo)
        );
    """)
    conn.commit()
    conn.close()

def inserir_aula(professor, disciplina, tipo, horas, sala, horario_inicio, cursos_semestres):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO aulas (professor_codigo, disciplina_codigo, tipo, horas, sala, horario_inicio)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (professor, disciplina, tipo, horas, sala, horario_inicio))
    id_aula = cursor.lastrowid

    for curso, semestre in cursos_semestres:
        cursor.execute("""
            INSERT INTO aulas_cursos (id_aula, curso_codigo, semestre)
            VALUES (?, ?, ?)
        """, (id_aula, curso, semestre))

    conn.commit()
    conn.close()

def buscar_aulas_por_professor(cod_prof):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            a.id, d.nome, a.tipo, a.horas, a.sala, a.horario_inicio,
            d.codigo, a.disciplina_codigo, a.dia_semana
        FROM aulas a
        JOIN disciplinas d ON a.disciplina_codigo = d.codigo
        WHERE a.professor_codigo = ?
        ORDER BY d.nome
    """, (cod_prof,))
    aulas = cursor.fetchall()

    dados_finais = []
    for aula in aulas:
        id_aula = aula[0]
        cursor.execute("""
            SELECT c.nome, ac.semestre 
            FROM aulas_cursos ac
            JOIN cursos c ON ac.curso_codigo = c.codigo
            WHERE ac.id_aula = ?
        """, (id_aula,))
        cursos = cursor.fetchall()
        dados_finais.append({
            "disciplina": aula[1],
            "tipo": aula[2],
            "horas": aula[3],
            "sala": aula[4],
            "horario_inicio": aula[5],
            "disciplina_codigo": aula[6],
            "dia_semana": aula[7],
            "cursos": cursos
        })
    conn.close()
    return dados_finais

def atualizar_aula(id_aula, tipo, horas, sala, horario_inicio, dia_semana):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE aulas
        SET tipo=?, horas=?, sala=?, horario_inicio=?, dia_semana=?
        WHERE id=?
    """, (tipo, horas, sala, horario_inicio, dia_semana, id_aula))
    conn.commit()
    conn.close()

def remover_aula(id_aula):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM aulas_cursos WHERE id_aula=?", (id_aula,))
    cursor.execute("DELETE FROM aulas WHERE id=?", (id_aula,))
    conn.commit()
    conn.close()

def atualizar_cursos_aula(id_aula, cursos_semestres):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM aulas_cursos WHERE id_aula=?", (id_aula,))
    for curso_codigo, semestre in cursos_semestres:
        cursor.execute("""
            INSERT INTO aulas_cursos (id_aula, curso_codigo, semestre)
            VALUES (?, ?, ?)
        """, (id_aula, curso_codigo, semestre))
    conn.commit()
    conn.close()











