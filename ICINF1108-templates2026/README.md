# CRUD Students & Pets (FastAPI)

Proyecto FastAPI que implementa un **CRUD en memoria** para la entidad `Student` y sus mascotas (`Pet`). No requiere base de datos ni contenedores: los datos viven en un diccionario dentro del servicio y se pierden al reiniciar la aplicación.

## Requerimientos

- Python 3.13+ (gestionado automáticamente por [uv](https://docs.astral.sh/uv/))
- uv

## Resumen funcional

La API expone operaciones CRUD completas:

- **Estudiantes** bajo `/api/students`:
    - **Crear**: `POST /api/students`
    - **Listar**: `GET /api/students`
    - **Buscar por id**: `GET /api/students/:id`
    - **Actualizar**: `PATCH /api/students/:id`
    - **Eliminar**: `DELETE /api/students/:id` (también elimina sus mascotas)
- **Mascotas** anidadas bajo `/api/students/:studentId/pets`:
    - **Listar**: `GET /api/students/:studentId/pets`
    - **Crear**: `POST /api/students/:studentId/pets`
    - **Actualizar**: `PATCH /api/students/:studentId/pets/:petId`
    - **Eliminar**: `DELETE /api/students/:studentId/pets/:petId`

Cada estudiante tiene `id` (UUID), `name`, `email`, `age`, `createdAt` y `updatedAt`. El `email` es único: se rechaza con `409 Conflict` si ya existe.

Cada mascota tiene `id` (UUID), `studentId`, `name`, `species`, `age` (opcional), `createdAt` y `updatedAt`. Solo puede operar sobre su estudiante dueño.

Todas las respuestas JSON, tanto exitosas como de error, utilizan un estándar común. Se conservan los códigos HTTP correspondientes, como `200`, `201`, `404`, `409`, `422` y `500`.

## Estándar de respuestas JSON

La API utiliza la clase genérica `ApiResponse[DataT]`. El campo `data` puede contener un objeto, una lista de objetos o `null`, pero la estructura principal siempre se mantiene.

| Campo | Tipo JSON | Descripción |
| --- | --- | --- |
| `success` | `boolean` | Indica si la solicitud terminó correctamente. |
| `statusCode` | `number` | Código de estado HTTP de la respuesta. |
| `message` | `string` | Mensaje que explica el resultado. |
| `data` | `object`, `array` o `null` | Contiene los datos solicitados. |
| `error` | `object` o `null` | Contiene el tipo y los detalles del error. |

### Ejemplo de respuesta exitosa con una lista

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Estudiantes obtenidos correctamente",
  "data": [],
  "error": null
}
```

### Ejemplo de respuesta exitosa con un objeto

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Estudiante creado correctamente",
  "data": {
    "id": "identificador-del-estudiante",
    "name": "Jose Sepulveda",
    "email": "jose@example.com",
    "age": 24
  },
  "error": null
}
```

### Ejemplo de respuesta de error

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Estudiante no encontrado",
  "data": null,
  "error": {
    "type": "not_found",
    "details": null
  }
}
```

Los errores HTTP, los errores de validación y los errores internos son transformados por manejadores globales para mantener este mismo formato.

## Contexto técnico

- **Backend**: FastAPI
- **Almacenamiento**: en memoria (sin persistencia)
- **Validación**: Pydantic v2
- **Gestor de dependencias**: uv
- **Documentación**: Swagger en `/docs`

## Ejecución local

1. Instalar dependencias:

    ```bash
    make install
    ```

    O directamente con uv:

    ```bash
    uv sync
    ```

2. Levantar el servidor en modo desarrollo:

    ```bash
    make dev
    ```

    O usando uv:

    ```bash
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
    ```

La aplicación queda disponible en:

- `http://localhost:3000`
- `http://localhost:3000/docs`

## Comandos útiles

- `make install` — sincroniza dependencias con uv
- `make dev` — arranca uvicorn en modo reload
- `make lint` — ejecuta Ruff (con autocorrección)
- `make format` — formatea el código con Ruff
- `make format-check` — verifica el formato
- `make clean` — elimina `.venv`, cachés y artefactos
