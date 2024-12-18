import os
from estructuras.lista_simple.nodo import Nodo

class ListaSimple:
    def __init__(self):
        self.primero = None
        self.tamanio = 0
    
    def __len__(self):
        return self.tamanio
    
    # Insertar al final de la lista
    def insertar(self, valor):
        if self.validarExiste(valor.id):
            return  # Evitar duplicados

        nuevo = Nodo(valor)
        if self.primero is None:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1

    # Validar si existe un ID
    def validarExiste(self, id):
        actual = self.primero
        while actual is not None:
            if actual.valor.id == id:
                return True
            actual = actual.siguiente
        return False

    # Imprimir la lista
    def imprimirLista(self):
        actual = self.primero
        while actual is not None:
            print(actual.valor)
            actual = actual.siguiente

    # Generar gráfico usando Graphviz
    def graficar(self):
        codigodot = '''digraph G {
    rankdir=LR;
    node[shape=record, height=.1]
    '''
        contador_nodos = 1
        actual = self.primero

        # Crear nodos
        while actual is not None:
            codigodot += f'nodo{contador_nodos}[label="{{{actual.valor}}}"];\n'
            actual = actual.siguiente
            contador_nodos += 1

        # Crear enlaces
        actual = self.primero
        contador_nodos = 1
        while actual is not None and actual.siguiente is not None:
            codigodot += f'nodo{contador_nodos} -> nodo{contador_nodos+1};\n'
            actual = actual.siguiente
            contador_nodos += 1

        codigodot += '}'

        # Guardar el archivo dot
        ruta_dot = 'reportesdot/listaSimple.dot'
        with open(ruta_dot, 'w') as archivo:
            archivo.write(codigodot)

        # Generar la imagen
        ruta_imagen = 'reportes/listaSimple.png'
        os.system(f'dot -Tpng {ruta_dot} -o {ruta_imagen}')
        os.startfile(os.path.abspath(ruta_imagen))
        print("Gráfico generado con éxito.")
