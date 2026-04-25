from typing import Any, cast

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrdenInputSerializer
from tienda_app.services import CompraService
from tienda_app.infra.factories import PaymentFactory


class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    POST /api/v1/comprar/
    Payload: {"libro_id": 1, "direccion_envio": "Calle 123", "cantidad": 1}
    """

    def post(self, request):
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = cast(dict[str, Any], serializer.validated_data)
        libro_id = datos.get('libro_id')
        direccion = datos.get('direccion_envio', '')
        cantidad = datos.get('cantidad', 1)

        if libro_id is None:
            return Response({'error': 'libro_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gateway = PaymentFactory.get_processor()
            servicio = CompraService(procesador_pago=gateway)
            usuario = request.user if request.user.is_authenticated else None
            orden = servicio.ejecutar_compra(
                libro_id=libro_id,
                direccion=direccion,
                cantidad=cantidad,
                usuario=usuario,
            )

            return Response(
                {
                    'estado': 'exito',
                    'orden_id': orden.pk,
                    'total': str(orden.total),
                    'mensaje': f'Orden creada. Total: {orden.total}',
                }, status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception:
            return Response({'error': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
