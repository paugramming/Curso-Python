from .emisiones import calcular_emisiones_carbono


def obtener_metricas_consumo(registros):
    """Procesa el historial de consumos por planta industrial.

    `registros`: lista de dicts {"planta": str, "consumo_kwh": número}.
    Una planta puede aparecer varias veces (historial): se acumula.

    Devuelve un dict con:
      - total_emisiones: emisiones globales (kg CO2)
      - planta_mayor_consumo: nombre de la planta con más kWh (None si no hay datos)
      - consumo_mayor_kwh: consumo total de esa planta
      - detalle_plantas: lista de dicts {planta, consumo_kwh, emisiones}, de mayor a menor consumo
    """
    consumo_por_planta = {}
    for registro in registros:
        planta = registro["planta"]
        consumo_por_planta[planta] = consumo_por_planta.get(planta, 0) + registro["consumo_kwh"]

    detalle = []
    total_emisiones = 0.0
    for planta, consumo in consumo_por_planta.items():
        emisiones = calcular_emisiones_carbono(consumo)  # ValueError si hay consumo negativo
        total_emisiones += emisiones
        detalle.append({"planta": planta, "consumo_kwh": consumo, "emisiones": emisiones})

    detalle.sort(key=lambda fila: fila["consumo_kwh"], reverse=True)

    return {
        "total_emisiones": total_emisiones,
        "planta_mayor_consumo": detalle[0]["planta"] if detalle else None,
        "consumo_mayor_kwh": detalle[0]["consumo_kwh"] if detalle else 0,
        "detalle_plantas": detalle,
    }
