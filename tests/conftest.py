"""Fixtures compartidas por las pruebas."""

import pytest

from datos_prueba import una_configuracion


@pytest.fixture
def configuracion() -> dict:
    return una_configuracion()
