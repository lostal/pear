import { http } from './http.js';
import type { User } from '../types/index.js';

export async function fetchUsers(): Promise<User[]> {
  return http.get<User[]>('/api/users');
}

export async function updateUserRole(id: string, role: 'user' | 'admin'): Promise<User> {
  return http.put<User>(`/api/users/${id}`, { role });
}

export async function deleteUser(id: string): Promise<void> {
  return http.delete<void>(`/api/users/${id}`);
}
