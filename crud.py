import sqlite3
from db import conectar_db

def crear_alumno(nombre, matricula):
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO Alumnos (nombre, matricula)
            VALUES (?, ?)
            """,
            (nombre, matricula)
        )
        return cursor.lastrowid


def leer_alumnos():
    with conectar_db() as conn:
        cursor = conn.execute(
            "SELECT id, nombre, matricula FROM Alumnos"
        )
        return cursor.fetchall()


def leer_alumno(alumno_id):
    with conectar_db() as conn:
        cursor = conn.execute(
            "SELECT id, nombre, matricula FROM Alumnos WHERE id = ?",
            (alumno_id,)
        )
        return cursor.fetchone()


def actualizar_alumno(alumno_id, nombre, matricula):
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            UPDATE Alumnos
            SET nombre = ?, matricula = ?
            WHERE id = ?
            """,
            (nombre, matricula, alumno_id)
        )
        return cursor.rowcount > 0


def eliminar_alumno(alumno_id):
    with conectar_db() as conn:
        cursor = conn.execute(
            "DELETE FROM Alumnos WHERE id = ?",
            (alumno_id,)
        )
        return cursor.rowcount > 0

def crear_curso(nombre_curso, creditos):
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO Cursos (nombreCurso, creditos)
            VALUES (?, ?)
            """,
            (nombre_curso, creditos)
        )
        return cursor.lastrowid


def leer_cursos():
    with conectar_db() as conn:
        cursor = conn.execute(
            "SELECT id, nombreCurso, creditos FROM Cursos"
        )
        return cursor.fetchall()


def leer_curso(curso_id):
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            SELECT id, nombreCurso, creditos
            FROM Cursos
            WHERE id = ?
            """,
            (curso_id,)
        )
        return cursor.fetchone()


def actualizar_curso(curso_id, nombre_curso, creditos):
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            UPDATE Cursos
            SET nombreCurso = ?, creditos = ?
            WHERE id = ?
            """,
            (nombre_curso, creditos, curso_id)
        )
        return cursor.rowcount > 0


def eliminar_curso(curso_id):
    with conectar_db() as conn:
        cursor = conn.execute(
            "DELETE FROM Cursos WHERE id = ?",
            (curso_id,)
        )
        return cursor.rowcount > 0


def crear_inscripcion(alumno_id, curso_id):
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO Inscripciones (alumno_id, curso_id)
            VALUES (?, ?)
            """,
            (alumno_id, curso_id)
        )
        return cursor.lastrowid


def leer_inscripciones():
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            SELECT
                i.id,
                a.nombre,
                a.matricula,
                c.nombreCurso,
                c.creditos
            FROM Inscripciones AS i
            JOIN Alumnos AS a ON i.alumno_id = a.id
            JOIN Cursos AS c ON i.curso_id = c.id
            ORDER BY i.id
            """
        )
        return cursor.fetchall()


def leer_inscripcion(inscripcion_id):
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            SELECT id, alumno_id, curso_id
            FROM Inscripciones
            WHERE id = ?
            """,
            (inscripcion_id,)
        )
        return cursor.fetchone()


def actualizar_inscripcion(inscripcion_id, alumno_id, curso_id):
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            UPDATE Inscripciones
            SET alumno_id = ?, curso_id = ?
            WHERE id = ?
            """,
            (alumno_id, curso_id, inscripcion_id)
        )
        return cursor.rowcount > 0


def eliminar_inscripcion(inscripcion_id):
    with conectar_db() as conn:
        cursor = conn.execute(
            "DELETE FROM Inscripciones WHERE id = ?",
            (inscripcion_id,)
        )
        return cursor.rowcount > 0