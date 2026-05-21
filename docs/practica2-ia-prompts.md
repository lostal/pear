# Práctica 2 - Memoria de uso de IA

## Herramienta utilizada

**opencode** (CLI) con **DeepSeek V4 Pro** como modelo, ejecutado en local sobre el repositorio del proyecto.

---

## Proceso real

### 1. Preparación del contexto

Convertí los PDFs de la práctica 1 y la práctica 2 a Markdown y los subí a `docs/practicas/practica1.md` y `docs/practicas/practica2.md`. También tenía en `docs/servidor.md` la documentación del entorno de producción (DigitalOcean, Docker, etc.).

Abrí opencode y lo primero que hice fue pedirle una auditoría completa del proyecto para que tuviera contexto antes de empezar:

> _"Antes de pasar a la sesión de hoy quiero que revises y analices todo el proyecto y lo auditorices para tenerlo todo bien claro"_

La IA analizó el frontend (Svelte 5), el backend (Express/MongoDB) y la infraestructura (Docker). Me dio un informe con bugs, problemas de seguridad, y un mapa completo de la API. Esto fue útil para tener una foto fija de dónde estábamos.

---

### 2. Análisis de las prácticas

Luego le pedí que revisara los enunciados:

> _"Como ves en docs/practicas están la práctica 1 y la 2. La 1 la entregué hace un par de meses y ahora nos acaban de mandar la 2. Quería planificar esta segunda práctica, ¿qué me sugieres?"_

La IA identificó que la práctica 2 consiste en **reemplazar el backend Node.js por uno en Python** (Flask o FastAPI) manteniendo el frontend Svelte 5 intacto y respetando el contrato de API existente.

Aquí la IA acertó sugiriendo FastAPI sobre Flask por los puntos "gratis" de Pydantic, pero yo ya tenía claro que quería FastAPI.

---

### 3. Planificación

> _"Ahora sí, pasa a planificar. Infórmate bien, razona, di lo que necesites y procede. Toma tú las decisiones."_

La IA investigó por su cuenta:

- La documentación oficial de FastAPI (estructura de proyectos, JWT, uploads, CORS, excepciones)
- Cómo migrar de MongoDB anidado a SQL relacional con SQLModel
- Patrón repositorio con SQLAlchemy

El plan que propuso fue sólido:

- **FastAPI** + **SQLModel** + **SQLite**
- Arquitectura en capas: `routers → services → repositories`
- 8 tablas para reemplazar los subdocumentos anidados de MongoDB
- Schemas Pydantic separados con `serialization_alias` para que el frontend no notara el cambio (campos como `precioBase`, `_id`, `gruposOpciones`)

Aquí no hubo que refinar mucho. El plan era correcto.

---

### 4. Implementación

> _"Procede"_

La IA empezó a generar archivos. En su mayoría lo hizo bien pero algún error hubo.

---

## Errores de la IA que tuve que corregir

### 1. Sintaxis de modelos incompatible

La IA generó las definiciones de las tablas mezclando dos formas distintas de escribirlas, una de SQLAlchemy puro y otra de SQLModel. El programa no arrancaba. El mensaje de error no daba ninguna pista útil. Tuve que ir probando cambios hasta dar con la sintaxis correcta.

### 2. Una importación que lo rompía todo

En otro intento de arreglar lo anterior, la IA añadió una línea para resolver referencias circulares entre modelos, pero esa línea provocaba que el sistema no reconociese los tipos de las columnas. Al quitarla y usar una alternativa más sencilla, funcionó.

### 3. Incompatibilidad de contraseñas con la migración

El backend antiguo guardaba las contraseñas con un algoritmo distinto al que la IA configuró en el nuevo. Al migrar los usuarios, el login no decía "contraseña incorrecta": el servidor devolvía directamente un error 500. La solución fue configurar el sistema para que aceptase ambos formatos, el antiguo y el nuevo.

### 4. Los tests se interferían entre sí

El rate limiter del login estaba implementado como una variable global que no se reiniciaba entre tests. Cada test sumaba intentos, y al llegar al octavo saltaba el límite aunque fuesen peticiones legítimas. Se arregló vaciando el contador al inicio de cada test.

### 5. Una opción mal colocada

La configuración para que al borrar un producto se eliminasen también sus opciones e imágenes estaba en el sitio equivocado. No daba error, simplemente no funcionaba: las imágenes se quedaban guardadas. Bastó con mover ese parámetro dentro de otro para que funcionase.

### 6. Nombres de campos que no coincidían

La IA usó el estilo de Python para nombrar campos (`created_at`, `precio_base`) pero el frontend Svelte 5 los espera en camelCase (`createdAt`, `precioBase`). También hubo que ajustar cómo se devolvían las fechas para que el frontend las interpretase correctamente. Revisé todas las respuestas endpoint por endpoint hasta que coincidiesen con las del backend original.

## Conclusión

La IA fue útil para generar la estructura del proyecto y el código repetitivo, que a mano habría llevado bastante tiempo. Sin embargo, los errores que cometió requirieron entender qué estaba fallando y buscar la solución por mi cuenta. Sin cierta familiaridad previa con el framework, varios de estos problemas habrían sido difíciles de diagnosticar.
