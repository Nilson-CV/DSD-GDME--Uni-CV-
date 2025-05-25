-- Criação das tabelas principais
CREATE TABLE IF NOT EXISTS professores (
    codigo TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    grau TEXT CHECK (grau IN ('Licenciado', 'Mestre', 'Doutor')) NOT NULL,
    carga_horaria INTEGER NOT NULL
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
CREATE TABLE IF NOT EXISTS aulas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disciplina_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    professor_id INTEGER NOT NULL,
    tipo TEXT CHECK (tipo IN ('Teorica', 'Pratica')) NOT NULL,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id),
    FOREIGN KEY (professor_id) REFERENCES professores(id)
);

-- Trigger: atualiza carga horária ao inserir nova aula
CREATE TRIGGER IF NOT EXISTS atualiza_carga_professor
AFTER INSERT ON aulas
FOR EACH ROW
BEGIN
    UPDATE professores
    SET carga_horaria = IFNULL(carga_horaria, 0) +
        (SELECT CASE NEW.tipo
                WHEN 'Teorica' THEN d.carga_teorica
                WHEN 'Pratica' THEN d.carga_pratica
         END
         FROM disciplinas d
         WHERE d.id = NEW.disciplina_id)
    WHERE id = NEW.professor_id;
END;

-- Trigger: remove carga horária ao excluir aula
CREATE TRIGGER IF NOT EXISTS remover_carga_professor
AFTER DELETE ON aulas
FOR EACH ROW
BEGIN
    UPDATE professores
    SET carga_horaria = IFNULL(carga_horaria, 0) -
        (SELECT CASE OLD.tipo
                WHEN 'Teorica' THEN d.carga_teorica
                WHEN 'Pratica' THEN d.carga_pratica
         END
         FROM disciplinas d
         WHERE d.id = OLD.disciplina_id)
    WHERE id = OLD.professor_id;
END;