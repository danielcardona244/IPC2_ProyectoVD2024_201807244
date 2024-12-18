import os

# Definición de la clase Nodo
class Nodo:
    def __init__(self, valor):
        self.valor = valor  # Almacena el objeto Solicitante
        self.siguiente = None
        self.anterior = None

# Definición de la clase ListaDoble
class ListaDoble:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        """
        Retorna el tamaño actual de la lista.
        """
        return self.tamanio

    def insertar(self, valor):
        """
        Inserta un nuevo nodo al final de la lista.
        """
        nuevo = Nodo(valor)
        if self.primero is None and self.ultimo is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
        self.tamanio += 1

    def buscar(self, id):
        """
        Busca si un ID ya existe en la lista.
        """
        actual = self.primero
        while actual:
            if actual.valor.id == id:  # Comparación con el ID del solicitante
                return True
            actual = actual.siguiente
        return False

    def imprimirListaHaciaAdelante(self):
        """
        Imprime la lista desde el inicio hacia el final.
        """
        actual = self.primero
        while actual:
            print(actual.valor)  # Llama a __str__ de la clase Solicitante
            actual = actual.siguiente

    def graficar(self):
        """
        Genera un archivo .dot y una imagen de la lista doblemente enlazada.
        """
        if self.primero is None:
            print("La lista está vacía. No se puede generar la gráfica.")
            return

        codigo_dot = 'digraph G {\n'
        codigo_dot += '    rankdir=LR;\n'
        codigo_dot += '    node [shape=record];\n\n'

        actual = self.primero
        contador = 0
        while actual:
            codigo_dot += f'    node{contador} [label="ID: {actual.valor.id} | Nombre: {actual.valor.nombre}"];\n'
            if actual.siguiente:
                codigo_dot += f'    node{contador} -> node{contador+1} [dir=both];\n'
            contador += 1
            actual = actual.siguiente

        codigo_dot += "}"

        if not os.path.exists("Reportes"):
            os.makedirs("Reportes")
        if not os.path.exists("reportesdot"):
            os.makedirs("reportesdot")

        ruta_dot = "reportesdot/ListaSolicitantes.dot"
        with open(ruta_dot, "w") as archivo:
            archivo.write(codigo_dot)

        ruta_imagen = "Reportes/ListaSolicitantes.svg"
        os.system(f'dot -Tsvg {ruta_dot} -o {ruta_imagen}')
        os.startfile(os.path.abspath(ruta_imagen))
        print("Gráfica generada en:", ruta_imagen)
