import { http } from './http.js';
import type { Product } from '../types/index.js';

export interface ProductPayload {
  nombre: string;
  precio: number;
}

export async function fetchProducts(): Promise<Product[]> {
  return http.get<Product[]>('/api/productos');
}

export async function fetchProduct(id: string): Promise<Product> {
  return http.get<Product>(`/api/productos/${id}`);
}

export async function createProduct(data: ProductPayload): Promise<Product> {
  return http.post<Product>('/api/productos', data);
}

export async function updateProduct(id: string, data: Partial<ProductPayload>): Promise<Product> {
  return http.put<Product>(`/api/productos/${id}`, data);
}

export async function deleteProduct(id: string): Promise<void> {
  return http.delete<void>(`/api/productos/${id}`);
}
