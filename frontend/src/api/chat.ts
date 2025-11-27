import client from './client'
import type { User } from './types'

/**
 * Message type based on OpenAPI schema
 */
export interface Message {
  id: number
  chatroom_id: number
  author: User
  phone: string | null
  is_transportista: boolean
  photo_url?: string | null
  body: string
  attachment: string | null
  created_at: string
  last_read_at?: string | null
}

/**
 * ChatRoom type based on OpenAPI schema
 */
export interface ChatRoom {
  id: number
  participants: User[]
  is_favorite: boolean
  is_muted: boolean
  last_message: Message | null
  created_at: string
  updated_at: string
  unread_count?: number
}

/**
 * Payload for creating a new chat room
 */
export interface CreateChatRoomPayload {
  participant_ids: number[]
}

/**
 * Response for paginated messages
 */
export interface MessagesResponse {
  count: number
  next: string | null
  previous: string | null
  results: Message[]
}

/**
 * Parameters for fetching messages
 */
export interface FetchMessagesParams {
  limit?: number
  offset?: number
}

/**
 * Get all chat rooms for the authenticated user
 * @returns Array of chat rooms
 */
export async function getChatRooms(): Promise<ChatRoom[]> {
  const response = await client.get<ChatRoom[]>('/chat/rooms/')
  return response.data
}

/**
 * Create a new chat room or get existing one
 * @param participantId - ID of the other participant (current user is added automatically)
 * @returns Created or existing chat room
 */
export async function startChatRoom(participantId: number): Promise<ChatRoom> {
  // Get current user ID from authStore
  const { useAuthStore } = await import('../stores/authStore')
  const authStore = useAuthStore()
  const currentUserId = authStore.user?.id

  if (!currentUserId) {
    throw new Error('User must be authenticated to create a chat room')
  }

  const payload: CreateChatRoomPayload = {
    participant_ids: [currentUserId, participantId],
  }

  const response = await client.post<ChatRoom>('/chat/rooms/', payload)
  return response.data
}

/**
 * Fetch messages from a chat room
 * @param roomId - ID of the chat room
 * @param params - Pagination parameters
 * @returns Paginated messages response
 */
export async function getMessages(
  roomId: number,
  params?: FetchMessagesParams
): Promise<MessagesResponse> {
  const response = await client.get<MessagesResponse>(
    `/chat/rooms/${roomId}/messages/`,
    {
      params,
    }
  )
  return response.data
}
