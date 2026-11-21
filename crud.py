import sqlite3
from db import conectar_db

# -------------------------------------------------------------
# ALUMNOS
# -------------------------------------------------------------

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


def leer_alumnos(activo=1):
    """activo=1 -> alumnos visibles; activo=0 -> alumnos eliminados."""
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            SELECT id, nombre, matricula
            FROM Alumnos
            WHERE activo = ?
            """,
            (activo,)
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
            WHERE id = ? AND activo = 1
            """,
            (nombre, matricula, alumno_id)
        )
        return cursor.rowcount > 0


def eliminar_alumno(alumno_id):
    """Eliminacion logica: UPDATE Alumnos SET activo = 0."""
    with conectar_db() as conn:
        cursor = conn.execute(
            "UPDATE Alumnos SET activo = 0 WHERE id = ? AND activo = 1",
            (alumno_id,)
        )
        return cursor.rowcount > 0


def recuperar_alumno(alumno_id):
    """Recuperacion: UPDATE Alumnos SET activo = 1."""
    with conectar_db() as conn:
        cursor = conn.execute(
            "UPDATE Alumnos SET activo = 1 WHERE id = ? AND activo = 0",
            (alumno_id,)
        )
        return cursor.rowcount > 0


# -------------------------------------------------------------
# CURSOS
# -------------------------------------------------------------

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


def leer_cursos(activo=1):
    """activo=1 -> cursos visibles; activo=0 -> cursos eliminados."""
    with conectar_db() as conn:
        cursor = conn.execute(
            """
            SELECT id, nombreCurso, creditos
            FROM Cursos
            WHERE activo = ?
            """,
            (activo,)
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
            WHERE id = ? AND activo = 1
            """,
            (nombre_curso, creditos, curso_id)
        )
        return cursor.rowcount > 0


def eliminar_curso(curso_id):
    """Eliminacion logica: UPDATE Cursos SET activo = 0."""
    with conectar_db() as conn:
        cursor = conn.execute(
            "UPDATE Cursos SET activo = 0 WHERE id = ? AND activo = 1",
            (curso_id,)
        )
        return cursor.rowcount > 0


def recuperar_curso(curso_id):
    """Recuperacion: UPDATE Cursos SET activo = 1."""
    with conectar_db() as conn:
        cursor = conn.execute(
            "UPDATE Cursos SET activo = 1 WHERE id = ? AND activo = 0",
            (curso_id,)
        )
        return cursor.rowcount > 0


# -------------------------------------------------------------
# INSCRIPCIONES
# -------------------------------------------------------------

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


def leer_inscripciones(activo=1):
    """
    activo=1 -> inscripciones visibles (la inscripcion, el alumno y el
                curso deben estar activos).
    activo=0 -> inscripciones eliminadas.
    """
    with conectar_db() as conn:
        if activo == 1:
            filtro = "i.activo = 1 AND a.activo = 1 AND c.activo = 1"
        else:
            filtro = "i.activo = 0"

        cursor = conn.execute(
            f"""
            SELECT
                i.id,
                a.nombre,
                a.matricula,
                c.nombreCurso,
                c.creditos
            FROM Inscripciones AS i
            JOIN Alumnos AS a ON i.alumno_id = a.id
            JOIN Cursos AS c ON i.curso_id = c.id
            WHERE {filtro}
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
            WHERE id = ? AND activo = 1
            """,
            (alumno_id, curso_id, inscripcion_id)
        )
        return cursor.rowcount > 0


def eliminar_inscripcion(inscripcion_id):
    """Eliminacion logica: UPDATE Inscripciones SET activo = 0."""
    with conectar_db() as conn:
        cursor = conn.execute(
            "UPDATE Inscripciones SET activo = 0 WHERE id = ? AND activo = 1",
            (inscripcion_id,)
        )
        return cursor.rowcount > 0


def recuperar_inscripcion(inscripcion_id):
    """
    Recuperacion: UPDATE Inscripciones SET activo = 1.
    Lanza ValueError si el alumno o el curso de la inscripcion
    estan eliminados (primero hay que recuperarlos).
    """
    with conectar_db() as conn:
        pendiente = conn.execute(
            """
            SELECT a.activo, c.activo
            FROM Inscripciones AS i
            JOIN Alumnos AS a ON i.alumno_id = a.id
            JOIN Cursos AS c ON i.curso_id = c.id
            WHERE i.id = ?
            """,
            (inscripcion_id,)
        ).fetchone()

        if pendiente is None:
            return False

        if pendiente[0] == 0 or pendiente[1] == 0:
            raise ValueError(
                "El alumno o el curso de esta inscripcion esta eliminado. "
                "Recuperalo primero."
            )

        cursor = conn.execute(
            "UPDATE Inscripciones SET activo = 1 WHERE id = ? AND activo = 0",
            (inscripcion_id,)
        )
        return cursor.rowcount > 0