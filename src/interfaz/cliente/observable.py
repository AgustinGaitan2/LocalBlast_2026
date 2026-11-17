"""Notificación de cambios por suscripción (variante de MVC adoptada en DA-07).

Los Modelos heredan de Observable: avisan que cambiaron a quien se haya
suscrito, sin conocer quién es (no conocen a la Vista ni al Controlador).
"""

from collections.abc import Callable


class Observable:
    def __init__(self) -> None:
        self._observadores: list[Callable[[], None]] = []

    def suscribir(self, observador: Callable[[], None]) -> None:
        self._observadores.append(observador)

    def _notificar(self) -> None:
        for observador in self._observadores:
            observador()
