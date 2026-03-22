import { http } from './http.js';
import { auth } from '../stores/auth.svelte.js';
import { parseJwt } from '../lib/utils.js';
import type { LoginCredentials } from '../types/index.js';

export async function login(credentials: LoginCredentials): Promise<void> {
  const res = await http.post<{ token: string }>('/api/login', credentials, { skipAuth: true });
  auth.setToken(res.token);
  const payload = parseJwt(res.token);
  if (payload) {
    auth.setUser({ _id: payload.id, username: payload.username, role: payload.role });
  }
}
