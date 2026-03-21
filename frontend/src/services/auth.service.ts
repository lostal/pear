import { http } from './http.js';
import { auth } from '../stores/auth.svelte.js';
import type { LoginCredentials, JwtPayload } from '../types/index.js';

function parseJwt(token: string): JwtPayload | null {
  try {
    const payload = token.split('.')[1];
    return JSON.parse(atob(payload)) as JwtPayload;
  } catch {
    return null;
  }
}

export async function login(credentials: LoginCredentials): Promise<void> {
  const res = await http.post<{ token: string }>('/api/login', credentials, { skipAuth: true });
  auth.setToken(res.token);
  const payload = parseJwt(res.token);
  if (payload) {
    auth.setUser({ _id: payload.id, username: payload.username, role: payload.role });
  }
}
