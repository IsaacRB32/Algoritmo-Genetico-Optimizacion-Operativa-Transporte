## Proyecto Algoritmo Genético para Optimización de Transporte
## Garcia Picazo Erick
## Rios Gomez Juan Esteban
## Rojas Barron Isaac
import random
import copy
from typing import List, Tuple, Dict, Optional


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


## Parametros para el algoritmo genetico
TAMANIO_POBLACION: int  = 50    
GENERACIONES: int       = 200   
TASA_CRUCE: float       = 0.80   
TASA_MUTACION: float    = 0.15  
TAMANIO_TORNEO: int     = 3   

# Constantes de normalización de la función objetivo
# Definen el techo teórico de cada criterio para proyectarlo al rango [0, 1]
EOP_MAX: float = 0.99 * 5      #  max(IER) x max(IC)
EUN_MAX: float = 5.2  * 1500   #  max(FRD) x max(D)

# Coeficientes de ponderacion
# w1 + w2 = 1.0: pesos proporcionales directos sobre criterios normalizados
W1: float = 0.3   # % de peso del criterio humano
W2: float = 0.7   # % depeso del criterio mecanico 

# Coeficientes de penalizacion exterior (escala normalizada: max beneficio aprox 20)
LAMBDA_D: float = 5.0    # penalizacion por disponibilidad fisica
LAMBDA_L: float = 10.0   # penalizacion por incumplimiento legal/documental


# Tipo: cromosoma = lista ordenada de n tuplas (OS, OP, UNI)
Individuo = List[Tuple[str, str, str]]

# Listas planas del catálogo para muestreo aleatorio eficiente
_LISTA_OPERADORES: List[str] = list(catalogo_ier.keys())
_LISTA_UNIDADES:   List[str] = list(catalogo_frd.keys())


def crear_individuo(ordenes: List[str]) -> Individuo:
    n    = len(ordenes)
    ops  = random.sample(_LISTA_OPERADORES, n)
    unis = random.sample(_LISTA_UNIDADES,   n)
    return [(ordenes[i], ops[i], unis[i]) for i in range(n)]


def inicializar_poblacion(
    ordenes: List[str],
    tam: int = TAMANIO_POBLACION
) -> List[Individuo]:

    return [crear_individuo(ordenes) for _ in range(tam)]


def evaluar_operador(op: str, os: str) -> float:
    ## Eop(o, s) = IER(o) × IC(s)
    return catalogo_ier[op] * catalogo_clientes[os]


def evaluar_unidad(uni: str, os: str) -> float:

    ##  Eun(u, s) = FR(u) × D(s)
    return catalogo_frd[uni] * distancia_servicios[os]


def calcular_penalizacion(individuo: Individuo) -> Tuple[float, int, int]:

    ##ΩA = λD × DA + λL × LA

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
    ## F(A) = BeneficioA - OmegaA

    beneficio = sum(
        W1 * (evaluar_operador(op, os) / EOP_MAX) +
        W2 * (evaluar_unidad(uni, os)  / EUN_MAX)
        for (os, op, uni) in individuo
    )
    omega, _, _ = calcular_penalizacion(individuo)
    return beneficio - omega


def seleccion_torneo(
    poblacion: List[Individuo],
    aptitudes: List[float],
    k: int = TAMANIO_TORNEO
) -> Individuo:

    competidores = random.sample(range(len(poblacion)), k)
    ganador      = max(competidores, key=lambda i: aptitudes[i])
    return copy.deepcopy(poblacion[ganador])


def _reparar_recurso(
    individuo: List[Tuple[str, str, str]],
    catalogo:  List[str],
    pos:       int
) -> List[Tuple[str, str, str]]:

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


def mutacion_reinicio_aleatorio(individuo: Individuo) -> Individuo:

    mutado = list(individuo)         # copia superficial de la lista de tuplas
    idx    = random.randrange(len(mutado))
    s, op, uni = mutado[idx]

    if random.randint(0, 1) == 0:
        # Mutar el OPERADOR
        ops_ocupados = {t[1] for t in mutado} - {op}   # excluir el actual
        candidatos   = [o for o in _LISTA_OPERADORES if o not in ops_ocupados]
        if candidatos:
            mutado[idx] = (s, random.choice(candidatos), uni)
    else:
        # Mutar la UNIDAD
        unis_ocupadas = {t[2] for t in mutado} - {uni}  # excluir la actual
        candidatos    = [u for u in _LISTA_UNIDADES if u not in unis_ocupadas]
        if candidatos:
            mutado[idx] = (s, op, random.choice(candidatos))

    return mutado


def mutacion_intercambio(individuo: Individuo) -> Individuo:
    mutado = list(individuo)
    n = len(mutado)

    # Seleccionar dos posiciones distintas al azar
    idx1, idx2 = random.sample(range(n), 2)

    s1, op1, uni1 = mutado[idx1]
    s2, op2, uni2 = mutado[idx2]

    # 50% de probabilidad de intercambiar operadores, 50% de intercambiar unidades
    if random.random() < 0.5:
        mutado[idx1] = (s1, op2, uni1)  # Swap de operadores
        mutado[idx2] = (s2, op1, uni2)
    else:
        mutado[idx1] = (s1, op1, uni2)  # Swap de unidades
        mutado[idx2] = (s2, op2, uni1)

    return mutado
def algoritmo_genetico(
    ordenes:       List[str],
    tam_poblacion: int   = TAMANIO_POBLACION,
    generaciones:  int   = GENERACIONES,
    tasa_cruce:    float = TASA_CRUCE,
    tasa_mutacion: float = TASA_MUTACION,
    k_torneo:      int   = TAMANIO_TORNEO,
    verbose:       bool  = True
) -> Tuple[Individuo, float, List[float]]:

    poblacion: List[Individuo] = inicializar_poblacion(ordenes, tam_poblacion)

    mejor_individuo: Optional[Individuo] = None
    mejor_aptitud:   float               = float("-inf")
    historial:       List[float]         = []

    for gen in range(generaciones):

        aptitudes: List[float] = [calcular_aptitud(ind) for ind in poblacion]

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


        nueva_poblacion: List[Individuo] = [elite]

        while len(nueva_poblacion) < tam_poblacion:

            padre1 = seleccion_torneo(poblacion, aptitudes, k_torneo)
            padre2 = seleccion_torneo(poblacion, aptitudes, k_torneo)

            if random.random() < tasa_cruce:
                hijo1, hijo2 = cruzamiento_uniforme(padre1, padre2)
            else:
                # Sin cruzamiento: los hijos son copias exactas de los padres
                hijo1 = copy.deepcopy(padre1)
                hijo2 = copy.deepcopy(padre2)

            if random.random() < tasa_mutacion:
                if random.random() < 0.5:
                    hijo1 = mutacion_reinicio_aleatorio(hijo1)  # trae recursos nuevos
                else:
                    hijo1 = mutacion_intercambio(hijo1)          # reorganiza existentes

            if random.random() < tasa_mutacion:
                if random.random() < 0.5:
                    hijo2 = mutacion_reinicio_aleatorio(hijo2)
                else:
                    hijo2 = mutacion_intercambio(hijo2)

            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < tam_poblacion:
                nueva_poblacion.append(hijo2)


        poblacion = nueva_poblacion

    return mejor_individuo, mejor_aptitud, historial



def imprimir_reporte(individuo: Individuo, aptitud: float) -> None:

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
        f"{'Eop':^6}  {'Eun':^8}  {'Contrib':^7}  Notas"
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
        # Contribucion normalizada de esta tupla a la FO
        contrib = W1 * (eop / EOP_MAX) + W2 * (eun / EUN_MAX)
        beneficio_bruto += contrib

        notas = []
        if not lic:
            notas.append("LIC.VENCIDA")
            LA_total += 1
        if est != "Disponible":
            notas.append(f"{est.upper()}")
            DA_total += 1

        lic_tag   = "Si" if lic else "No"
        notas_str = "  ".join(notas) if notas else "OK"

        print(
            f"  {os:^7}  {op:^7}  {ier:.2f}  {lic_tag:^4}  "
            f"{uni:^8}  {frd:.1f}  {est:^17}  "
            f"{ic:^3}  {dist:>10.1f}  "
            f"{eop:>6.3f}  {eun:>8.1f}  {contrib:>6.4f}  {notas_str}"
        )

    penalizacion = LAMBDA_D * DA_total + LAMBDA_L * LA_total
    print(f"  {SEP_D}")
    print(f"  Beneficio Bruto  BeneficioA  = sum(w1*Eop/EOP_MAX + w2*Eun/EUN_MAX) = {beneficio_bruto:>8.4f}")
    print(f"  Penalizacion     OmegaA      = lambdaD({LAMBDA_D:.0f})*DA({DA_total}) + lambdaL({LAMBDA_L:.0f})*LA({LA_total})  = {penalizacion:>8.4f}")
    print(f"  Aptitud Neta     F(A)        = BeneficioA - OmegaA                   = {beneficio_bruto - penalizacion:>8.4f}")
    print(f"{SEP_D2}\n")


def imprimir_convergencia(historial: List[float]) -> None:

    g = len(historial)
    print("  CURVA DE CONVERGENCIA DEL ALGORITMO:")
    print(f"  {'Generación':^12}  {'F(A) Máxima':^16}")
    print(f"  {'─'*12}  {'─'*16}")

    hitos = sorted(set([0, g // 4, g // 2, 3 * g // 4, g - 1]))
    for h in hitos:
        print(f"  {h + 1:^12}  {historial[h]:>16.4f}")

    mejora = historial[-1] - historial[0]
    print(f"\n  Mejora total (Gen 1 → Gen {g}): {mejora:+.4f}\n")


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
    print(f"  Pesos FO : w1 = {W1} (humano)  |  w2 = {W2} (mecanico)  [normalizados]")
    print(f"  Penal.   : lambdaD = {LAMBDA_D:.0f}  |  lambdaL = {LAMBDA_L:.0f}  (escala normalizada)")
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