# main_redis.py
from utils.redis_client import RedisClient
import json
from collections import defaultdict

# -------------------------------
# Inicialización
# -------------------------------
redis_client = RedisClient()
print("\n--- Conexión a Redis establecida ---\n")

# Limpiar BD

redis_client.flushdb

# -------------------------------
# 1. Crear registros clave-valor
# Redis permite acceso rápido a datos individuales ideal para guardar información frecuente.
# -------------------------------
# redis_client.set("student:101:name", "Laura Gómez")
# redis_client.set("student:101:hours", 35)
# redis_client.set("student:102:name", "Carlos M.")
# redis_client.set("student:102:hours", 40)
# redis_client.set("student:103:name", "Ana P.")
# redis_client.set("student:103:hours", 30)

redis_client.set("student:101",  {
    "id_estudiante": 101,
    "dni": "12345678A",
    "nombre": "Laura Gómez",
    "fecha_nacimiento": "2002-05-10",
    "id_centro": 1,
    "titulacion": "DAW",
    "curso_academico": "2025",
    "hours": 35
})

redis_client.set("student:102", {
    "id_estudiante": 102,
    "dni": "12345678B",
    "nombre": "Carlos M.",
    "fecha_nacimiento": "2001-08-20",
    "id_centro": 1,
    "titulacion": "DAM",
    "curso_academico": "2025",
    "hours": 40
})

redis_client.set("student:103", {
    "id_estudiante": 103,
    "dni": "12345678C",
    "nombre": "Ana P.",
    "fecha_nacimiento": "2003-02-15",
    "id_centro": 2,
    "titulacion": "DAW",
    "curso_academico": "2025",
    "hours": 30
})
print("1. Crear registros clave-valor\n")
print("Claves creadas: student:101, student:102, student:103\n")

# -------------------------------
# 2. Obtener número de claves
# Permite auditar y verificar la cantidad de registros almacenados.
# -------------------------------
print("2. Obtener número de claves\n")
all_keys = redis_client.keys("*")
print(f"Total de claves: {len(all_keys)}\n")

# -------------------------------
# 3. Obtener un registro por clave
# Recuperar rápidamente datos de un estudiante concreto usando la clave.
# -------------------------------
print("3. Obtener un registro por clave\n")
value = redis_client.get("student:101:name")
print(f"Valor: {value}\n")

# -------------------------------
# 4. Actualizar valor de una clave
# Redis permite modificar valores existentes de forma inmediata.
# -------------------------------
print("4. Actualizar valor de una clave\n")
redis_client.set("student:101:name", "Laura G.")
new_value = redis_client.get("student:101:name")
print(f"Nuevo valor: {new_value}\n")

# -------------------------------
# 5. Eliminar una clave-valor
# Limpieza de datos obsoletos o irrelevantes.
# -------------------------------
print("5. Eliminar una clave-valor\n")
deleted_value = redis_client.delete("student:103:name")
print(f"Clave eliminada: student:103:name, valor eliminado: {deleted_value}\n")

# -------------------------------
# 6. Mostrar todas las claves
# Útil para inspección y debugging.
# -------------------------------
print("6. Mostrar todas las claves\n")
all_keys = redis_client.keys("*")
print(f"{all_keys}, \n")

# -------------------------------
# 7. Mostrar todos los valores
# Permite obtener datos completos para análisis o informes.
# -------------------------------
print("7. Mostrar todos los valores\n")
string_keys = [k for k in redis_client.keys("*") if redis_client.type(k) == "string"]
all_values = redis_client.mget(string_keys)
print(f"{all_values}, \n")

# -------------------------------
# 8. Obtener varios registros con patrón *
# Búsqueda por patrón de clave, útil para manejar grupos de datos relacionados.
# -------------------------------
print("8. Obtener varios registros con patrón *\n")
keys_pattern = redis_client.keys("student:101:*")
keys_string = [k for k in keys_pattern if redis_client.type(k) == "string"]
values_pattern = redis_client.mget(keys_string)
print(f"Claves: {keys_string}\nValores: {values_pattern}\n")

# -------------------------------
# 9. Obtener varios registros con patrón []
# Filtrar subconjuntos exactos de datos sin recorrer todo el dataset.
# -------------------------------
print("9. Obtener varios registros con patrón []\n")
keys_pattern = redis_client.keys("student:10[1-2]:name")
values_pattern = redis_client.mget(keys_pattern)
print(f"Claves: {keys_pattern}\nValores: {values_pattern}\n")

# -------------------------------
# 10. Obtener varios registros con patrón ?
# Búsquedas flexibles y precisas en claves.
# -------------------------------
print("10. Obtener varios registros con patrón ?\n")
keys_pattern = redis_client.keys("student:10?:hours")
values_pattern = redis_client.mget(keys_pattern)
print(f"Claves: {keys_pattern}\nValores: {values_pattern}\n")

# -------------------------------
# 11. Filtrar registros por valor
# Consultas rápidas en memoria, ejemplo: estudiantes con ≥35 horas.
# -------------------------------
print("11. Filtrar registros por valor\n")
keys_hours = redis_client.keys("student:*:hours")
filtered_students = []
for k in keys_hours:
    v = int(redis_client.get(k))
    if v >= 35:
        filtered_students.append((k, v))
print(f"{filtered_students}, \n")

# -------------------------------
# 12. Actualizar varios registros por filtro
# Redis permite operaciones masivas eficientes, como incrementar horas para ciertos estudiantes.
# -------------------------------
print("12: Actualizar varios registros por filtro\n")
for k, v in filtered_students:
    if v < 40:
        redis_client.set(k, v + 1)
updated_values = [(k, redis_client.get(k)) for k, v in filtered_students]
print(f"12. {updated_values}, \n")

# -------------------------------
# 13. Eliminar registros por filtro
# Limpieza selectiva de registros que cumplen condiciones específicas.
# -------------------------------
print("13: Eliminar registros por filtro\n")
student_keys = [k for k in redis_client.keys("student:*") if redis_client.type(k) == "string"]

for k in student_keys:
    student = redis_client.get(k)
    if isinstance(student, str):
        try:
            student = json.loads(student)
        except:
            continue  # si no es JSON válido, saltar

    if isinstance(student, dict) and student.get("hours", 0) <= 36:
        deleted = redis_client.delete(k)
        print(f"Eliminado {k}: {deleted}")
print("")

# -------------------------------
# 14. Crear estructura JSON
# Guardar objetos complejos en Redis para consultas ricas sin desnormalizar.
# -------------------------------
print("14. Crear estructura JSON\n")
students_json = [
    {"id":101, "nombre":"Laura G.", "curso":"DAW", "hours":36},
    {"id":102, "nombre":"Carlos M.", "curso":"DAM", "hours":41}
]
redis_client.delete("students")
redis_client.set("students", students_json)
print("JSON guardado en Redis\n")

# -------------------------------
# 15. Filtrar JSON por atributo
# Consultas basadas en atributos internos sin SQL.
# -------------------------------
print("15. Filtrar JSON por atributo\n")
stored_students = redis_client.get("students")
filtered = [s for s in stored_students if s["curso"]=="DAW"]
print(f"{filtered}, \n")

# -------------------------------
# 16. Crear lista en Redis
# Redis maneja listas ordenadas (queues, logs, actividades) eficientemente.
# -------------------------------
print("16. Crear lista en Redis\n")
redis_client.rpush("student:101:activities", "Entrega informe 1", "Sesion tutoría")

# -------------------------------
# 17. Obtener elementos de lista con filtro
# Buscar elementos dentro de la lista, útil para dashboards o notificaciones.
# -------------------------------
print("17. Obtener elementos de lista con filtro\n")
activities = redis_client.lrange("student:101:activities")
filtered_activities = [a for a in activities if "informe" in a]
print(f"{filtered_activities}, \n")

# -------------------------------
# 18. Crear datos con índices (JSON)
# Guardar con índice único facilita búsquedas rápidas por id.
# -------------------------------
print("18. Crear datos con índices (JSON)\n")
redis_client.delete("student:104")
student_104 = {"id":104, "nombre":"Marta L.", "hours":25}
redis_client.set("student:104", student_104)
print("JSON con índice creado\n")

# -------------------------------
# 19. Buscar por índice (nombre)
# Redis no tiene índices secundarios nativos, pero se puede filtrar por valor para simular búsquedas.
# -------------------------------
print("19. Buscar por índice (nombre)\n")
keys_student = redis_client.keys("student:*")
keys_string = [k for k in keys_student if redis_client.type(k) == "string"]
found = []
for k in keys_string:
    val = redis_client.get(k)
    if val == "Carlos M.":
        found.append((k,val))
print(found, "\n")

# -------------------------------
# 20. Group by usando índice (curso)
# Agrupar objetos JSON por atributo permite análisis tipo "reporting" directamente en memoria.
# -------------------------------
print("20. Group by usando índice (curso)\n")
students_all = redis_client.get("students")
grouped = defaultdict(list)
for s in students_all:
    grouped[s["curso"]].append(s)
for curso, lista in grouped.items():
    print(f"Curso {curso}: {lista}")

print("\n--- Fin de ejecución de funcionalidades 1-20 ---")
