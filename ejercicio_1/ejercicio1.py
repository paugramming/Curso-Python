"""Ejercicio 1 - Sanitización y Análisis Estadístico de Sensores (EcoTech Solutions)."""

import re

UBICACION_POR_DEFECTO = "Sin ubicación"

# Número (con signo y decimales opcionales) seguido de cualquier sufijo de unidad.
_PATRON_TEMPERATURA = re.compile(r"^\s*([-+]?\d+(?:[.,]\d+)?)")


def limpiar_registro_sensor(registro_raw):
    """Normaliza un registro crudo de sensor y devuelve un NUEVO diccionario.

    - sensor_id: sin espacios sobrantes.
    - temperatura: float sin sufijo de unidad (ej. "24.5C" -> 24.5).
    - ubicacion: valor por defecto si no existe o está vacía.

    Lanza ValueError si falta el id o la temperatura no es interpretable.
    """
    sensor_id = str(registro_raw.get("sensor_id") or "").strip()
    if not sensor_id:
        raise ValueError("El registro no tiene 'sensor_id' válido.")

    temperatura_raw = registro_raw.get("temperatura")
    if isinstance(temperatura_raw, (int, float)) and not isinstance(temperatura_raw, bool):
        temperatura = float(temperatura_raw)
    else:
        coincidencia = _PATRON_TEMPERATURA.match(str(temperatura_raw or ""))
        if not coincidencia:
            raise ValueError(
                f"Temperatura inválida para el sensor {sensor_id}: {temperatura_raw!r}"
            )
        temperatura = float(coincidencia.group(1).replace(",", "."))

    ubicacion = str(registro_raw.get("ubicacion") or "").strip() or UBICACION_POR_DEFECTO

    return {"sensor_id": sensor_id, "temperatura": temperatura, "ubicacion": ubicacion}


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """Devuelve (lista_sensores_alerta, promedio_temperatura).

    lista_sensores_alerta: IDs de los sensores cuya temperatura supera el umbral.
    promedio_temperatura: promedio global (0.0 si no hay sensores).
    """
    lista_sensores_alerta = [
        s["sensor_id"] for s in lista_sensores_limpios if s["temperatura"] > umbral_temperatura
    ]
    if lista_sensores_limpios:
        promedio = sum(s["temperatura"] for s in lista_sensores_limpios) / len(
            lista_sensores_limpios
        )
    else:
        promedio = 0.0
    return lista_sensores_alerta, promedio


if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 31.2 °C ", "ubicacion": " Planta Sur "},
        {"sensor_id": "  SENSOR-003", "temperatura": "28C"},
        {"sensor_id": "SENSOR-004 ", "temperatura": "35,8C", "ubicacion": ""},
        {"sensor_id": "SENSOR-005", "temperatura": 22, "ubicacion": "Planta Este"},
    ]
    UMBRAL = 30.0

    sensores_limpios = []
    for crudo in registros_crudos:
        try:
            sensores_limpios.append(limpiar_registro_sensor(crudo))
        except ValueError as error:
            print(f"[AVISO] Registro descartado: {error}")

    alertas, promedio = generar_resumen_sensores(sensores_limpios, UMBRAL)

    print("=" * 50)
    print("REPORTE DE SENSORES - EcoTech Solutions")
    print("=" * 50)
    for s in sensores_limpios:
        print(f"{s['sensor_id']:<12} {s['temperatura']:>6.1f} °C  {s['ubicacion']}")
    print("-" * 50)
    print(f"Umbral de alerta:        {UMBRAL:.1f} °C")
    print(f"Sensores en alerta ({len(alertas)}):  {', '.join(alertas) if alertas else 'ninguno'}")
    print(f"Temperatura promedio:    {promedio:.2f} °C")
    print("=" * 50)
