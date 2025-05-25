import sqlite3

def conectar():
    return sqlite3.connect("database.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            titulacao TEXT CHECK (titulacao IN ('Licenciado', 'Mestre', 'Doutor')) NOT NULL,
            carga_max INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            carga_total INTEGER NOT NULL,
            teorica INTEGER NOT NULL,
            pratica INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS atribuicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina_id INTEGER NOT NULL,
            curso_id INTEGER NOT NULL,
            professor_teorico_id INTEGER,
            professor_pratico_id INTEGER,
            compartilhada_teorica BOOLEAN DEFAULT 0,
            FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id),
            FOREIGN KEY (curso_id) REFERENCES cursos (id),
            FOREIGN KEY (professor_teorico_id) REFERENCES professores (id),
            FOREIGN KEY (professor_pratico_id) REFERENCES professores (id)
        )
    ''')
    conn.commit()
    conn.close()
