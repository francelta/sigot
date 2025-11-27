"""
Puertos (Interfaces) del Núcleo de SIGOT
Contratos que definen la comunicación entre el Core y la Infrastructure

IMPORTANTE: Este archivo NO debe importar Django ni ningún framework.
Solo usa Python puro (abc, typing, dataclasses).
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# Data Transfer Objects (DTOs) - Estructuras de datos puras
# ============================================================================

@dataclass
class Point:
    """Representa un punto geográfico (latitud, longitud)."""
    latitude: float
    longitude: float


@dataclass
class TransportistaData:
    """DTO para datos de un transportista."""
    user_id: int
    disponible: bool
    ubicacion: Optional[Point]
    trial_end: Optional[datetime]
    categoria_ids: List[int]


@dataclass
class MessageData:
    """DTO para datos de un mensaje."""
    chatroom_id: int
    author_id: int
    body: str
    attachment_path: Optional[str] = None


# ============================================================================
# Puertos (Interfaces) - Contratos del Núcleo
# ============================================================================

class TransportistaRepositoryPort(ABC):
    """
    Puerto para operaciones de repositorio de Transportistas.
    Define el contrato que cualquier adaptador de persistencia debe cumplir.
    """

    @abstractmethod
    def find_by_id(self, transportista_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca un transportista por su ID.
        
        Args:
            transportista_id: ID del transportista
            
        Returns:
            Dict con los datos del transportista o None si no existe
        """
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca un transportista por el ID de su usuario asociado.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Dict con los datos del transportista o None si no existe
        """
        pass

    @abstractmethod
    def find_near_location_by_category(
        self,
        point: Point,
        radius_km: float,
        category_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca transportistas cercanos a una ubicación, opcionalmente filtrados por categoría.
        
        Args:
            point: Punto geográfico (latitud, longitud)
            radius_km: Radio de búsqueda en kilómetros
            category_id: ID de categoría opcional para filtrar
            
        Returns:
            Lista de dicts con los datos de los transportistas encontrados
        """
        pass

    @abstractmethod
    def save(self, transportista_data: TransportistaData) -> Dict[str, Any]:
        """
        Guarda o actualiza un transportista.
        
        Args:
            transportista_data: DTO con los datos del transportista
            
        Returns:
            Dict con los datos del transportista guardado (incluyendo ID)
        """
        pass

    @abstractmethod
    def update_disponibilidad(self, user_id: int, is_disponible: bool) -> bool:
        """
        Actualiza el estado de disponibilidad de un transportista.
        
        Args:
            user_id: ID del usuario transportista
            is_disponible: Nuevo estado de disponibilidad
            
        Returns:
            True si la actualización fue exitosa, False en caso contrario
        """
        pass

    @abstractmethod
    def update_ubicacion(self, user_id: int, point: Point) -> bool:
        """
        Actualiza la ubicación de un transportista.
        
        Args:
            user_id: ID del usuario transportista
            point: Nueva ubicación (latitud, longitud)
            
        Returns:
            True si la actualización fue exitosa, False en caso contrario
        """
        pass


class ChatRepositoryPort(ABC):
    """
    Puerto para operaciones de repositorio de Chat.
    Define el contrato para gestionar salas de chat y mensajes.
    """

    @abstractmethod
    def get_room_by_id(self, room_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene una sala de chat por su ID.
        
        Args:
            room_id: ID de la sala de chat
            
        Returns:
            Dict con los datos de la sala o None si no existe
        """
        pass

    @abstractmethod
    def get_rooms_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene todas las salas de chat de un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de dicts con los datos de las salas de chat
        """
        pass

    @abstractmethod
    def create_room(self, participant_ids: List[int]) -> Dict[str, Any]:
        """
        Crea una nueva sala de chat con los participantes especificados.
        
        Args:
            participant_ids: Lista de IDs de usuarios participantes
            
        Returns:
            Dict con los datos de la sala creada
        """
        pass

    @abstractmethod
    def save_message(self, message_data: MessageData) -> Dict[str, Any]:
        """
        Guarda un mensaje en una sala de chat.
        
        Args:
            message_data: DTO con los datos del mensaje
            
        Returns:
            Dict con los datos del mensaje guardado (incluyendo ID y timestamp)
        """
        pass

    @abstractmethod
    def get_messages_for_room(
        self,
        room_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene los mensajes de una sala de chat con paginación opcional.
        
        Args:
            room_id: ID de la sala de chat
            limit: Número máximo de mensajes a retornar
            offset: Número de mensajes a saltar (para paginación)
            
        Returns:
            Lista de dicts con los datos de los mensajes
        """
        pass


class CategoriaRepositoryPort(ABC):
    """
    Puerto para operaciones de repositorio de Categorías.
    Define el contrato para gestionar categorías y sus jerarquías.
    """

    @abstractmethod
    def get_all_with_children(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las categorías con su estructura jerárquica (árbol).
        
        Returns:
            Lista de dicts con las categorías y sus hijos anidados
        """
        pass

    @abstractmethod
    def get_by_id(self, categoria_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene una categoría por su ID.
        
        Args:
            categoria_id: ID de la categoría
            
        Returns:
            Dict con los datos de la categoría o None si no existe
        """
        pass

    @abstractmethod
    def get_children(self, categoria_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene las subcategorías (hijos) de una categoría.
        
        Args:
            categoria_id: ID de la categoría padre
            
        Returns:
            Lista de dicts con las subcategorías
        """
        pass


class ValoracionRepositoryPort(ABC):
    """
    Puerto para operaciones de repositorio de Valoraciones.
    Define el contrato para gestionar valoraciones entre usuarios.
    """

    @abstractmethod
    def save(
        self,
        author_id: int,
        rated_user_id: int,
        rating: int,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Guarda una nueva valoración.
        
        Args:
            author_id: ID del usuario que envía la valoración
            rated_user_id: ID del usuario que recibe la valoración
            rating: Calificación (1-5)
            comment: Comentario opcional
            
        Returns:
            Dict con los datos de la valoración guardada
        """
        pass

    @abstractmethod
    def get_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene todas las valoraciones recibidas por un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de dicts con las valoraciones
        """
        pass

    @abstractmethod
    def has_rated(self, author_id: int, rated_user_id: int) -> bool:
        """
        Verifica si un usuario ya ha valorado a otro.
        
        Args:
            author_id: ID del usuario que envía la valoración
            rated_user_id: ID del usuario que recibe la valoración
            
        Returns:
            True si ya existe una valoración, False en caso contrario
        """
        pass


