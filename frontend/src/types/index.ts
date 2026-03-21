export interface User {
  _id: string;
  username: string;
  role: 'user' | 'admin';
}

// Campos en español, tal como devuelve el backend
export interface Product {
  _id: string;
  nombre: string;
  precio: number;
  imagen?: string;
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
