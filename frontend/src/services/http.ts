import { auth } from '../stores/auth.svelte.js';
import { toast } from '../stores/toast.svelte.js';

interface RequestOptions extends RequestInit {
  skipAuth?: boolean;
}

async function request<T>(url: string, options: RequestOptions = {}): Promise<T> {
  const { skipAuth = false, headers: extraHeaders, ...init } = options;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  // Merge any extra headers passed by the caller
  if (extraHeaders && !(extraHeaders instanceof Headers)) {
    Object.assign(headers, extraHeaders);
  }

  if (!skipAuth && auth.token) {
    headers['Authorization'] = `Bearer ${auth.token}`;
  }

  const res = await fetch(url, { ...init, headers });

  if (res.status === 401 || res.status === 403) {
    auth.logout();
    toast.error(res.status === 401 ? 'Sesión expirada. Inicia sesión de nuevo.' : 'Acceso denegado.');
    throw new Error(res.status === 401 ? 'Unauthorized' : 'Forbidden');
  }

  if (res.status === 500) {
    toast.error('Error interno del servidor. Inténtalo más tarde.');
    throw new Error('Server error');
  }

  if (res.status === 204) return undefined as T;

  if (!res.ok) {
    let message = `Error ${res.status}`;
    try {
      const body = await res.json() as { message?: string; error?: string };
      message = body.message ?? body.error ?? message;
    } catch { /* empty */ }
    throw new Error(message);
  }

  return res.json() as Promise<T>;
}

export const http = {
  get: <T>(url: string, opts?: RequestOptions) =>
    request<T>(url, { method: 'GET', ...opts }),

  post: <T>(url: string, body: unknown, opts?: RequestOptions) =>
    request<T>(url, { method: 'POST', body: JSON.stringify(body), ...opts }),

  put: <T>(url: string, body: unknown, opts?: RequestOptions) =>
    request<T>(url, { method: 'PUT', body: JSON.stringify(body), ...opts }),

  patch: <T>(url: string, body: unknown, opts?: RequestOptions) =>
    request<T>(url, { method: 'PATCH', body: JSON.stringify(body), ...opts }),

  delete: <T>(url: string, opts?: RequestOptions) =>
    request<T>(url, { method: 'DELETE', ...opts }),
};
