from decimal import Decimal

from django.shortcuts import get_object_or_404
from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro, Orden


class CompraService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        inventario = get_object_or_404(Inventario, libro=libro)
        total = CalculadorImpuestos.obtener_total_con_iva(float(libro.precio))
        return {
            "libro": libro,
            "total": total,
            "stock_actual": inventario.cantidad,
        }

    def ejecutar_compra(self, libro_id, cantidad=1, direccion="", usuario=None):
        libro = get_object_or_404(Libro, id=libro_id)
        inventario = get_object_or_404(Inventario, libro=libro)

        if inventario.cantidad < cantidad:
            raise ValueError("No hay suficiente stock para completar la compra.")

        total_unitario = CalculadorImpuestos.obtener_total_con_iva(float(libro.precio))
        total = Decimal(str(total_unitario)) * cantidad

        if not self.procesador_pago.pagar(float(total)):
            raise Exception("Error en la pasarela de pagos.")

        orden = Orden.objects.create(
            usuario=usuario if getattr(usuario, "is_authenticated", False) else None,
            libro=libro,
            total=total,
            direccion_envio=direccion,
        )

        inventario.cantidad -= cantidad
        inventario.save()

        return orden

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):

        orden = (
            self.builder
            .con_usuario(usuario)
            .con_productos(lista_productos)
            .para_envio(direccion)
            .build()
        )

        if self.procesador_pago.pagar(orden.total):
            return f"Orden {orden.pk} procesada exitosamente."

        orden.delete()
        raise Exception("Error en la pasarela de pagos.")

class CompraRapidaService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago

    def procesar(self, libro_id):
        libro = Libro.objects.get(id=libro_id)
        inv = Inventario.objects.get(libro=libro)
        
        if inv.cantidad <= 0:
            raise ValueError("No hay existencias.")
        
        total = CalculadorImpuestos.obtener_total_con_iva(float(libro.precio))
        if self.procesador_pago.pagar(total):
            inv.cantidad -= 1
            inv.save()
            return total
        return None