# TP Final - EcoTech Solutions

Estructura del repositorio:

```
ejercicio_1/   -> ejercicio1.py   (sensores)
ejercicio_2/   -> ejercicio2.py   (catálogo, excepciones, JSON)
ejercicio_3/   -> proyecto Django completo (tests + vista)
```

## Ejecución

```bash
# Ejercicio 1
python ejercicio_1/ejercicio1.py

# Ejercicio 2 (genera catalogo_ecotech.json)
python ejercicio_2/ejercicio2.py

# Ejercicio 3
cd ejercicio_3
pip install -r requirements.txt
python manage.py test sustentabilidad   # tests unitarios
python manage.py runserver              # abrir http://127.0.0.1:8000/
```
