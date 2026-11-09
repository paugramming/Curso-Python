import unittest

from .emisiones import calcular_emisiones_carbono
from .metricas import obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    """Auditoría de calcular_emisiones_carbono."""

    def test_calculo_con_factor_por_defecto(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)

    def test_calculo_con_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(200, factor_emision=0.5), 100.0)

    def test_consumo_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    def test_consumo_decimal(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(12.5), 5.0)

    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-1)

    def test_consumo_negativo_con_factor_personalizado(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-50, factor_emision=0.7)


class TestMetricasConsumo(unittest.TestCase):
    """Verifica la integración de la función de emisiones en las métricas."""

    def setUp(self):
        self.registros = [
            {"planta": "Norte", "consumo_kwh": 100},
            {"planta": "Sur", "consumo_kwh": 300},
            {"planta": "Norte", "consumo_kwh": 100},
        ]

    def test_total_y_planta_mayor_consumo(self):
        metricas = obtener_metricas_consumo(self.registros)
        self.assertAlmostEqual(metricas["total_emisiones"], 200.0)  # 500 kWh * 0.4
        self.assertEqual(metricas["planta_mayor_consumo"], "Sur")

    def test_sin_registros(self):
        metricas = obtener_metricas_consumo([])
        self.assertEqual(metricas["total_emisiones"], 0)
        self.assertIsNone(metricas["planta_mayor_consumo"])

    def test_consumo_negativo_propaga_error(self):
        with self.assertRaises(ValueError):
            obtener_metricas_consumo([{"planta": "Norte", "consumo_kwh": -10}])


if __name__ == "__main__":
    unittest.main()
