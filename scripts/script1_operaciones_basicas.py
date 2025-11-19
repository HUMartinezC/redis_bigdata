

from utils.utils import print_json
from utils.redis_client import RedisClient
from utils.sql_client import SQLClient

rdb = RedisClient()
sql = SQLClient(host="localhost", user="root", password="root", database="gestion_practicas")

# ----------------------
# Punto 1: Crear registros clave-valor
# ----------------------
def punto1_crear_registros():
    # Insertamos un estudiante de ejemplo
    key = "estudiante:999"
    value = {
        "id": 999,
        "nombre": "Alumno Ejemplo",
        "dni": "00000000X",
        "correo": "alumno@ejemplo.com",
        "centro_id": 1,
        "titulacion": "FP Desarrollo",
        "curso": "2025"
    }
    rdb.set(key, value)
    print("Punto 1: Registro creado")
    print_json(rdb.get(key))

# ----------------------
# Punto 2: Obtener y mostrar número de claves registradas
# ----------------------
def punto2_numero_claves():
    count = len(rdb.keys("*"))
    print(f"Punto 2: Número de claves en Redis = {count}")

# ----------------------
# Punto 3: Obtener un registro por clave
# ----------------------
def punto3_obtener_por_clave():
    key = "estudiante:999"
    print("Punto 3: Registro obtenido")
    print_json(rdb.get(key))

# ----------------------
# Punto 4: Actualizar valor de una clave y mostrar
# ----------------------
def punto4_actualizar_valor():
    key = "estudiante:999"
    value = rdb.get(key)
    value["correo"] = "nuevo@correo.com"
    rdb.set(key, value)
    print("Punto 4: Registro actualizado")
    print_json(rdb.get(key))

# ----------------------
# Punto 5: Eliminar clave-valor y mostrar
# ----------------------
def punto5_eliminar_clave():
    key = "estudiante:999"
    value = rdb.delete(key)
    print(f"Punto 5: Registro eliminado -> {key}: {value}")

# ----------------------
# Punto 6: Obtener todas las claves
# ----------------------
def punto6_todas_claves():
    keys = rdb.keys("*")
    print("Punto 6: Todas las claves")
    print_json(keys)

# ----------------------
# Punto 7: Obtener todos los valores
# ----------------------
def punto7_todos_valores():
    keys = [k for k in rdb.keys("*") if rdb.type(k) == "string"]
    values = rdb.mget(keys)
    print("Punto 7: Todos los valores")
    print_json(values)

# ----------------------
# Punto 8-10: Obtener registros con patrones
# ----------------------
def punto8_patron_asterisco():
    keys = rdb.keys("estudiante:*")
    print("Punto 8 (*):")
    print_json(rdb.mget(keys))

def punto9_patron_corchetes():
    # Ejemplo: claves estudiante:9[9,8]*
    keys = rdb.keys("estudiante:9[0-9]*")
    print("Punto 9 ([]):")
    print_json(rdb.mget(keys))

def punto10_patron_interrogacion():
    # Ejemplo: estudiante:99?
    keys = rdb.keys("estudiante:99?")
    print("Punto 10 (?):")
    print_json(rdb.mget(keys))

# ----------------------
# Punto 11: Filtrar por valor
# ----------------------
def punto11_filtrar_por_valor():
    keys = rdb.keys("estudiante:*")
    alumnos = [rdb.get(k) for k in keys if rdb.get(k)["centro_id"] == 1]
    print("Punto 11: Filtrados por centro_id=1")
    print_json(alumnos)

# ----------------------
# Punto 12: Actualizar una serie de registros por filtro
# ----------------------
def punto12_actualizar_serie():
    keys = rdb.keys("estudiante:*")
    for k in keys:
        val = rdb.get(k)
        val["curso"] = "2026"
        rdb.set(k, val)
    print("Punto 12: Curso actualizado a 2026")
    punto7_todos_valores()

# ----------------------
# Punto 13: Eliminar serie de registros por filtro
# ----------------------
def punto13_eliminar_serie():
    keys = rdb.keys("estudiante:*")
    for k in keys:
        val = rdb.delete(k)
    print("Punto 13: Serie de registros eliminados")
    punto6_todas_claves()

# ----------------------
# Punto 14: Crear estructura JSON de array de datos
# ----------------------
def punto14_json_array():
    array = []
    keys = rdb.keys("empresa:*")
    for k in keys:
        array.append(rdb.get(k))
    print("Punto 14: JSON array de empresas")
    print_json(array)

# ----------------------
# Punto 15: Filtrar por cada atributo de JSON
# ----------------------
def punto15_filtrar_json():
    array = [rdb.get(k) for k in rdb.keys("empresa:*")]
    filtrado = [e for e in array if e.get("satisfaccion",0) >= 4.0]
    print("Punto 15: Empresas con satisfacción >= 4.0")
    print_json(filtrado)

# ----------------------
# Punto 16: Crear una lista en Redis
# ----------------------
def punto16_lista_redis():
    rdb.rpush("practicas:pendientes", "practica:1", "practica:2")
    print("Punto 16: Lista de prácticas pendientes creada")
    print_json(rdb.lrange("practicas:pendientes"))

# ----------------------
# Punto 17: Obtener elementos de lista con filtro
# ----------------------
def punto17_lista_filtrada():
    # Obtenemos todos los elementos de la lista "practicas:pendientes"
    lista = rdb.lrange("practicas:pendientes", 0, -1)
    # Filtramos los elementos que contengan '1'
    filtrada = [p for p in lista if "1" in p]
    print("Punto 17: Filtrada lista prácticas con '1'")
    print_json(filtrada)

# ----------------------
# Punto 18: Crear datos con índices (simulado con sets)
# ----------------------
def punto18_datos_indices():
    keys = rdb.keys("estudiante:*")
    if keys:  # solo si hay elementos
        rdb.sadd("set:estudiantes_por_curso:2025", *keys)
    print("Punto 18: Índices por curso 2025 creados")
    miembros = list(rdb.smembers("set:estudiantes_por_curso:2025")) if keys else []
    print_json(miembros)

# ----------------------
# Punto 19: Búsqueda con índices
# ----------------------
def punto19_busqueda_indices():
    # Obtenemos los alumnos del curso 2025 usando el set (índice)
    alumnos = list(rdb.smembers("set:estudiantes_por_curso:2025"))
    print("Punto 19: Alumnos curso 2025 usando índice")
    print_json(alumnos)

# ----------------------
# Punto 20: Group by usando índices
# ----------------------
def punto20_group_by():
    # Agrupamos todos los estudiantes por su centro_id
    keys = rdb.keys("estudiante:*")
    group = {}
    for k in keys:
        val = rdb.get(k)
        if val:  # Verificamos que el valor exista
            cid = val.get("centro_id")
            if cid not in group:
                group[cid] = []
            group[cid].append(val)
    print("Punto 20: Agrupación por centro_id")
    print_json(group)


# ----------------------
# Menú interactivo para probar
# ----------------------
def menu():
    funciones = [
        punto1_crear_registros,
        punto2_numero_claves,
        punto3_obtener_por_clave,
        punto4_actualizar_valor,
        punto5_eliminar_clave,
        punto6_todas_claves,
        punto7_todos_valores,
        punto8_patron_asterisco,
        punto9_patron_corchetes,
        punto10_patron_interrogacion,
        punto11_filtrar_por_valor,
        punto12_actualizar_serie,
        punto13_eliminar_serie,
        punto14_json_array,
        punto15_filtrar_json,
        punto16_lista_redis,
        punto17_lista_filtrada,
        punto18_datos_indices,
        punto19_busqueda_indices,
        punto20_group_by
    ]
    for i, f in enumerate(funciones,1):
        print(f"\n==== Ejecutando Punto {i} ====")
        f()

if __name__ == "__main__":
    menu()
