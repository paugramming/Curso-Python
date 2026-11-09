def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """Calcula las emisiones de CO2 (kg) = consumo (kWh) * factor de emisión.

    Lanza ValueError si el consumo es negativo.
    """
    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo.")
    return consumo_kwh * factor_emision
