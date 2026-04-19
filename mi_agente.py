"""
mi_agente.py — Aquí defines tu agente.
╔══════════════════════════════════════════════╗
║  ✏️  EDITA ESTE ARCHIVO                      ║
╚══════════════════════════════════════════════╝

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el método decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
───────────────────────────────
percepcion = {
    'posicion':       (3, 5),          # Tu fila y columna actual
    'arriba':         'libre',         # Qué hay arriba
    'abajo':          'pared',         # Qué hay abajo
    'izquierda':      'libre',         # Qué hay a la izquierda
    'derecha':        None,            # None = fuera del mapa

    # OPCIONAL — brújula hacia la meta.
    # No es percepción real del entorno, es información global.
    # Usarla hace el ejercicio más fácil. No usarla es más realista.
    'direccion_meta': ('abajo', 'derecha'),
}

Valores posibles de cada dirección:
    'libre'  → puedes moverte ahí
    'pared'  → bloqueado
    'meta'   → ¡la meta! ve hacia allá
    None     → borde del mapa, no puedes ir

Si tu agente retorna un movimiento inválido (hacia pared o
fuera del mapa), simplemente se queda en su lugar.
"""

from entorno import Agente


class MiAgente(Agente):
    """
    Tu agente de navegación.

    Implementa el método decidir() para que el agente
    llegue del punto A al punto B en el grid.
    """

    def __init__(self):
        super().__init__(nombre="Mi Agente")
        # Puedes agregar atributos aquí si los necesitas.
        self.visitados = set()

    def al_iniciar(self):
        """Se llama una vez al iniciar la simulación. Opcional."""
        self.visitados.clear()

    def decidir(self, percepcion):
        
        """
        Decide la siguiente acción del agente.
        
        Parámetros:
            percepcion – diccionario con lo que el agente puede ver

        Retorna:
            'arriba', 'abajo', 'izquierda' o 'derecha'
        """
        # ╔══════════════════════════════════════╗
        # ║   ESCRIBE TU LÓGICA AQUÍ             ║
        # ╚══════════════════════════════════════╝

        pos_actual = percepcion['posicion']
        self.visitados.add(pos_actual)

        mejor_movimiento = None
        mejor_puntaje = -999

        for direccion in self.ACCIONES:
            estado = percepcion[direccion]

            # Ignorar paredes o bordes
            if estado not in ['libre', 'meta']:
                continue

            # Si es la meta → prioridad máxima
            if estado == 'meta':
                return direccion

            # Calcular posición futura
            df, dc = self.DELTAS[direccion]
            nueva_pos = (pos_actual[0] + df, pos_actual[1] + dc)

            puntaje = 0

            # 1. Acercarse a la meta (usar brújula)
            if percepcion.get('direccion_meta') and direccion in percepcion['direccion_meta']:
                puntaje += 5

            # 2. Evitar repetir posiciones
            if nueva_pos in self.visitados:
                puntaje -= 3
            else:
                puntaje += 2

            # 3. Pequeño incentivo por moverse
            puntaje += 1

            # Elegir mejor opción
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_movimiento = direccion

        if mejor_movimiento:
            return mejor_movimiento

        # fallback
        return 'abajo'