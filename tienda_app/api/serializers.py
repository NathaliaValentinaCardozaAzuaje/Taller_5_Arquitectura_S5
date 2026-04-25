from rest_framework import serializers
from tienda_app.models import Libro, Orden


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'precio', 'stock_actual']

class OrdenInputSerializer(serializers.Serializer):
    libro_id = serializers.IntegerField()
    direccion_envio = serializers.CharField(max_length=200)
    cantidad = serializers.IntegerField(min_value=1, default=1)
