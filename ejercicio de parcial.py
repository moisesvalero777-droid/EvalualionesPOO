#crear una clases bateria que me permita instanciar una bateria y demostrar el uso de copy.deepcopy modificando la copia sin afectar la origina·
#crear nodo bateria y lista bateria cun unico puntero cabeza, emplementar los metodos y insertar al inicio y purgar agotadas el cual debe recorrer la lista y reconectar los punteros y elimine las baterias con menos de 3 voltios.
import copy
from typing import Callable, Optional


class Bateria:
    """Representa un dispositivo físico de medición de voltaje"""

    def __init__(self, id_bateria: str, voltaje: float) -> None:
        self.id_bateria: str = id_bateria
        self.voltaje: float = voltaje


def alerta_sobrevoltaje(bateria: Bateria) -> None:
    """Función Callback para eventos de alto voltaje (> 3.0V)."""
    print(
        f"   [ALERTA DE SEGURIDAD]: {bateria.id_bateria} registró {bateria.voltaje}V (Límite superado)"
    )


class NodoBateria:
    """Clase autoreferenciada para la estructura dinámica en la RAM"""

    def __init__(self, id_Bateria: Bateria) -> None:
        self.Bateria: Bateria = id_Bateria
        self.siguiente: Optional["NodoBateria"] = None


class ListaBateria:
    """Estructura dinámicamente enlazada"""

    def __init__(self) -> None:
        self.frente: Optional[NodoBateria] = None
        self.final: Optional[NodoBateria] = None

    def encolar_lectura(
        self,
        Bateria: Bateria,
        callback_alerta: Optional[Callable[[Bateria], None]] = None,
    ) -> None:
        """Encola una nueva lectura en la RAM e invoca el callback si aplica."""
        nuevo_nodo = NodoBateria(Bateria)

        if callback_alerta and Bateria.voltaje < 3.0:
            callback_alerta(Bateria)

        if self.final is None:
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo

        print(f"-> [ENCOLA]: {Bateria.id_bateria} ({Bateria.voltaje}V) almacenado en RAM.")

    def purgar_lecturas_ruidosas(self, umbral_minimo: float) -> None:
        """Elimina nodos menores al umbral y reconecta punteros para el Garbage Collector."""
        
        # CASO 1: Purgar elementos ubicados al INICIO (frente) de la cola
        while self.frente is not None and self.frente.Bateria.voltaje < umbral_minimo:
            print(f"-> [PURGA]: Descartando nodo inicial {self.frente.Bateria.id_bateria} ({self.frente.Bateria.voltaje}V)")
            self.frente = self.frente.siguiente  # El nodo viejo queda huérfano para el recolector de basura

        if self.frente is None:
            self.final = None
            print("-> [PURGA]: La cola ha quedado completamente vacía.")
            return

        # CASO 2: Purgar elementos en el cuerpo o final de la cola
        actual = self.frente
        while actual.siguiente is not None:
            if actual.siguiente.Bateria.voltaje < umbral_minimo:
                print(f"-> [PURGA]: Descartando nodo {actual.siguiente.Bateria.id_bateria} ({actual.siguiente.Bateria.voltaje}V)")
                
                # RECONEXIÓN DE PUNTEROS CLAVE:
                # Saltamos el nodo no deseado conectando el actual directamente con el siguiente del siguiente
                actual.siguiente = actual.siguiente.siguiente
            else:
                actual = actual.siguiente

        # CASO 3: Actualizar el puntero 'final' en caso de que el último nodo fuera eliminado
        temp = self.frente
        ultimo = None
        while temp is not None:
            ultimo = temp
            temp = temp.siguiente
        self.final = ultimo


# --- Bloque de Pruebas / Demostración ---
if __name__ == "__main__":
    print("=== INICIO DE PRUEBAS: BÚFER TELEMÉTRICO Y PURGA ===")
    
    # 1. Instanciar la cola de telemetría
    cola = ListaBateria()

    # 2. Crear sensores con diferentes niveles de voltaje
    s1 = Bateria("SENSOR_01", 2.1)  # Válido / < 3V (activa callback)
    s2 = Bateria("SENSOR_02", 5.6)  # Ruidoso / Bajo umbral
    s3 = Bateria("SENSOR_03", 1.5)  # Válido / < 3V (activa callback)
    s4 = Bateria("SENSOR_04", 4.2)  # Ruidoso / Bajo umbral

    # 3. Encolar lecturas evaluando la alerta de sobrevoltaje
    cola.encolar_lectura(s1, alerta_sobrevoltaje)
    cola.encolar_lectura(s2, alerta_sobrevoltaje)
    cola.encolar_lectura(s3, alerta_sobrevoltaje)
    cola.encolar_lectura(s4, alerta_sobrevoltaje)

    # 4. Ejecutar la purga de memoria descartando voltajes menores a 3.0V
    print("\n--- EJECUTANDO PURGA (Umbral mínimo: 3.0V) ---")
    cola.purgar_lecturas_ruidosas(3.0)
    print("=== PRUEBA FINALIZADA CON ÉXITO ===")