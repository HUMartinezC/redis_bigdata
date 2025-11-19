# cargar_datos_mysql.py
from utils.redis_client import RedisClient
from utils.sql_client import SQLClient

# Conexión a Redis
rdb = RedisClient()

# Conexión a MySQL
sql = SQLClient(host="localhost", user="root", password="root", database="gestion_practicas")

# --------------------------
# 1. Centros Educativos
# --------------------------
centros = sql.fetchall("SELECT id_centro, nombre, provincia, tipo_centro FROM CENTROS_EDUCATIVOS")
for c in centros:
    key = f"centro:{c['id_centro']}"
    value = {
        "id": c["id_centro"],
        "nombre": c["nombre"],
        "provincia": c["provincia"],
        "tipo": c["tipo_centro"]
    }
    rdb.set(key, value)

# --------------------------
# 2. Estudiantes
# --------------------------
estudiantes = sql.fetchall("""SELECT id_estudiante, nombre, dni, correo, id_centro, titulacion, curso_academico
                              FROM ESTUDIANTES""")
for s in estudiantes:
    key = f"estudiante:{s['id_estudiante']}"
    value = {
        "id": s["id_estudiante"],
        "nombre": s["nombre"],
        "dni": s["dni"],
        "correo": s["correo"],
        "centro_id": s["id_centro"],
        "titulacion": s["titulacion"],
        "curso": s["curso_academico"]
    }
    rdb.set(key, value)

# --------------------------
# 3. Tutores
# --------------------------
tutores = sql.fetchall("""SELECT id_tutor, nombre, correo, id_centro, especialidad
                          FROM TUTORES""")
for t in tutores:
    key = f"tutor:{t['id_tutor']}"
    value = {
        "id": t["id_tutor"],
        "nombre": t["nombre"],
        "correo": t["correo"],
        "centro_id": t["id_centro"],
        "especialidad": t["especialidad"]
    }
    rdb.set(key, value)

# --------------------------
# 4. Empresas
# --------------------------
empresas = sql.fetchall("SELECT id_empresa, nombre, sector, ciudad, satisfaccion_media FROM EMPRESAS")
for e in empresas:
    key = f"empresa:{e['id_empresa']}"
    value = {
        "id": e["id_empresa"],
        "nombre": e["nombre"],
        "sector": e["sector"],
        "ciudad": e["ciudad"],
        "satisfaccion": float(e["satisfaccion_media"] or 0)
    }
    rdb.set(key, value)

# --------------------------
# 5. Prácticas
# --------------------------
practicas = sql.fetchall("""SELECT id_practica, id_estudiante, id_tutor, id_empresa, id_convenio,
                                   fecha_inicio, fecha_fin, estado, evaluacion_final
                            FROM PRACTICAS""")
for p in practicas:
    key = f"practica:{p['id_practica']}"
    value = {
        "id": p["id_practica"],
        "estudiante_id": p["id_estudiante"],
        "tutor_id": p["id_tutor"],
        "empresa_id": p["id_empresa"],
        "convenio_id": p["id_convenio"],
        "fecha_inicio": str(p["fecha_inicio"]),
        "fecha_fin": str(p["fecha_fin"]),
        "estado": p["estado"],
        "evaluacion_final": float(p["evaluacion_final"] or 0)
    }
    rdb.set(key, value)

# --------------------------
# 6. Convenios
# --------------------------
convenios = sql.fetchall("""SELECT id_convenio, id_empresa, id_centro, fecha_inicio, fecha_fin
                            FROM CONVENIOS""")
for c in convenios:
    key = f"convenio:{c['id_convenio']}"
    value = {
        "id": c["id_convenio"],
        "empresa_id": c["id_empresa"],
        "centro_id": c["id_centro"],
        "fecha_inicio": str(c["fecha_inicio"]),
        "fecha_fin": str(c["fecha_fin"])
    }
    rdb.set(key, value)

# --------------------------
# 7. Actividades, Evaluaciones e Incidencias (listas por práctica)
# --------------------------
actividades = sql.fetchall("SELECT id_practica, fecha, descripcion, horas, validado_por_tutor FROM REGISTROS_ACTIVIDAD")
for a in actividades:
    key = f"actividad:{a['id_practica']}"
    rdb.rpush(key, {
        "fecha": str(a["fecha"]),
        "descripcion": a["descripcion"],
        "horas": a["horas"],
        "validado": a["validado_por_tutor"]
    })

evaluaciones = sql.fetchall("SELECT id_practica, tipo, fecha, puntuacion, comentarios FROM EVALUACIONES")
for e in evaluaciones:
    key = f"evaluacion:{e['id_practica']}"
    rdb.rpush(key, {
        "tipo": e["tipo"],
        "fecha": str(e["fecha"]),
        "puntuacion": float(e["puntuacion"] or 0),
        "comentarios": e["comentarios"]
    })

incidencias = sql.fetchall("SELECT id_practica, fecha, descripcion, tipo, resuelta FROM INCIDENCIAS")
for i in incidencias:
    key = f"incidencia:{i['id_practica']}"
    rdb.rpush(key, {
        "fecha": str(i["fecha"]),
        "descripcion": i["descripcion"],
        "tipo": i["tipo"],
        "resuelta": i["resuelta"]
    })

print("Datos cargados correctamente en Redis ✅")
sql.close()
