class NodoDecision:
    def __init__(self, estado, entrada=None, padre=None):
        self.estado = estado
        self.entrada = entrada
        self.padre = padre
        self.hijos = []
        self.resultado = None
        # Nuevos atributos para Monty Hall
        self.puerta_premiada = None
        self.puerta_seleccionada = None

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)
        hijo.padre = self

    def __str__(self):
        return f"{self.estado} [{self.entrada}]"