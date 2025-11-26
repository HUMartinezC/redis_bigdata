# redis_mysql_sync.py

from utils.redis_client import RedisClient
from utils.sql_client import SQLClient
from datetime import date
import json

# -------------------------------
# Inicialización
# -------------------------------
redis_client = RedisClient()
sql = SQLClient(
    host="localhost", user="root", password="root", database="gestion_practicas"
)

# -------------------------------
# 21. Obtener datos de MySQL e incluirlos en Redis
# -------------------------------
print("21. Traer estudiantes de MySQL e insertar en Redis \n")

students = sql.fetchall(
    """
    SELECT id_estudiante, dni, nombre, fecha_nacimiento, correo, telefono, nacionalidad,
           id_centro, titulacion, curso_academico
    FROM ESTUDIANTES
    LIMIT 5
"""
)

for s in students:
    key = f"student:{s['id_estudiante']}"
    value = {
        "id_estudiante": s["id_estudiante"],
        "dni": s["dni"],
        "nombre": s["nombre"],
        "fecha_nacimiento": s["fecha_nacimiento"].isoformat(),
        "correo": s.get("correo"),
        "telefono": s.get("telefono"),
        "nacionalidad": s.get("nacionalidad"),
        "id_centro": s["id_centro"],
        "titulacion": s.get("titulacion"),
        "curso_academico": s.get("curso_academico"),
    }
    redis_client.set(key, value)
    print(f"Guardado en Redis -> {key}: {value}")

# -------------------------------
# 22. Leer datos de Redis e insertar/actualizar en MySQL
# -------------------------------
print("\n22. Leer estudiantes de Redis e insertar/actualizar en MySQL\n")

student_keys = [k for k in redis_client.keys("student:*") 
                if redis_client.type(k) == "string" and ":" not in k.split(":", 1)[1]]


for key in student_keys:
    student = redis_client.get(key)
    
    # Solo parsear si es string
    if isinstance(student, str):
        try:
            student = json.loads(student)
        except json.JSONDecodeError:
            print(f"[WARN] No se pudo parsear JSON de la clave {key}: {student}")
            continue

    # Asegurarse de que si es string JSON se convierta a dict
    # if isinstance(student, str):
    #     student = json.loads(student)

    # Validación mínima para campos obligatorios
    required_fields = ["id_estudiante", "dni", "nombre", "fecha_nacimiento", "id_centro", "titulacion", "curso_academico"]
    if not all(field in student and student[field] is not None for field in required_fields):
        print(f"[WARN] Datos incompletos en {key}, se omite: {student}")
        continue

    sql.execute("""
        INSERT INTO ESTUDIANTES (
            id_estudiante, dni, nombre, fecha_nacimiento, id_centro, titulacion, curso_academico
        ) VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            dni=%s, nombre=%s, fecha_nacimiento=%s, id_centro=%s, titulacion=%s, curso_academico=%s
    """, (
        student["id_estudiante"],
        student["dni"],
        student["nombre"],
        student["fecha_nacimiento"],
        student["id_centro"],
        student["titulacion"],
        student["curso_academico"],
        student["dni"],
        student["nombre"],
        student["fecha_nacimiento"],
        student["id_centro"],
        student["titulacion"],
        student["curso_academico"]
    ))

    print(f"Insertado/Actualizado en MySQL -> id: {student['id_estudiante']}, nombre: {student['nombre']}, curso: {student['curso_academico']}")


print("\n--- Sincronización Redis <-> MySQL completada ---\n")

# Cerrar conexión
sql.close()
