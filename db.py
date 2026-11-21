import sqlite3

def conectar_db():
    conn = sqlite3.connect("certificacion.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _agregar_columna_activo(cursor, tabla):
    """
    Migración: si la tabla ya existía sin la columna 'activo',
    la agrega. Los registros existentes quedan con activo = 1.
    """
    columnas = [fila[1] for fila in cursor.execute(f"PRAGMA table_info({tabla})")]

    if "activo" not in columnas:
        cursor.execute(
            f"ALTER TABLE {tabla} "
            "ADD COLUMN activo INTEGER NOT NULL DEFAULT 1 "
            "CHECK (activo IN (0, 1))"
        )


def init_db():
    conn = conectar_db()

    try:
        cursor = conn.cursor()

        # Tabla Alumnos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                matricula TEXT NOT NULL UNIQUE,
                activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
            )
        """)

        # Tabla Cursos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombreCurso TEXT NOT NULL,
                creditos INTEGER NOT NULL CHECK (creditos > 0),
                activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
            )
        """)

        # Tabla Inscripciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Inscripciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumno_id INTEGER NOT NULL,
                curso_id INTEGER NOT NULL,
                activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1)),
                FOREIGN KEY (alumno_id) REFERENCES Alumnos(id),
                FOREIGN KEY (curso_id) REFERENCES Cursos(id),
                UNIQUE (alumno_id, curso_id)
            )
        """)

        # Migrar bases de datos creadas antes de agregar 'activo'
        for tabla in ("Alumnos", "Cursos", "Inscripciones"):
            _agregar_columna_activo(cursor, tabla)

        conn.commit()

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()