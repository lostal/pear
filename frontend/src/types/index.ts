export interface User {
  _id: string;
  username: string;
  role: 'user' | 'admin';
}

export interface LoginCredentials {
  username: string;
  password: string;
}

// Payload decodificado del JWT
export interface JwtPayload {
  id: string;
  username: string;
  role: 'user' | 'admin';
  exp?: number;
}

// ── Catálogo de productos ────────────────────────────────────────────────────

export interface Categoria {
  _id: string;
  nombre: string;
  slug: string;
  orden: number;
  icono?: string;
}

export interface OpcionColor {
  _id: string;
  valor: string;        // "Negro Sideral"
  codigoHex: string;    // "#1c1c1e"
  imagenes: string[];   // filenames
  modificadorPrecio: number;
}

export interface OpcionStorage {
  _id: string;
  valor: string;        // "256GB"
  codigoHex?: string;
  imagenes: string[];
  modificadorPrecio: number; // +100, etc.
}

export type Opcion = OpcionColor | OpcionStorage;

export type TipoGrupo = 'color' | 'storage' | 'button';

export interface GrupoOpciones {
  _id: string;
  tipo: TipoGrupo;
  nombre: string;       // "Color", "Almacenamiento"
  opciones: Opcion[];
}

export interface Product {
  _id: string;
  nombre: string;
  descripcion: string;
  categoria: Categoria;
  precioBase: number;
  imagenesDefault: string[];
  gruposOpciones: GrupoOpciones[];
  activo: boolean;
  orden: number;
}

// Grupo de productos por categoría (para la vista de tienda)
export interface ProductosPorCategoria {
  categoria: Categoria;
  productos: Product[];
}

// ── Helpers ─────────────────────────────────────────────────────────────────

/** Devuelve las imágenes a mostrar según el color seleccionado (o las default) */
export function getImagenesForProduct(product: Product, colorValor?: string): string[] {
  if (colorValor) {
    const colorGrupo = product.gruposOpciones.find(g => g.tipo === 'color');
    const opcion = colorGrupo?.opciones.find(o => o.valor === colorValor) as OpcionColor | undefined;
    if (opcion?.imagenes?.length) return opcion.imagenes;
  }
  // Fallback: primera opción de color disponible
  const colorGrupo = product.gruposOpciones.find(g => g.tipo === 'color');
  if (colorGrupo?.opciones.length) {
    const primera = colorGrupo.opciones[0] as OpcionColor;
    if (primera.imagenes?.length) return primera.imagenes;
  }
  return product.imagenesDefault;
}

/** Precio base + modificador del storage seleccionado */
export function getPrecioTotal(product: Product, storageValor?: string): number {
  let precio = product.precioBase;
  if (storageValor) {
    const storageGrupo = product.gruposOpciones.find(g => g.tipo === 'storage' || g.tipo === 'button');
    const opcion = storageGrupo?.opciones.find(o => o.valor === storageValor);
    if (opcion) precio += opcion.modificadorPrecio;
  }
  return precio;
}

/** Precio mínimo (para mostrar "Desde €X" en la card) */
export function getPrecioMinimo(product: Product): number {
  return product.precioBase;
}

/** URL completa de una imagen */
export function getImageUrl(filename: string): string {
  return `/api/uploads/${filename}`;
}
