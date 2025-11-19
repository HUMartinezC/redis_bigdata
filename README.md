# Redis - Plataforma de Gestión y Análisis de Prácticas Formativas

Proyecto académico para el curso de IA y Big Data que implementa operaciones con Redis en el contexto de una plataforma de gestión y análisis de prácticas formativas.

## Descripción

Este proyecto contiene una aplicación en Python que implementa 22 operaciones diferentes con Redis, cubriendo desde operaciones básicas de clave-valor hasta funcionalidades avanzadas con JSON, listas, búsqueda y sincronización con bases de datos relacionales.

## Estructura del Proyecto

```
redis/
├── README.md                 # Este archivo
├── requirements.txt          # Dependencias del proyecto
├── scripts/
│   └── script_1.py          # Aplicación principal con todas las operaciones
└── redis/                   # Entorno virtual Python
```

## Requisitos

- Python 3.7+
- Redis Server
- Librerías Python:
  - `redis` (cliente oficial de Redis)
  - Opcional: RedisJSON y RediSearch (si están disponibles en el servidor)

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd redis
```

2. Crear y activar entorno virtual:
```bash
python -m venv redis
source redis/Scripts/activate  # Windows
# o
source redis/bin/activate      # Linux/Mac
```

3. Instalar dependencias:
```bash
pip install redis
```

## Uso

Ejecutar aplicaciones:
```bash
python scripts/script1_operaciones_basicas.py
```

## TODO: (Opcional/Útil?) La aplicación presenta un menú interactivo que permite probar cada una de las 22 operaciones implementadas.

## Datos almacenados en Redis

Para este proyecto, se eligieron las siguientes entidades y campos de la base de datos gestion_practicas para operar en Redis:

| Entidad/Tabla | Clave Redis | Estructura/JSON almacenado | Comentario |
|---------------|-------------|----------------------------|------------|
| Centros Educativos | `centro:{id_centro}` | `{"id":..., "nombre":..., "provincia":..., "tipo":...}` | Permite filtrar por provincia o tipo de centro |
| Estudiantes | `estudiante:{id_estudiante}` | `{"id":..., "nombre":..., "dni":..., "correo":..., "centro_id":..., "titulacion":..., "curso":...}` | Búsquedas rápidas por estudiante o filtrado por centro/titulación |
| Tutores | `tutor:{id_tutor}` | `{"id":..., "nombre":..., "correo":..., "telefono":..., "centro_id":..., "especialidad":...}` | Acceso rápido para asignar tutor a práctica |
| Empresas | `empresa:{id_empresa}` | `{"id":..., "nombre":..., "sector":..., "ciudad":..., "satisfaccion":...}` | Dashboard de satisfacción y recomendaciones |
| Prácticas | `practica:{id_practica}` | `{"id":..., "estudiante_id":..., "tutor_id":..., "empresa_id":..., "convenio_id":..., "fecha_inicio":..., "fecha_fin":..., "estado":..., "evaluacion_final":...}` | Seguimiento de estado y evaluación final |
| Convenios | `convenio:{id_convenio}` | `{"id":..., "empresa_id":..., "centro_id":..., "fecha_inicio":..., "fecha_fin":...}` | Consultas rápidas por empresa o centro |
| Registros de actividad / Evaluaciones / Incidencias | `actividad:{id_practica}`, `evaluacion:{id_practica}`, `incidencia:{id_practica}` | Listas o sets con los elementos asociados a cada práctica | Permite filtrar por práctica o tipo de incidencia |

Notas:

 - Las claves siguen un patrón {entidad}:{id} para facilitar búsquedas, filtrados y agrupaciones en Redis.

 - Se usan estructuras JSON para almacenar metadatos relevantes y listas/sets para datos asociados de múltiples registros (actividades, evaluaciones, incidencias).

 - Solo se almacenan datos que se consultan frecuentemente o que benefician de acceso rápido.

## TODO: Operaciones Implementadas



## Conexión a Redis

La aplicación se conecta a Redis por defecto en:
- **Host**: localhost
- **Puerto**: 6379
- **Base de datos**: 0
- **Password**: None

Estos parámetros pueden ser modificados al llamar a la función `connect_redis()`.

## Características Adicionales

- **Manejo de errores**: Implementación robusta con manejo de excepciones de Redis
- **Tipado**: Uso de type hints para mejor claridad del código
- **Modularidad**: Cada operación está implementada como una función independiente
- **Interfaz interactiva**: Menú fácil de usar para probar todas las funcionalidades

## Notas sobre Módulos Redis

- **RedisJSON**: El cliente `redis-py` 4.x proporciona `client.json()` si el módulo está disponible en el servidor
- **RediSearch**: `redis-py` 4.x proporciona `redis.commands.search`. Alternativamente, se puede usar `redisearch-py`

## Contexto Académico

Este proyecto fue desarrollado como parte del curso de IA y Big Data, específicamente para el módulo de Sistemas de Bases de Datos (SBD). Implementa operaciones prácticas sobre Redis aplicadas a una plataforma de gestión de prácticas formativas.

## Licencia

Proyecto educativo desarrollado para fines académicos.