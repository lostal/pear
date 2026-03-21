## Contexto de la práctica

Puedes utilizar tu propio backend en Node.js con JWT creado en la primera parte de la asignatura o el backend https://github.com/dperezalvarez/PW2-inicial-2026/tree/main/backend en caso de que te falte funcionalidad.

El backend tiene dos recursos principales:

- Productos (CRUD completo, protegido por roles).
- Usuarios (CRUD completo, con roles usuario/admin).

El objetivo es construir el frontend completo en Svelte 5 (sin SvelteKit, o SvelteKit pero usando sólo frontend) consumiendo esta API y gestionando autenticación, estado global y navegación de la aplicación.

## Requisitos mínimos de la entrega (5 puntos)

Estos requisitos son obligatorios para aprobar (máx. 5 puntos si solo se cumple este bloque).

### 1. Estructura del proyecto

- Proyecto creado con Vite + Svelte 5 (plantilla oficial actual).
- Organización básica en carpetas: components, pages, services (o similar).

### 2. Autenticación básica con JWT

- Pantalla de login con usuario y contraseña.
- Envío de credenciales al backend, gestión de respuestas de error.
- Almacenar el token JWT en memoria (no es obligatorio persistir, eso es ampliación).
- Evitar mostrar las pantallas privadas si no hay usuario autenticado.

### 3. Consumo de API de productos

- Listado de productos mostrando al menos: nombre, precio y estado (activo/no activo).
- Detalle de un producto en una vista aparte o modal.
- Creación de producto nuevo (formulario).
- Edición y borrado de producto (si el backend lo permite según rol).

### 4. Navegación

- Navegación tipo SPA: al menos 3 "pantallas": Login, Productos, Perfil o similar.
- Resaltar claramente la pantalla actual (barra de navegación o similar).

### 5. Estilos y UX básicos

- Layout mínimamente cuidado (no vale HTML con los estilos sin trabajar).
- Diseño responsive básico (que no se rompa en móvil).

## Uso de funcionalidades de Svelte 5 (hasta +3 puntos)

Este bloque evalúa que usen runes y nuevas APIs de Svelte 5.

### 1. Estado y derivados con runes (hasta +1 punto)

- Uso de `$state()` para manejar el estado principal de la aplicación (usuario autenticado, token, productos cargados).
- Uso de `$derived()` para valores derivados (por ejemplo: productos filtrados, contador de productos, nombre del usuario en cabecera).

### 2. Efectos y side effects (hasta +1 punto)

- Uso de `$effect()` para:
  - Reaccionar a cambios de usuario autenticado (por ejemplo, redirigir al login si se borra el token).
  - Sincronizar datos del frontend con el backend (volver a cargar productos cuando cambie un filtro importante o el rol).

### 3. Props y comunicación entre componentes (hasta +1 punto)

- Uso de `$props()` para definir props de componentes (por ejemplo, componente ProductCard, ProductForm, UserRow, etc.).
- Uso de callbacks (en lugar de eventos personalizados clásicos) para comunicar acciones del hijo al padre (por ejemplo, `onSave(producto)`, `onDelete(id)`).

## Funcionalidades avanzadas opcionales (hasta +2 puntos)

Cada funcionalidad suma parte de los 2 puntos máximos según grado de calidad y complejidad.

### 1. Gestión de usuarios y roles

- Zona de administración solo accesible a rol admin.
- Listado de usuarios, cambio de rol, alta/baja de usuarios.
- Mostrar/ocultar acciones en producto según rol (p.ej. solo admin puede borrar).

### 2. Persistencia de sesión

- Persistir el JWT en localStorage o sessionStorage.
- Al recargar la página, restaurar el estado del usuario usando `$state()` inicializado desde el almacenamiento.
- Cerrar sesión limpiando correctamente el estado y el almacenamiento.

### 3. Filtros y búsqueda

- Barra de búsqueda de productos (por nombre, categoría, rango de precio).
- Filtros combinados con `$derived()` para no recalcular ni recargar innecesariamente.
- Paginación o carga incremental si el backend lo soporta.

### 4. Manejo avanzado de formularios

- Validaciones en el frontend (campos obligatorios, formatos, rangos).
- Mensajes de error y éxito claros para el usuario.
- Deshabilitar botones mientras se guardan cambios.

### 5. Experiencia de usuario mejorada

- Feedback de carga (spinners, skeletons) cuando se piden datos al backend.
- Manejo de errores global (ej. toast/alerta para errores 401/403/500).
- Confirmación de acciones destructivas (borrado de producto/usuario).

## Criterios de evaluación resumidos

| Aspecto | Descripción | Puntos máx. |
|---|---|---|
| Requisitos mínimos backend/frontend | Login, consumo de API de productos, navegación básica, estilos mínimos | 5 |
| Runes Svelte 5: estado y derivados | Uso correcto de `$state()` y `$derived()` para estado global y datos derivados | 1 |
| Runes Svelte 5: efectos | Uso adecuado de `$effect()` para side effects (carga de datos, redirecciones, sincronización) | 1 |
| Comunicación con `$props()` y callbacks | Componentes reutilizables con `$props()` y callbacks para acciones | 1 |
| Funcionalidades avanzadas | Gestión de usuarios/roles, persistencia de sesión, filtros, UX avanzada, formularios complejos | 2 |
| **Total** | | **10** |

## Entrega

- Código en un repositorio público (GitHub, GitLab, etc.) con instrucciones claras de instalación y ejecución en el README.
- Explicar en el README qué runas de Svelte 5 se usan y en qué componentes.
- Indicar qué partes del backend se están utilizando (endpoints principales y roles necesarios).
- Necesario subir la documentación al Campus.

**Fecha de entrega:**

- Hasta el 25 de marzo de 2026 a las 23:59
