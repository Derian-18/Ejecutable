import sqlite3

def conectar_db():
    conn = sqlite3.connect("certificacion.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = conectar_db()

    try:
        cursor = conn.cursor()

        # Tabla Alumnos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                matricula TEXT NOT NULL UNIQUE
            )
        """)

        # Tabla Cursos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombreCurso TEXT NOT NULL,
                prioridad INTEGER NOT NULL
            )
        """)

        # Tabla Inscripciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Inscripciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumno_id INTEGER NOT NULL,
                curso_id INTEGER NOT NULL,
                FOREIGN KEY (alumno_id) REFERENCES Alumnos(id),
                FOREIGN KEY (curso_id) REFERENCES Cursos(id),
                UNIQUE (alumno_id, curso_id)
            )
        """)

        conn.commit()

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()