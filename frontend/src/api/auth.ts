import client from './client'
import type { LoginPayload, RegisterPayload, AuthResponse } from './types'

/**
 * Login user function
 * @param payload - Login credentials
 * @returns Auth response with token and user data
 */
export async function loginUser(payload: LoginPayload): Promise<AuthResponse> {
  const response = await client.post<AuthResponse>('/auth/login/', payload)
  return response.data
}

/**
 * Register new user function
 * @param payload - Registration data
 * @returns Auth response with token and user data
 */
export async function registerUser(
  payload: RegisterPayload
): Promise<AuthResponse> {
  const response = await client.post<AuthResponse>('/auth/register/', payload)
  return response.data
}

// Re-export types for convenience
export type { LoginPayload, RegisterPayload, AuthResponse } from './types'
