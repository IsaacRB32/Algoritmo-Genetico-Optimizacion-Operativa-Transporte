
"""
=============================================================================
ag_optimizacion_transporte.py
=============================================================================
ALGORITMO GENÉTICO PARA OPTIMIZACIÓN DE ASIGNACIÓN DE RECURSOS
Empresa de Renta de Transporte de Pasajeros

Objetivo: Maximizar la utilidad operativa diaria mediante la asignación
          óptima de operadores y unidades vehiculares a las órdenes de
          servicio del día.

─────────────────────────────────────────────────────────────────────────────
FUNCIÓN OBJETIVO:
    F(A) = Σ [w1·Eop(o,s) + w2·Eun(u,s)] − ΩA

    Evaluación del recurso humano:    Eop(o,s) = IER(o) · IC(s)
    Evaluación del recurso mecánico:  Eun(u,s) = FR(u)  · D(s)
    Penalización exterior:            ΩA = λD·DA + λL·LA

─────────────────────────────────────────────────────────────────────────────
ESTRUCTURA DEL CROMOSOMA (codificación entera):
    A = [(s₁,o₁,u₁), (s₂,o₂,u₂), …, (sₙ,oₙ,uₙ)]
    Donde sᵢ = OS (constante), oᵢ = Operador (variable), uᵢ = Unidad (variable)

=============================================================================
"""

import random
import copy
from typing import List, Tuple, Dict, Optional


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 1 — BASE DE CONOCIMIENTO (Catálogos del Sistema)
# ─────────────────────────────────────────────────────────────────────────────

## Clasificación Comercial del Cliente (Importancia Comercial "IC")
## 1=Particular, 2=Escuela/Grupo local, 3=Empresa privada,
## 4=Agencia turística nacional, 5=Agencia turística internacional
catalogo_clientes: Dict[str, int] = {
    "OS-01": 5, "OS-02": 1, "OS-03": 3, "OS-04": 4, "OS-05": 2,
    "OS-06": 3, "OS-07": 1, "OS-08": 5, "OS-09": 2, "OS-10": 1,
    "OS-11": 4, "OS-12": 3, "OS-13": 2, "OS-14": 4, "OS-15": 5,
    "OS-16": 3, "OS-17": 2, "OS-18": 1, "OS-19": 4, "OS-20": 5
}

## Distancia total del servicio en kilómetros
distancia_servicios: Dict[str, float] = {
    "OS-01": 1200.0, "OS-02": 45.0,  "OS-03": 350.0, "OS-04": 800.0, "OS-05": 120.0,
    "OS-06": 500.0,  "OS-07": 80.0,  "OS-08": 950.0, "OS-09": 400.0, "OS-10": 60.0,
    "OS-11": 1500.0, "OS-12": 200.0, "OS-13": 90.0,  "OS-14": 600.0, "OS-15": 1100.0,
    "OS-16": 450.0,  "OS-17": 150.0, "OS-18": 55.0,  "OS-19": 750.0, "OS-20": 1300.0
}

## Índice de Eficiencia Relativa del Operador (IER) ∈ [0.0, 1.0]
catalogo_ier: Dict[str, float] = {
    "OP-01": 0.95, "OP-02": 0.88, "OP-03": 0.75, "OP-04": 0.92, "OP-05": 0.60,
    "OP-06": 0.81, "OP-07": 0.99, "OP-08": 0.70, "OP-09": 0.85, "OP-10": 0.91,
    "OP-11": 0.65, "OP-12": 0.89, "OP-13": 0.77, "OP-14": 0.94, "OP-15": 0.82,
    "OP-16": 0.68, "OP-17": 0.97, "OP-18": 0.84, "OP-19": 0.72, "OP-20": 0.90,
    "OP-21": 0.55, "OP-22": 0.86, "OP-23": 0.79, "OP-24": 0.93, "OP-25": 0.64,
    "OP-26": 0.87, "OP-27": 0.96, "OP-28": 0.71, "OP-29": 0.83, "OP-30": 0.80,
    "OP-31": 0.98, "OP-32": 0.62, "OP-33": 0.78, "OP-34": 0.88, "OP-35": 0.91
}

## Estatus legal del operador (True=Vigente, False=Vencido/Vacaciones/Inhabilitado)
licencias_vigentes: Dict[str, bool] = {
    "OP-01": True,  "OP-02": True,  "OP-03": True,  "OP-04": False, "OP-05": False,
    "OP-06": True,  "OP-07": True,  "OP-08": False, "OP-09": True,  "OP-10": True,
    "OP-11": True,  "OP-12": True,  "OP-13": True,  "OP-14": True,  "OP-15": False,
    "OP-16": True,  "OP-17": True,  "OP-18": True,  "OP-19": False, "OP-20": True,
    "OP-21": False, "OP-22": True,  "OP-23": True,  "OP-24": True,  "OP-25": False,
    "OP-26": True,  "OP-27": True,  "OP-28": False, "OP-29": True,  "OP-30": True,
    "OP-31": True,  "OP-32": False, "OP-33": True,  "OP-34": True,  "OP-35": False
}

## Factor de Rendimiento de la Unidad (FRD) en km/L
catalogo_frd: Dict[str, float] = {
    "UNI-01": 4.5, "UNI-02": 3.8, "UNI-03": 2.9, "UNI-04": 4.1, "UNI-05": 3.5,
    "UNI-06": 4.8, "UNI-07": 3.2, "UNI-08": 2.5, "UNI-09": 4.6, "UNI-10": 3.9,
    "UNI-11": 4.0, "UNI-12": 3.1, "UNI-13": 2.8, "UNI-14": 4.3, "UNI-15": 3.7,
    "UNI-16": 4.9, "UNI-17": 3.4, "UNI-18": 2.6, "UNI-19": 4.2, "UNI-20": 3.6,
    "UNI-21": 4.7, "UNI-22": 3.0, "UNI-23": 2.7, "UNI-24": 4.4, "UNI-25": 3.3,
    "UNI-26": 5.0, "UNI-27": 3.8, "UNI-28": 2.4, "UNI-29": 4.1, "UNI-30": 3.5,
    "UNI-31": 5.2, "UNI-32": 2.2, "UNI-33": 3.9, "UNI-34": 4.6, "UNI-35": 3.1
}

## Estatus Operativo de la Unidad
estado_unidades: Dict[str, str] = {
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


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 2 — PARÁMETROS DE CONTROL DEL ALGORITMO GENÉTICO
# ─────────────────────────────────────────────────────────────────────────────

TAMANIO_POBLACION: int  = 50      # N  — individuos por generación
GENERACIONES: int       = 200     # G  — condición de paro (máx. generaciones)
TASA_CRUCE: float       = 0.80    # Pc — probabilidad de cruzamiento por pareja
TASA_MUTACION: float    = 0.15    # Pm — probabilidad de mutación por individuo
TAMANIO_TORNEO: int     = 3       # k  — tamaño del subconjunto para torneo

# Coeficientes de ponderación de la función objetivo
W1: float = 1.0      # Peso de la evaluación del recurso humano  Eop(o,s)
W2: float = 0.002    # Peso de la evaluación del recurso mecánico Eun(u,s)
# Nota: W2 << W1 porque Eun opera en la escala km·(km/L) ≈ [99, 7800],
#       mientras Eop opera en IER·IC ≈ [0.55, 4.95]. Los pesos compensan
#       la diferencia de magnitud entre ambos criterios de optimización.

# Coeficientes de penalización exterior
LAMBDA_D: float = 500.0    # λD — penalización por disponibilidad física
LAMBDA_L: float = 1000.0   # λL — penalización por incumplimiento legal/documental


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 3 — TIPOS Y ESTRUCTURAS AUXILIARES
# ─────────────────────────────────────────────────────────────────────────────

# Tipo: cromosoma = lista ordenada de n tuplas (OS, OP, UNI)
Individuo = List[Tuple[str, str, str]]

# Listas planas del catálogo para muestreo aleatorio eficiente
_LISTA_OPERADORES: List[str] = list(catalogo_ier.keys())
_LISTA_UNIDADES:   List[str] = list(catalogo_frd.keys())


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 4 — PASO 1: INICIALIZACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def crear_individuo(ordenes: List[str]) -> Individuo:
    """
    Construye un individuo (agenda diaria) asignando recursos mediante
    muestreo aleatorio SIN reemplazo.

    Garantía estructural: ningún operador ni ninguna unidad se repite
    dentro de la misma agenda (restricción de exclusividad diaria).

    Args:
        ordenes: Lista de IDs de Órdenes de Servicio (s₁ … sₙ) del día.

    Returns:
        Individuo: lista de n tuplas [(s₁,o₁,u₁), …, (sₙ,oₙ,uₙ)].
    """
    n    = len(ordenes)
    ops  = random.sample(_LISTA_OPERADORES, n)  # sin reemplazo → sin duplicados
    unis = random.sample(_LISTA_UNIDADES,   n)
    return [(ordenes[i], ops[i], unis[i]) for i in range(n)]


def inicializar_poblacion(
    ordenes: List[str],
    tam: int = TAMANIO_POBLACION
) -> List[Individuo]:
    """
    Genera la población inicial de tamaño N mediante llamadas sucesivas
    a crear_individuo(). Cada individuo es independiente (distinto muestreo).

    Args:
        ordenes: IDs de las Órdenes de Servicio del día.
        tam:     Tamaño N de la población.

    Returns:
        Lista de N individuos (agendas diarias candidatas).
    """
    return [crear_individuo(ordenes) for _ in range(tam)]


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 5 — PASO 2: EVALUACIÓN (Función Objetivo + Penalización Exterior)
# ─────────────────────────────────────────────────────────────────────────────

def evaluar_operador(op: str, os: str) -> float:
    """
    Eop(o, s) = IER(o) × IC(s)

    Califica la calidad de emparejar el operador 'op' con el servicio 'os'.
    El producto es alto únicamente cuando AMBOS factores son altos
    simultáneamente: operador experimentado en servicio de alta importancia.

    Args:
        op: ID del operador asignado.
        os: ID de la Orden de Servicio.

    Returns:
        Valor escalar de evaluación del recurso humano.
    """
    return catalogo_ier[op] * catalogo_clientes[os]


def evaluar_unidad(uni: str, os: str) -> float:
    """
    Eun(u, s) = FR(u) × D(s)

    Califica el ahorro potencial de combustible al asignar la unidad 'uni'
    al servicio 'os'. El producto amplifica el beneficio de unidades
    eficientes en rutas largas donde el ahorro de diésel es mayor.

    Args:
        uni: ID de la unidad vehicular asignada.
        os:  ID de la Orden de Servicio.

    Returns:
        Valor escalar de evaluación del recurso mecánico.
    """
    return catalogo_frd[uni] * distancia_servicios[os]


def calcular_penalizacion(individuo: Individuo) -> Tuple[float, int, int]:
    """
    ΩA = λD × DA + λL × LA

    Contabiliza las violaciones de las reglas de negocio:
      DA — Disponibilidad física: unidades con estatus ≠ "Disponible"
           (En Mantenimiento, Taller Externo, Baja).
      LA — Cumplimiento legal:    operadores con licencia/examen vencido
           o inhabilitados (licencias_vigentes == False).

    Las soluciones infactibles no se descartan; reciben una reducción
    proporcional de aptitud que disminuye su probabilidad de selección
    (Método de Penalización Exterior).

    Args:
        individuo: Cromosoma a evaluar.

    Returns:
        Tupla (ΩA, DA, LA):
            ΩA  — valor total de penalización.
            DA  — contador de violaciones de disponibilidad física.
            LA  — contador de violaciones legales/documentales.
    """
    DA: int = 0
    LA: int = 0

    for (_, op, uni) in individuo:
        if estado_unidades[uni] != "Disponible":   # Violación de disponibilidad física
            DA += 1
        if not licencias_vigentes[op]:              # Violación legal/documental
            LA += 1

    omega = (LAMBDA_D * DA) + (LAMBDA_L * LA)
    return omega, DA, LA


def calcular_aptitud(individuo: Individuo) -> float:
    """
    F(A) = BeneficioA − ΩA

    BeneficioA = Σ_{(s,o,u) ∈ A} [ w1·Eop(o,s) + w2·Eun(u,s) ]

    Función escalar que el Algoritmo Genético busca maximizar.
    Un valor alto indica una agenda rentable Y operativamente válida.

    Args:
        individuo: Cromosoma (lista de tuplas) a evaluar.

    Returns:
        Aptitud F(A) del individuo.
    """
    beneficio = sum(
        W1 * evaluar_operador(op, os) + W2 * evaluar_unidad(uni, os)
        for (os, op, uni) in individuo
    )
    omega, _, _ = calcular_penalizacion(individuo)
    return beneficio - omega


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 6 — PASO 4: SELECCIÓN (Torneo Determinístico)
# ─────────────────────────────────────────────────────────────────────────────

def seleccion_torneo(
    poblacion: List[Individuo],
    aptitudes: List[float],
    k: int = TAMANIO_TORNEO
) -> Individuo:
    """
    Torneo Determinístico de tamaño k.

    Extrae aleatoriamente k individuos de la población y retorna una copia
    del que posea la mayor aptitud F(A). Al ser determinístico, siempre
    gana el mejor del subconjunto: no intervienen probabilidades adicionales.

    Ventaja para este modelo: los individuos infactibles con penalizaciones
    acumuladas perderán consistentemente, guiando la búsqueda hacia la
    región de soluciones válidas de forma natural y automática.

    Args:
        poblacion: Individuos de la generación actual.
        aptitudes: Vector de aptitudes F(A) correspondiente a cada individuo.
        k:         Tamaño del torneo (subconjunto competidor).

    Returns:
        Copia profunda del individuo ganador (mayor aptitud del torneo).
    """
    competidores = random.sample(range(len(poblacion)), k)
    ganador      = max(competidores, key=lambda i: aptitudes[i])
    return copy.deepcopy(poblacion[ganador])


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 7 — PASO 5: CRUZAMIENTO + REPARACIÓN ESTRUCTURAL
# ─────────────────────────────────────────────────────────────────────────────

def _reparar_recurso(
    individuo: List[Tuple[str, str, str]],
    catalogo:  List[str],
    pos:       int
) -> List[Tuple[str, str, str]]:
    """
    Mecanismo de reparación de duplicados para un tipo de recurso.

    Detecta posiciones con recursos repetidos en el cromosoma y los
    sustituye con recursos libres del catálogo, restaurando la restricción
    de exclusividad diaria (cada recurso aparece a lo sumo una vez).

    Algoritmo:
        1. Primera pasada: identificar duplicados y construir conjunto de
           recursos ya asignados.
        2. Calcular conjunto de recursos libres (catálogo − asignados).
        3. Segunda pasada: reemplazar cada duplicado con un recurso libre
           elegido al azar.

    Args:
        individuo: Cromosoma mutable sobre el que se opera.
        catalogo:  Lista completa de IDs del catálogo del recurso a reparar
                   (_LISTA_OPERADORES para pos=1, _LISTA_UNIDADES para pos=2).
        pos:       Posición del recurso dentro de la tupla (1=OP, 2=UNI).

    Returns:
        Individuo con duplicados corregidos (misma referencia de lista).
    """
    asignados:  set  = set()
    duplicados: List[int] = []

    # Primera pasada: detectar qué posiciones tienen recursos ya vistos
    for idx, tupla in enumerate(individuo):
        recurso = tupla[pos]
        if recurso in asignados:
            duplicados.append(idx)
        else:
            asignados.add(recurso)

    if not duplicados:
        return individuo  # Sin duplicados: retornar sin modificaciones

    # Recursos disponibles para sustitución (presentes en catálogo, no en agenda)
    libres = [r for r in catalogo if r not in asignados]
    random.shuffle(libres)

    # Segunda pasada: sustituir cada posición duplicada con un recurso libre
    for idx in duplicados:
        if not libres:
            break  # Catálogo exhausto: detener reparación (caso extremo)
        sustituto = libres.pop()
        asignados.add(sustituto)
        s, op, uni = individuo[idx]
        individuo[idx] = (s, sustituto, uni) if pos == 1 else (s, op, sustituto)

    return individuo


def cruzamiento_uniforme(
    padre1: Individuo,
    padre2: Individuo
) -> Tuple[Individuo, Individuo]:
    """
    Cruzamiento Uniforme con herencia íntegra de tupla.

    Para cada posición i ∈ [0, n) se lanza una moneda (P=0.5) y se decide
    si hijo1 hereda la tupla de padre1 o de padre2 (hijo2 hereda la opuesta).
    La TUPLA COMPLETA se transfiere de forma indivisible, preservando el
    acoplamiento operador-unidad construido en generaciones anteriores.

    Inmediatamente después del cruce se ejecuta la verificación estructural:
    se reparan duplicados de operadores y de unidades de forma independiente,
    garantizando que cada recurso aparezca a lo sumo una vez en la agenda.

    Args:
        padre1: Primer progenitor.
        padre2: Segundo progenitor.

    Returns:
        (hijo1, hijo2): par de descendientes reparados y listos para evaluación.
    """
    n = len(padre1)
    hijo1: List[Tuple[str, str, str]] = []
    hijo2: List[Tuple[str, str, str]] = []

    # Recombinación uniforme tupla por tupla
    for i in range(n):
        if random.random() < 0.5:
            hijo1.append(padre1[i])
            hijo2.append(padre2[i])
        else:
            hijo1.append(padre2[i])
            hijo2.append(padre1[i])

    # Reparación estructural: primero operadores (pos=1), luego unidades (pos=2)
    hijo1 = _reparar_recurso(hijo1, _LISTA_OPERADORES, 1)
    hijo1 = _reparar_recurso(hijo1, _LISTA_UNIDADES,   2)

    hijo2 = _reparar_recurso(hijo2, _LISTA_OPERADORES, 1)
    hijo2 = _reparar_recurso(hijo2, _LISTA_UNIDADES,   2)

    return hijo1, hijo2


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 8 — PASO 6: MUTACIÓN (Reinicio Aleatorio Puro)
# ─────────────────────────────────────────────────────────────────────────────

def mutacion_reinicio_aleatorio(individuo: Individuo) -> Individuo:
    """
    Mutación por Reinicio Aleatorio (Random Resetting).

    Selecciona una tupla al azar y reemplaza su OPERADOR o su UNIDAD por
    un recurso completamente nuevo extraído del catálogo general, inyectando
    material genético externo al individuo para evitar óptimos locales.

    Validación aplicada (solo estructural):
      ✓ El nuevo recurso no duplica a ningún otro ya presente en la agenda.
      ✗ NO se pre-valida estatus legal u operativo del recurso inyectado.
        Esta validación se delega al Paso 2 (función de penalización) en la
        siguiente generación, justificando matemáticamente la existencia de λD y λL.

    Args:
        individuo: Cromosoma a mutar.

    Returns:
        Nuevo cromosoma con la mutación aplicada (lista nueva).
    """
    mutado = list(individuo)         # copia superficial de la lista de tuplas
    idx    = random.randrange(len(mutado))
    s, op, uni = mutado[idx]

    if random.randint(0, 1) == 0:
        # --- Mutar el OPERADOR ---
        ops_ocupados = {t[1] for t in mutado} - {op}   # excluir el actual
        candidatos   = [o for o in _LISTA_OPERADORES if o not in ops_ocupados]
        if candidatos:
            mutado[idx] = (s, random.choice(candidatos), uni)
    else:
        # --- Mutar la UNIDAD ---
        unis_ocupadas = {t[2] for t in mutado} - {uni}  # excluir la actual
        candidatos    = [u for u in _LISTA_UNIDADES if u not in unis_ocupadas]
        if candidatos:
            mutado[idx] = (s, op, random.choice(candidatos))

    return mutado


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 9 — ALGORITMO GENÉTICO COMPLETO (Pasos 1–7)
# ─────────────────────────────────────────────────────────────────────────────

def algoritmo_genetico(
    ordenes:       List[str],
    tam_poblacion: int   = TAMANIO_POBLACION,
    generaciones:  int   = GENERACIONES,
    tasa_cruce:    float = TASA_CRUCE,
    tasa_mutacion: float = TASA_MUTACION,
    k_torneo:      int   = TAMANIO_TORNEO,
    verbose:       bool  = True
) -> Tuple[Individuo, float, List[float]]:
    """
    Ejecuta el Algoritmo Genético para la asignación óptima de recursos
    en la programación de servicios de transporte.

    ┌─ Flujo evolutivo ────────────────────────────────────────────────────┐
    │  1. Inicialización  → población aleatoria sin duplicados             │
    │  2. Evaluación      → F(A) = Σ(w1·Eop + w2·Eun) − ΩA               │
    │  3. Elitismo        → copiar y preservar el mejor individuo          │
    │  4. Selección       → torneo determinístico de tamaño k              │
    │  5. Cruzamiento     → uniforme por tupla + reparación estructural    │
    │  6. Mutación        → reinicio aleatorio puro (sin pre-validación)   │
    │  7. Reemplazo       → generacional extintivo + élite                 │
    │     └─ ¿Gen < G? → volver a Paso 2   |   ¿Gen = G? → retornar      │
    └──────────────────────────────────────────────────────────────────────┘

    Args:
        ordenes:       IDs de las Órdenes de Servicio del día a programar.
        tam_poblacion: Tamaño N de la población.
        generaciones:  Número máximo de generaciones (condición de paro).
        tasa_cruce:    Probabilidad Pc de aplicar cruzamiento a una pareja.
        tasa_mutacion: Probabilidad Pm de mutar un individuo descendiente.
        k_torneo:      Tamaño k del torneo de selección de padres.
        verbose:       Imprimir progreso cada 10 generaciones si es True.

    Returns:
        Tupla (mejor_individuo, mejor_aptitud, historial):
          mejor_individuo — Agenda óptima encontrada (cromosoma completo).
          mejor_aptitud   — Valor máximo de F(A) alcanzado en toda la ejecución.
          historial       — Lista con el F(A) máximo por cada generación
                            (curva de convergencia del algoritmo).
    """
    # ── PASO 1: Inicialización ──────────────────────────────────────────────
    poblacion: List[Individuo] = inicializar_poblacion(ordenes, tam_poblacion)

    mejor_individuo: Optional[Individuo] = None
    mejor_aptitud:   float               = float("-inf")
    historial:       List[float]         = []

    for gen in range(generaciones):

        # ── PASO 2: Evaluación ─────────────────────────────────────────────
        aptitudes: List[float] = [calcular_aptitud(ind) for ind in poblacion]

        # ── PASO 3: Elitismo ───────────────────────────────────────────────
        # Identificar el mejor individuo de la generación actual y resguardarlo
        idx_elite  = max(range(tam_poblacion), key=lambda i: aptitudes[i])
        elite      = copy.deepcopy(poblacion[idx_elite])
        apt_elite  = aptitudes[idx_elite]

        # Actualizar el mejor global si la generación actual lo supera
        if apt_elite > mejor_aptitud:
            mejor_aptitud   = apt_elite
            mejor_individuo = copy.deepcopy(elite)

        historial.append(mejor_aptitud)

        if verbose and (gen % 10 == 0 or gen == generaciones - 1):
            print(f"  Gen {gen + 1:>4}/{generaciones}  │  "
                  f"Élite actual: {apt_elite:>10.4f}  │  "
                  f"Mejor global: {mejor_aptitud:>10.4f}")

        # ── PASOS 4, 5, 6: Reproducción ────────────────────────────────────
        # El élite ocupa la primera plaza (elitismo). Se producen (N-1)
        # descendientes adicionales mediante selección → cruce → mutación.
        nueva_poblacion: List[Individuo] = [elite]

        while len(nueva_poblacion) < tam_poblacion:

            # Paso 4 — Selección de dos progenitores por torneo determinístico
            padre1 = seleccion_torneo(poblacion, aptitudes, k_torneo)
            padre2 = seleccion_torneo(poblacion, aptitudes, k_torneo)

            # Paso 5 — Cruzamiento uniforme con reparación estructural
            if random.random() < tasa_cruce:
                hijo1, hijo2 = cruzamiento_uniforme(padre1, padre2)
            else:
                # Sin cruzamiento: los hijos son copias exactas de los padres
                hijo1 = copy.deepcopy(padre1)
                hijo2 = copy.deepcopy(padre2)

            # Paso 6 — Mutación por reinicio aleatorio puro
            if random.random() < tasa_mutacion:
                hijo1 = mutacion_reinicio_aleatorio(hijo1)
            if random.random() < tasa_mutacion:
                hijo2 = mutacion_reinicio_aleatorio(hijo2)

            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < tam_poblacion:
                nueva_poblacion.append(hijo2)

        # ── PASO 7: Reemplazo generacional extintivo ───────────────────────
        # Toda la generación anterior se reemplaza por la nueva descendencia.
        # El élite, ya insertado en nueva_poblacion[0], actúa como escudo.
        poblacion = nueva_poblacion

    return mejor_individuo, mejor_aptitud, historial


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 10 — REPORTE DE RESULTADOS
# ─────────────────────────────────────────────────────────────────────────────

def imprimir_reporte(individuo: Individuo, aptitud: float) -> None:
    """
    Imprime un reporte tabular detallado de la mejor agenda logística
    encontrada por el algoritmo, con métricas individuales por servicio
    y un resumen global de beneficio, penalización y aptitud neta.

    Args:
        individuo: Mejor cromosoma retornado por el AG.
        aptitud:   Aptitud F(A) del individuo.
    """
    SEP_D = "─" * 104
    SEP_D2 = "═" * 104

    print(f"\n{SEP_D2}")
    print(f"  REPORTE DE AGENDA ÓPTIMA LOGÍSTICA")
    print(f"  Aptitud Final  F(A) = {aptitud:,.4f}")
    print(f"{SEP_D2}")
    print(
        f"  {'OS':^7}  {'OP':^7}  {'IER':^5}  {'Lic.':^4}  "
        f"{'UNI':^8}  {'FRD':^5}  {'Estado Unidad':^17}  "
        f"{'IC':^3}  {'Dist (km)':^10}  "
        f"{'Eop':^6}  {'Eun':^8}  Notas"
    )
    print(f"  {SEP_D}")

    beneficio_bruto = 0.0
    DA_total        = 0
    LA_total        = 0

    for (os, op, uni) in individuo:
        ier  = catalogo_ier[op]
        ic   = catalogo_clientes[os]
        frd  = catalogo_frd[uni]
        dist = distancia_servicios[os]
        lic  = licencias_vigentes[op]
        est  = estado_unidades[uni]

        eop = evaluar_operador(op, os)
        eun = evaluar_unidad(uni, os)
        beneficio_bruto += W1 * eop + W2 * eun

        notas = []
        if not lic:
            notas.append("⚠ LIC.VENCIDA")
            LA_total += 1
        if est != "Disponible":
            notas.append(f"⚠ {est.upper()}")
            DA_total += 1

        lic_tag   = "✓" if lic else "✗"
        notas_str = "  ".join(notas) if notas else "OK"

        print(
            f"  {os:^7}  {op:^7}  {ier:.2f}  {lic_tag:^4}  "
            f"{uni:^8}  {frd:.1f}  {est:^17}  "
            f"{ic:^3}  {dist:>10.1f}  "
            f"{eop:>6.3f}  {eun:>8.1f}  {notas_str}"
        )

    penalizacion = LAMBDA_D * DA_total + LAMBDA_L * LA_total
    print(f"  {SEP_D}")
    print(f"  Beneficio Bruto  BeneficioA  = Σ(w1·Eop + w2·Eun)              = {beneficio_bruto:>12.4f}")
    print(f"  Penalización     ΩA          = λD({LAMBDA_D:.0f})×DA({DA_total}) + λL({LAMBDA_L:.0f})×LA({LA_total}) = {penalizacion:>12.4f}")
    print(f"  Aptitud Neta     F(A)        = BeneficioA − ΩA                  = {beneficio_bruto - penalizacion:>12.4f}")
    print(f"{SEP_D2}\n")


def imprimir_convergencia(historial: List[float]) -> None:
    """
    Imprime un resumen de la curva de convergencia del AG, mostrando
    el valor de F(A) máximo en cinco puntos clave de la ejecución.

    Args:
        historial: Lista de aptitudes máximas por generación.
    """
    g = len(historial)
    print("  CURVA DE CONVERGENCIA DEL ALGORITMO:")
    print(f"  {'Generación':^12}  {'F(A) Máxima':^16}")
    print(f"  {'─'*12}  {'─'*16}")

    hitos = sorted(set([0, g // 4, g // 2, 3 * g // 4, g - 1]))
    for h in hitos:
        print(f"  {h + 1:^12}  {historial[h]:>16.4f}")

    mejora = historial[-1] - historial[0]
    print(f"\n  Mejora total (Gen 1 → Gen {g}): {mejora:+.4f}\n")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 11 — PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Definir las Órdenes de Servicio del día (todas las del catálogo)
    ordenes_del_dia: List[str] = list(catalogo_clientes.keys())  # OS-01 … OS-20

    print("\n" + "═" * 72)
    print("  OPTIMIZACIÓN LOGÍSTICA — ALGORITMO GENÉTICO DE ASIGNACIÓN")
    print("═" * 72)
    print(f"  Servicios del día  : {len(ordenes_del_dia)} órdenes")
    print(f"  Operadores en cat. : {len(_LISTA_OPERADORES)}")
    print(f"  Unidades en cat.   : {len(_LISTA_UNIDADES)}")
    print("─" * 72)
    print(f"  Tamaño de población N  = {TAMANIO_POBLACION}")
    print(f"  Generaciones máx.  G  = {GENERACIONES}")
    print(f"  Tasa de cruce      Pc = {TASA_CRUCE}")
    print(f"  Tasa de mutación   Pm = {TASA_MUTACION}")
    print(f"  Tamaño de torneo   k  = {TAMANIO_TORNEO}")
    print("─" * 72)
    print(f"  Pesos FO : w1 = {W1}  |  w2 = {W2}")
    print(f"  Penal.   : λD = {LAMBDA_D:.0f}  |  λL = {LAMBDA_L:.0f}")
    print("═" * 72)
    print("\n  Evolucionando...\n")

    mejor_agenda, aptitud_final, historial_aptitud = algoritmo_genetico(
        ordenes       = ordenes_del_dia,
        tam_poblacion = TAMANIO_POBLACION,
        generaciones  = GENERACIONES,
        tasa_cruce    = TASA_CRUCE,
        tasa_mutacion = TASA_MUTACION,
        k_torneo      = TAMANIO_TORNEO,
        verbose       = True
    )

    imprimir_reporte(mejor_agenda, aptitud_final)
    imprimir_convergencia(historial_aptitud)