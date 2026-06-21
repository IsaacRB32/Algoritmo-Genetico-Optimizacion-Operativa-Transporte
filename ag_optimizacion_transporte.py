## Clasificación Comercial del Cliente (Importancia Comercial "IC")
## 1 = Cliente particular, 2 = Escuela o grupo local, 3 = Empresa privada
## 4 = Agencia turística nacional, 5 = Agencia turística internacional
catalogo_clientes = {
    "OS-01": 5, "OS-02": 1, "OS-03": 3, "OS-04": 4, "OS-05": 2,
    "OS-06": 3, "OS-07": 1, "OS-08": 5, "OS-09": 2, "OS-10": 1,
    "OS-11": 4, "OS-12": 3, "OS-13": 2, "OS-14": 4, "OS-15": 5,
    "OS-16": 3, "OS-17": 2, "OS-18": 1, "OS-19": 4, "OS-20": 5
}

## Distancia total del servicio en kilómetros
distancia_servicios = {
    "OS-01": 1200.0, "OS-02": 45.0,  "OS-03": 350.0, "OS-04": 800.0, "OS-05": 120.0,
    "OS-06": 500.0,  "OS-07": 80.0,  "OS-08": 950.0, "OS-09": 400.0, "OS-10": 60.0,
    "OS-11": 1500.0, "OS-12": 200.0, "OS-13": 90.0,  "OS-14": 600.0, "OS-15": 1100.0,
    "OS-16": 450.0,  "OS-17": 150.0, "OS-18": 55.0,  "OS-19": 750.0, "OS-20": 1300.0
}

## Índice de Eficiencia Relativa (IER) - Valores entre 0.0 y 1.0
catalogo_ier = {
    "OP-01": 0.95, "OP-02": 0.88, "OP-03": 0.75, "OP-04": 0.92, "OP-05": 0.60,
    "OP-06": 0.81, "OP-07": 0.99, "OP-08": 0.70, "OP-09": 0.85, "OP-10": 0.91,
    "OP-11": 0.65, "OP-12": 0.89, "OP-13": 0.77, "OP-14": 0.94, "OP-15": 0.82,
    "OP-16": 0.68, "OP-17": 0.97, "OP-18": 0.84, "OP-19": 0.72, "OP-20": 0.90,
    "OP-21": 0.55, "OP-22": 0.86, "OP-23": 0.79, "OP-24": 0.93, "OP-25": 0.64,
    "OP-26": 0.87, "OP-27": 0.96, "OP-28": 0.71, "OP-29": 0.83, "OP-30": 0.80,
    "OP-31": 0.98, "OP-32": 0.62, "OP-33": 0.78, "OP-34": 0.88, "OP-35": 0.91
}

## Estatus legal (True = Vigente, False = Vencido/Vacaciones/Inhabilitado)
licencias_vigentes = {
    "OP-01": True,  "OP-02": True,  "OP-03": True,  "OP-04": False, "OP-05": False,
    "OP-06": True,  "OP-07": True,  "OP-08": False, "OP-09": True,  "OP-10": True,
    "OP-11": True,  "OP-12": True,  "OP-13": True,  "OP-14": True,  "OP-15": False,
    "OP-16": True,  "OP-17": True,  "OP-18": True,  "OP-19": False, "OP-20": True,
    "OP-21": False, "OP-22": True,  "OP-23": True,  "OP-24": True,  "OP-25": False,
    "OP-26": True,  "OP-27": True,  "OP-28": False, "OP-29": True,  "OP-30": True,
    "OP-31": True,  "OP-32": False, "OP-33": True,  "OP-34": True,  "OP-35": False
}

## Factor de Rendimiento (FRD) en km/L
catalogo_frd = {
    "UNI-01": 4.5, "UNI-02": 3.8, "UNI-03": 2.9, "UNI-04": 4.1, "UNI-05": 3.5,
    "UNI-06": 4.8, "UNI-07": 3.2, "UNI-08": 2.5, "UNI-09": 4.6, "UNI-10": 3.9,
    "UNI-11": 4.0, "UNI-12": 3.1, "UNI-13": 2.8, "UNI-14": 4.3, "UNI-15": 3.7,
    "UNI-16": 4.9, "UNI-17": 3.4, "UNI-18": 2.6, "UNI-19": 4.2, "UNI-20": 3.6,
    "UNI-21": 4.7, "UNI-22": 3.0, "UNI-23": 2.7, "UNI-24": 4.4, "UNI-25": 3.3,
    "UNI-26": 5.0, "UNI-27": 3.8, "UNI-28": 2.4, "UNI-29": 4.1, "UNI-30": 3.5,
    "UNI-31": 5.2, "UNI-32": 2.2, "UNI-33": 3.9, "UNI-34": 4.6, "UNI-35": 3.1
}

## Estatus Operativo
estado_unidades = {
    "UNI-01": "Disponible",       "UNI-02": "Disponible",       "UNI-03": "Disponible",
    "UNI-04": "Disponible",       "UNI-05": "En Mantenimiento", "UNI-06": "Disponible",
    "UNI-07": "Disponible",       "UNI-08": "Taller Externo",   "UNI-09": "Disponible",
    "UNI-10": "Disponible",       "UNI-11": "Disponible",       "UNI-12": "Disponible",
    "UNI-13": "En Mantenimiento", "UNI-14": "Disponible",       "UNI-15": "Disponible",
    "UNI-16": "Disponible",       "UNI-17": "En Mantenimiento", "UNI-18": "Disponible",
    "UNI-19": "Disponible",       "UNI-20": "Baja",             "UNI-21": "Disponible",
    "UNI-22": "Disponible",       "UNI-23": "En Mantenimiento", "UNI-24": "Disponible",
    "UNI-25": "Disponible",       "UNI-26": "Disponible",       "UNI-27": "Disponible",
    "UNI-28": "En Mantenimiento", "UNI-29": "Disponible",       "UNI-30": "En Mantenimiento",
    "UNI-31": "Disponible",       "UNI-32": "En Mantenimiento", "UNI-33": "Disponible",
    "UNI-34": "Disponible",       "UNI-35": "Disponible"
}