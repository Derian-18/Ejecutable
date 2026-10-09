class Alumnos:
    def __init__(self, nombre, matricula):
        self.nombre = nombre
        self.matricula = matricula

class Cursos:
    def __init__(self, nombreCurso, prioridad):
        self.nombreCurso = nombreCurso
        self.prioridad = prioridad

class Inscripciones:
    def __init__(self, alumno_id, curso_id):
        self.alumno_id = alumno_id
        self.curso_id = curso_id
