import client from './client'
import type { User } from './types'

/**
 * Categoria type based on OpenAPI schema
 */
export interface Categoria {
  id: number
  nombre: string
  descripcion: string | null
  parent: number | null
  children?: Categoria[]
}

/**
 * Transportista type based on OpenAPI schema v3.0
 */
export interface Transportista {
  id: number
  user: User
  disponible: boolean
  codigo_postal: string | null
  base_geocodificada: {
    lat: number
    lon: number
  } | null
  tipo_zona_actuacion: 'RADIO' | 'ZONAS'
  radio_km_general: number | null
  zonas_definidas: Record<string, unknown> | null
  foto_de_perfil_url: string | null
  trial_end: string | null
  categorias: Categoria[]
  maquinaria?: Array<{
    categoria: Categoria
    radio_km_especifico: number | null
    nombre_vehiculo: string | null
    marca: string | null
    tonelaje: number | null
    caracteristicas: string | null
    imagen_maquina_url: string | null
  }>
  distancia_km?: number | null
}

/**
 * Parameters for fetching transportistas by zone
 */
export interface FetchTransportistasParams {
  q: string
  categoria?: number
}

/**
 * Response for transportistas search
 */
export interface TransportistasResponse {
  count: number
  results: Transportista[]
}

/**
 * Payload for updating transportista availability
 */
export interface UpdateMiEstadoPayload {
  disponible: boolean
}

/**
 * Response for updating transportista availability
 */
export interface UpdateMiEstadoResponse {
  disponible: boolean
  message: string
}

/**
 * Payload for updating complete transportista profile
 * @deprecated Use submitOnboardingWizard instead for transactional updates
 */
export interface UpdateMiPerfilPayload {
  phone?: string | null
  codigo_postal?: string | null
  tipo_zona_actuacion?: 'RADIO' | 'ZONAS'
  radio_km_general?: number | null
  zonas_definidas?: Record<string, unknown> | null
  categoria_ids?: number[]
}

/**
 * Response for updating profile
 */
export interface UpdateMiPerfilResponse {
  message: string
}

/**
 * Item de maquinaria en el payload de onboarding v3.0
 */
export interface MaquinariaItem {
  categoria_id: number
  radio_km_especifico: number | null
  nombre_vehiculo?: string | null
  marca?: string | null
  tonelaje?: number | null
  caracteristicas?: string | null
  imagen?: File | null
}

/**
 * Complete payload for onboarding wizard submission v3.0
 * This payload contains all data from the wizard steps in a single transaction
 */
export interface WizardDataPayload {
  // Step 1: Código Postal
  codigo_postal: string
  // Step 2: Maquinaria (ya seleccionada)
  maquinaria: MaquinariaItem[]
  // Step 3: Radio General
  radio_km_general: number | null
  // Step 4: Imágenes (opcionales)
  foto_de_perfil?: File | null
}

/**
 * Response for onboarding wizard submission
 */
export interface WizardSubmissionResponse {
  message: string
  transportista: Transportista
  user: User
}

/**
 * Fetch all categories with hierarchical structure
 * @returns Array of categories with children
 */
export async function fetchCategorias(): Promise<Categoria[]> {
  const response = await client.get<Categoria[]>('/categorias/')
  return response.data
}

/**
 * Fetch transportistas by zone of operation
 * @param params - Search parameters (query and optional category filter)
 * @returns Transportistas response with count and results
 */
export async function fetchTransportistasPorZona(
  params: FetchTransportistasParams
): Promise<TransportistasResponse> {
  const response = await client.get<TransportistasResponse>(
    '/transportistas/cercanos/',
    {
      params,
    }
  )
  return response.data
}

/**
 * Get current transportista profile
 * @returns Transportista profile
 */
export async function getMiPerfil(): Promise<Transportista> {
  const response = await client.get<Transportista>('/transportistas/mi-perfil/')
  return response.data
}

/**
 * Update transportista availability status
 * @param payload - Availability status
 * @returns Update response
 */
export async function updateMiEstado(
  payload: UpdateMiEstadoPayload
): Promise<UpdateMiEstadoResponse> {
  const response = await client.patch<UpdateMiEstadoResponse>(
    '/transportistas/mi-estado/',
    payload
  )
  return response.data
}

/**
 * Submit complete onboarding wizard data v3.0 in a single transactional request
 * This function sends all wizard data to the backend in one atomic operation,
 * preventing partial updates that could leave the profile in an inconsistent state.
 *
 * @param payload - Complete wizard data (all 4 steps)
 * @returns Response with updated transportista and user data
 * @throws Error if the backend endpoint is not available or request fails
 *
 * @example
 * ```typescript
 * const payload: WizardDataPayload = {
 *   codigo_postal: '28001',
 *   maquinaria: [
 *     { categoria_id: 10, radio_km_especifico: 50, imagen: file1 },
 *     { categoria_id: 20, radio_km_especifico: null }
 *   ],
 *   radio_km_general: 100,
 *   foto_de_perfil: file2
 * }
 * const response = await submitOnboardingWizard(payload)
 * ```
 */
export async function submitOnboardingWizard(
  payload: WizardDataPayload
): Promise<WizardSubmissionResponse> {
  // Check if we need to use FormData (if there are files)
  const hasFiles = payload.foto_de_perfil || payload.maquinaria.some(m => m.imagen)
  
  if (hasFiles) {
    // Use FormData for multipart/form-data
    const formData = new FormData()
    formData.append('codigo_postal', payload.codigo_postal)
    formData.append('radio_km_general', payload.radio_km_general?.toString() || '')
    
    if (payload.foto_de_perfil) {
      formData.append('foto_de_perfil', payload.foto_de_perfil)
    }
    
    // Append maquinaria as JSON string (backend will parse it)
    // For files in maquinaria, we need to append them separately
    const maquinariaData = payload.maquinaria.map((m, index) => ({
      categoria_id: m.categoria_id,
      radio_km_especifico: m.radio_km_especifico,
      // Image will be appended separately with index
    }))
    formData.append('maquinaria', JSON.stringify(maquinariaData))
    
    // Append images for each maquina
    payload.maquinaria.forEach((m, index) => {
      if (m.imagen) {
        formData.append(`maquinaria_${index}_imagen`, m.imagen)
      }
    })
    
    const response = await client.post<WizardSubmissionResponse>(
      '/onboarding/complete/',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    )
    return response.data
  } else {
    // Use JSON for simple data
    const response = await client.post<WizardSubmissionResponse>(
      '/onboarding/complete/',
      payload
    )
    return response.data
  }
}

/**
 * Update complete transportista profile
 * @deprecated This function makes multiple non-transactional PATCH requests
 * which can leave the profile in an inconsistent state if one fails.
 * Use submitOnboardingWizard instead for onboarding flows.
 *
 * @param payload - Profile data
 * @returns Update response
 */
export async function updateMiPerfil(
  payload: UpdateMiPerfilPayload
): Promise<UpdateMiPerfilResponse> {
  // First update user phone if provided
  if (payload.phone !== undefined) {
    await client.patch('/auth/user/', { phone: payload.phone })
  }

  // Update transportista profile
  const transportistaPayload: Record<string, unknown> = {}

  if (payload.codigo_postal !== undefined) {
    transportistaPayload.codigo_postal = payload.codigo_postal
  }

  if (payload.tipo_zona_actuacion !== undefined) {
    transportistaPayload.tipo_zona_actuacion = payload.tipo_zona_actuacion
  }

  if (payload.radio_km_general !== undefined) {
    transportistaPayload.radio_km_general = payload.radio_km_general
  }

  if (payload.zonas_definidas !== undefined) {
    transportistaPayload.zonas_definidas = payload.zonas_definidas
  }

  // Update transportista basic data if any
  if (Object.keys(transportistaPayload).length > 0) {
    await client.patch('/transportistas/mi-perfil/', transportistaPayload)
  }

  // Update categories if provided
  if (payload.categoria_ids && payload.categoria_ids.length > 0) {
    await client.patch('/transportistas/mi-perfil/', {
      categoria_ids: payload.categoria_ids,
    })
  }

  return { message: 'Perfil actualizado correctamente' }
}
