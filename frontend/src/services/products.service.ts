import { http } from './http.js';
import type { Product, Categoria } from '../types/index.js';

// ── Categorías ────────────────────────────────────────────────────────────────

export async function fetchCategories(): Promise<Categoria[]> {
  return http.get<Categoria[]>('/api/categorias');
}

export async function createCategory(data: { nombre: string; slug: string; orden?: number }): Promise<Categoria> {
  return http.post<Categoria>('/api/categorias', data);
}

export async function updateCategory(id: string, data: Partial<{ nombre: string; slug: string; orden: number }>): Promise<Categoria> {
  return http.put<Categoria>(`/api/categorias/${id}`, data);
}

export async function deleteCategory(id: string): Promise<void> {
  return http.delete<void>(`/api/categorias/${id}`);
}

// ── Productos ─────────────────────────────────────────────────────────────────

export async function fetchProducts(categoriaSlug?: string): Promise<Product[]> {
  const url = categoriaSlug ? `/api/productos?categoria=${categoriaSlug}` : '/api/productos';
  return http.get<Product[]>(url);
}

export async function fetchProduct(id: string): Promise<Product> {
  return http.get<Product>(`/api/productos/${id}`);
}

export async function createProduct(data: {
  nombre: string;
  descripcion?: string;
  categoria: string;
  precioBase: number;
  orden?: number;
}): Promise<Product> {
  return http.post<Product>('/api/productos', data);
}

export async function updateProduct(id: string, data: Partial<{
  nombre: string;
  descripcion: string;
  categoria: string;
  precioBase: number;
  activo: boolean;
  orden: number;
}>): Promise<Product> {
  return http.put<Product>(`/api/productos/${id}`, data);
}

export async function deleteProduct(id: string): Promise<void> {
  return http.delete<void>(`/api/productos/${id}`);
}

// ── Grupos de opciones ────────────────────────────────────────────────────────

export async function addGrupo(productId: string, data: { tipo: string; nombre: string }): Promise<Product> {
  return http.post<Product>(`/api/productos/${productId}/grupos`, data);
}

export async function updateGrupo(productId: string, gId: string, data: { nombre?: string; tipo?: string }): Promise<Product> {
  return http.put<Product>(`/api/productos/${productId}/grupos/${gId}`, data);
}

export async function deleteGrupo(productId: string, gId: string): Promise<void> {
  return http.delete<void>(`/api/productos/${productId}/grupos/${gId}`);
}

// ── Opciones ──────────────────────────────────────────────────────────────────

export async function addOpcionColor(
  productId: string,
  gId: string,
  data: { valor: string; codigoHex: string },
  imagenes?: FileList | File[]
): Promise<Product> {
  const form = new FormData();
  form.append('valor', data.valor);
  form.append('codigoHex', data.codigoHex);
  if (imagenes) {
    Array.from(imagenes).forEach(f => form.append('imagenes', f));
  }
  return http.postForm<Product>(`/api/productos/${productId}/grupos/${gId}/opciones`, form);
}

export async function addOpcionStorage(
  productId: string,
  gId: string,
  data: { valor: string; modificadorPrecio: number }
): Promise<Product> {
  return http.post<Product>(`/api/productos/${productId}/grupos/${gId}/opciones`, data);
}

export async function updateOpcion(
  productId: string,
  gId: string,
  oId: string,
  data: Partial<{ valor: string; codigoHex: string; modificadorPrecio: number }>
): Promise<Product> {
  return http.put<Product>(`/api/productos/${productId}/grupos/${gId}/opciones/${oId}`, data);
}

export async function deleteOpcion(productId: string, gId: string, oId: string): Promise<void> {
  return http.delete<void>(`/api/productos/${productId}/grupos/${gId}/opciones/${oId}`);
}

// ── Imágenes de opciones de color ─────────────────────────────────────────────

export async function uploadImagenesOpcion(
  productId: string,
  gId: string,
  oId: string,
  files: FileList | File[]
): Promise<Product> {
  const form = new FormData();
  Array.from(files).forEach(f => form.append('imagenes', f));
  return http.postForm<Product>(
    `/api/productos/${productId}/grupos/${gId}/opciones/${oId}/imagenes`,
    form
  );
}

export async function deleteImagenOpcion(
  productId: string,
  gId: string,
  oId: string,
  filename: string
): Promise<void> {
  return http.delete<void>(
    `/api/productos/${productId}/grupos/${gId}/opciones/${oId}/imagenes?f=${encodeURIComponent(filename)}`
  );
}

// ── Imágenes default ──────────────────────────────────────────────────────────

export async function uploadImagenesDefault(productId: string, files: FileList | File[]): Promise<Product> {
  const form = new FormData();
  Array.from(files).forEach(f => form.append('imagenes', f));
  return http.postForm<Product>(`/api/productos/${productId}/imagenes-default`, form);
}

export async function reorderCategories(ids: string[]): Promise<void> {
  return http.put<void>('/api/categorias/reorder', { ids });
}

export async function reorderProductsBatch(ids: string[]): Promise<void> {
  return http.put<void>('/api/productos/reorder', { ids });
}

export async function reorderOpciones(productId: string, gId: string, opcionIds: string[]): Promise<Product> {
  return http.put<Product>(`/api/productos/${productId}/grupos/${gId}/opciones`, { opcionIds });
}

export async function reorderImagenesDefault(productId: string, imagenes: string[]): Promise<Product> {
  return http.put<Product>(`/api/productos/${productId}/imagenes-default`, { imagenes });
}

export async function reorderImagenesOpcion(
  productId: string,
  gId: string,
  oId: string,
  imagenes: string[]
): Promise<Product> {
  return http.put<Product>(`/api/productos/${productId}/grupos/${gId}/opciones/${oId}/imagenes`, { imagenes });
}

export async function deleteImagenDefault(productId: string, filename: string): Promise<void> {
  return http.delete<void>(
    `/api/productos/${productId}/imagenes-default?f=${encodeURIComponent(filename)}`
  );
}
