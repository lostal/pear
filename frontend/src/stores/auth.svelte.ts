import type { User, JwtPayload } from '../types/index.js';

function parseJwt(token: string): JwtPayload | null {
  try {
    return JSON.parse(atob(token.split('.')[1])) as JwtPayload;
  } catch {
    return null;
  }
}

function userFromToken(token: string): User | null {
  const payload = parseJwt(token);
  if (!payload) return null;
  // Comprobar que el token no ha expirado
  if (payload.exp && payload.exp * 1000 < Date.now()) return null;
  return { _id: payload.id, username: payload.username, role: payload.role };
}

function createAuth() {
  const savedToken = localStorage.getItem('pear_token');
  // Intentar restaurar usuario desde el token guardado
  const restoredUser = savedToken ? userFromToken(savedToken) : null;
  // Si el token ha expirado, descartarlo
  const initialToken = restoredUser ? savedToken : null;

  let token = $state<string | null>(initialToken);
  let user = $state<User | null>(restoredUser);

  const isAuthenticated = $derived(token !== null && user !== null);
  const isAdmin = $derived(user?.role === 'admin');
  const displayName = $derived(user?.username ?? 'Invitado');

  function setToken(t: string | null) {
    token = t;
    if (t) {
      localStorage.setItem('pear_token', t);
    } else {
      localStorage.removeItem('pear_token');
    }
  }

  function setUser(u: User | null) {
    user = u;
  }

  function logout() {
    token = null;
    user = null;
    localStorage.removeItem('pear_token');
  }

  return {
    get token() { return token; },
    get user() { return user; },
    get isAuthenticated() { return isAuthenticated; },
    get isAdmin() { return isAdmin; },
    get displayName() { return displayName; },
    setToken,
    setUser,
    logout,
  };
}

export const auth = createAuth();
