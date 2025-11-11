"""
Šablona pro nový Django testovací soubor
----------------------------------------
Tento soubor je pouze šablona. Pokud vytváříš nový test, zkopíruj si jej a přepiš podle potřeby.
POZOR: Třída NovaFunkceTestCase je zakomentovaná, aby pytest nehlásil chybu při běhu všech testů.

Navíc: Ukázkový test, který ověří, že všechny šablony lze načíst bez syntax erroru.
"""

import os

from django.template import Template, TemplateSyntaxError

import pytest

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../klienti/templates/")


@pytest.mark.parametrize(
    "template_path",
    [
        os.path.join(root, file)
        for root, _, files in os.walk(TEMPLATES_DIR)
        for file in files
        if file.endswith(".html")
    ],
)
def test_template_can_be_loaded(template_path):
    """
    Ověří, že šablonu lze načíst bez syntax erroru.
    """
    with open(template_path, encoding="utf-8") as f:
        content = f.read()
    try:
        Template(content)
    except TemplateSyntaxError as e:
        pytest.fail(f"Chyba v šabloně {template_path}: {e}")


# from django.test import TestCase

# class NovaFunkceTestCase(TestCase):
#     """
#     Popiš, co tato třída testuje (např. import klientů, export, reporting, ...)
#     """
#     def setUp(self):
#         # Inicializace dat, příprava prostředí
#         pass
#
#     def test_zakladni_scenar(self):
#         """
#         Popiš, co tento test ověřuje (např. úspěšný import, správný výstup, ...)
#         """
#         # ...testovací logika...
#         self.assertTrue(True)
#
#     def test_edge_case(self):
#         """
#         Ověř edge-case scénář (např. chybějící pole, nevalidní vstup, ...)
#         """
#         # ...testovací logika...
#         self.assertTrue(True)
