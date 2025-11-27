/**
 * Shared types for API responses
 * Based on OpenAPI schema
 */

export interface User {
  id: number
  username: string
  email: string
  phone: string | null
  is_transportista: boolean
  photo_url?: string | null
  created_at: string
}

export interface AuthResponse {
  access: string
  refresh?: string
  user: User
}

export interface LoginPayload {
  username: string
  password: string
}

export interface RegisterPayload {
  username: string
  email: string
  password: string
  is_transportista: boolean
  phone?: string | null
}

export interface ErrorResponse {
  error: string
  message: string
  details?: Record<string, unknown> | null
}

