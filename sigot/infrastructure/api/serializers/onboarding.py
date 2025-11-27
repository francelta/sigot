"""
Serializers para el proceso de onboarding de transportistas
"""

from rest_framework import serializers


class MaquinariaItemSerializer(serializers.Serializer):
    """
    Serializer para cada item de maquinaria en el payload de onboarding.
    """
    categoria_id = serializers.IntegerField(
        required=True,
        help_text='ID de la categoría (máquina)'
    )
    radio_km_especifico = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
        help_text='Radio de actuación específico para esta máquina en kilómetros. Si es null, usa radio_km_general'
    )
    nombre_vehiculo = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=200,
        help_text='Nombre personalizado del vehículo (ej. "Mi Furgoneta Mercedes")'
    )
    marca = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=100,
        help_text='Marca del vehículo (ej. "Mercedes", "Volvo", "Caterpillar")'
    )
    tonelaje = serializers.DecimalField(
        required=False,
        allow_null=True,
        max_digits=10,
        decimal_places=2,
        help_text='Tonelaje o capacidad de carga del vehículo'
    )
    caracteristicas = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='Descripción detallada de características especiales del vehículo'
    )
    imagen = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text='Imagen de la máquina (opcional). Puede venir como archivo separado en FormData'
    )


class OnboardingPayloadSerializer(serializers.Serializer):
    """
    Serializer para validar el payload completo del wizard de onboarding v3.0.
    Valida todos los datos de los 4 pasos del wizard.
    """

    # Step 1: Código Postal
    codigo_postal = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=10,
        help_text='Código postal para geocodificar la base de actuación'
    )

    # Step 2: Maquinaria (ya seleccionada en el frontend)
    maquinaria = serializers.ListField(
        child=MaquinariaItemSerializer(),
        required=True,
        min_length=1,
        help_text='Lista de máquinas (categorías) con sus radios e imágenes específicas'
    )

    # Step 3: Radio General
    radio_km_general = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
        help_text='Radio de actuación general en kilómetros (usado si no hay radio_km_especifico en maquinaria)'
    )

    # Step 4: Imágenes (opcionales)
    foto_de_perfil = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text='Foto de perfil del transportista (opcional)'
    )

    def validate(self, data):
        """
        Validación cruzada de campos.
        Verifica que haya al menos un radio definido (general o específico).
        """
        radio_km_general = data.get('radio_km_general')
        maquinaria = data.get('maquinaria', [])

        # Verificar que al menos haya un radio definido
        tiene_radio_general = radio_km_general is not None and radio_km_general > 0
        tiene_radio_especifico = any(
            item.get('radio_km_especifico') is not None and item.get('radio_km_especifico') > 0
            for item in maquinaria
        )

        if not tiene_radio_general and not tiene_radio_especifico:
            raise serializers.ValidationError({
                'radio_km_general': 'Debe proporcionar al menos un radio_km_general o al menos un radio_km_especifico en maquinaria'
            })

        # Verificar que todas las categorías sean únicas
        categoria_ids = [item['categoria_id'] for item in maquinaria]
        if len(categoria_ids) != len(set(categoria_ids)):
            raise serializers.ValidationError({
                'maquinaria': 'No se pueden duplicar categorías en la lista de maquinaria'
            })

        return data

