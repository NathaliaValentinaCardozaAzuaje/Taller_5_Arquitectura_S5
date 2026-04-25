from decimal import Decimal

from .logic import CalculadorImpuestos
from ..models import Orden


class OrdenBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._usuario = None
        self.items = []
        self._direccion = ""

    def con_usuario(self, usuario):
        self._usuario = usuario
        return self

    def con_productos(self, productos):
        self.items = productos
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self

    def build(self) -> Orden:
        if not self._usuario or not self.items:
            raise ValueError("Datos insuficientes para crear la orden.")

        subtotal = sum(p.precio for p in self.items)
        total_con_iva = subtotal * 1.19

        orden = Orden.objects.create(
            usuario=self._usuario,
            total=total_con_iva,
            direccion_envio=self._direccion,
        )
        self.reset()
        return orden
