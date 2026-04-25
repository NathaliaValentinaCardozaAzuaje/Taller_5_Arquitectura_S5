from django.urls import path
from .api.views import CompraAPIView
from .views import CompraRapidaView, CompraView, InventarioView

urlpatterns = [
    path('', InventarioView.as_view(), name='inicio'),
    path('inventario/', InventarioView.as_view(), name='inventario'),
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
    path('compra-rapida/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida'),

]