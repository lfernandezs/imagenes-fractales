import sys
from math import pi, sin, cos

class _Punto:
    """Representación de un punto en el plano en coordenadas cartesianas (x, y)."""
    def __init__(self, x, y):
        """Constructor de Punto. Recibe x e y, deben ser numéricos."""
        self.x = x
        self.y = y

    def __add__(self, otro):
        """Devuelve el punto que resulta de la suma de otro punto recibido."""
        return _Punto(self.x+otro.x, self.y+otro.y)

    def __sub__(self, otro):
        """Devuelve el punto que resulta de la resta de otro punto recibido."""
        return _Punto(self.x-otro.x, self.y-otro.y)

class Tortuga:
    """Representación de una tortuga que puede avanzar y girar en coordenadas cartesianas."""
    def __init__(self, pos = _Punto(0, 0), orientacion = 0):
        """Contructor de la tortuga. Puede recibir la posición inicial y su orientación."""
        self.pos = pos
        self.orientacion = orientacion
        self.pluma = _Pluma()

    def adelante(self, n):
        """Recibe un número n y avanza la tortuga esa cantidad. Devuelve la nueva posición."""
        self.pos = _Punto(self.pos.x + n * sin(self.orientacion), self.pos.y + n * cos(self.orientacion))
        return self.pos

    def derecha(self, angulo):
        """Gira la tortuga a la derecha en el ángulo recibido."""
        self.orientacion += angulo

    def izquierda(self, angulo):
        """Gira la tortuga a la izquierda en el ángulo recibido."""
        self.orientacion -= angulo

class Pila:
    """Representa una pila con operaciones de apilar, desapilar, ver tope y longitud."""
    def __init__(self):
        """Crea una pila vacía."""
        self.items = []
        self.len = 0

    def apilar(self, dato):
        """Apila un elemento dado."""
        self.items.append(dato)
        self.len += 1

    def desapilar(self):
        """Devuelve el elemento que está el el tope y lo elimina de la pila."""
        self.len -= 1
        return self.items.pop()

    def __len__(self):
        """Devuelve la cantidad de elementos de la pila."""
        return self.len

    def ver_tope(self):
        """Devuelve el elemento que se encuentra en el tope de la pila. Si la pila está vacía, devuelve None."""
        if self.items:
            return self.items[-1]
        return None

class _Pluma:
    """Representa una pluma con operaciones de escribir, no escribir, cambiar ancho y color."""
    def __init__(self, color="black", ancho=1, escribe=True):
        """Crea una pluma, puede recibir el color, ancho y un booleano si esta escribe o no."""
        self.color = color
        self.ancho = ancho
        self.escribe = escribe

    def arriba(self):
        """La pluma deja de escribir."""
        self.escribe = False

    def abajo(self):
        """La pluma comienza a escribir."""
        self.escribe = True

    def color(self, color):
        """Recibe un color para cambiar el color de la pluma."""
        self.color = color

    def ancho(self, ancho):
        """Recibe un ancho para cambiar el ancho de la pluma."""
        self.ancho = ancho

def grads_a_rads(x):
    """Recibe un angulo en grados y devuelve su conversión en radianes. Out of place."""
    return (x * 2 * pi) / 360

def verificar_comandos():
    """Verifica si los comandos ingresados son válidos. Si lo son, devuelve
    el nombre del archivo de las instrucciones, la cantidad de iteraciones y
    el nombre del archivo en donde se encontrará la imagen. Sino, devuelve un
    mensaje de error y finaliza el programa"""
    mens_error = "Los comandos ingresados son inválidos."
    if len(sys.argv) != 4:
        sys.exit(mens_error)
    param_1, param_2, param_3 = sys.argv[1:]
    if param_1[-3:] == ".sl":
        path_arbol = param_1
    else:
        sys.exit(mens_error)
    if param_2.isdigit():
        iterac = int(param_2)
    else:
        sys.exit(mens_error)
    if param_3[-4:] == ".svg":
        path_img = param_3
    else:
        sys.exit(mens_error)
    return path_arbol, iterac, path_img

def leer_arbol(path):
    """Recibe el nombre del archivo y devuelve una lista con el ángulo, el axioma
    y las reglas. Si no encuentra el archivo, devuelve un mensaje de error y 
    finaliza el programa."""
    try:
        with open(path) as arbol:
            angulo_g = float(arbol.readline().rstrip("\n"))
            angulo = grads_a_rads(angulo_g)
            axioma = arbol.readline().rstrip("\n")
            reglas = {}
            for linea in arbol:
                pre, suc = linea.split()
                reglas[pre] = suc
    except FileNotFoundError:
        sys.exit(f"El archivo '{path}' no fue encontrado.")
    return [angulo, axioma, reglas]

def generar_instr(arbol, iterac):
    """Recibe una lista con el ángulo, el axioma y las reglas del dibujo,
    y la cantidad de iteraciones. Devuelve una cadena con los pasos a seguir.""" 
    axioma = arbol[1]
    reglas = arbol[2]
    instr = axioma
    for i in range(iterac):
        cadena_aux = ""
        for c in instr:
            if c in reglas:
                cadena_aux += reglas[c]
            else:
                cadena_aux += c
        instr = cadena_aux
    return instr

def comparar_coord(extremos, nueva_pos):
    """Recibe los extremos del dibujo en una lista de coordenadas y la nueva posición de la tortuga.
    Devuelve una lista con los nuevos extremos del dibujo."""
    min_x, min_y, max_x, max_y = extremos
    if nueva_pos.x > max_x:
        max_x = nueva_pos.x
    if nueva_pos.x < min_x:
        min_x = nueva_pos.x
    if nueva_pos.y > max_y:
        max_y = nueva_pos.y
    if nueva_pos.y < min_y:
        min_y = nueva_pos.y
    return [min_x, min_y, max_x, max_y]

def procesar_letra(lineas, tortuga, extremos):
    """Recibe la lista de lineas, la tortuga del tope y los extremos.
    Avanza la tortuga y devuelve los nuevos extremos."""
    ant_pos = tortuga.pos
    nueva_pos = tortuga.adelante(10)
    extremos = comparar_coord(extremos, nueva_pos)
    if tortuga.pluma.escribe:
        lineas.append(f'   <line x1="{ant_pos.x}" y1="{-ant_pos.y}"\
 x2="{nueva_pos.x}" y2="{-nueva_pos.y}"\
 stroke-width="{tortuga.pluma.ancho}" stroke="{tortuga.pluma.color}" />\n')
    return extremos
        
def generar_lineas(angulo, instr):
    """Recibe el ángulo y las instrucciones. Devuelve las lineas del dibujo y sus extremos."""
    lineas = []
    pila = Pila()
    pila.apilar(Tortuga())
    extremos = [0, 0, 0, 0]
    for c in instr:
        tortuga = pila.ver_tope()
        if c in ['F', 'G']:
            extremos = procesar_letra(lineas, tortuga, extremos)
        elif c in ['f', 'g']:
            tortuga.pluma.arriba()
            extremos = procesar_letra(lineas, tortuga, extremos)
            tortuga.pluma.abajo()
        elif c == '|':
            tortuga.derecha(pi)
        elif c == '+':
            tortuga.derecha(angulo)
        elif c == '-':
            tortuga.izquierda(angulo)
        elif c == '[':
            pila.apilar(Tortuga(tortuga.pos, tortuga.orientacion))
        elif c == ']':
            pila.desapilar()
    return lineas, extremos

def generar_img(extremos, lineas, path_img):
    """Recibe los extremos, las líneas del dibujo y el nombre del archivo de la imagen.
    Escribe en ese archivo las lineas y los respectivos extremos de la imagen."""
    box_x = extremos[0]
    box_y = -extremos[3]
    ancho = (extremos[2] - extremos[0]) * 1.1
    alto = (extremos[3] - extremos[1]) * 1.1
    with open(path_img, 'w') as archivo:
        archivo.write(f'<svg viewBox="{box_x} {box_y} {ancho} {alto}" xmlns="http://www.w3.org/2000/svg">\n')
    with open(path_img, 'a') as archivo:
        for linea in lineas:
            archivo.write(linea)
        archivo.write('</svg>')

def main():
    """Inicializa el programa que genera la imagen."""
    path_arbol, iterac, path_img = verificar_comandos()
    arbol = leer_arbol(path_arbol)
    angulo = arbol[0]
    instr = generar_instr(arbol, iterac)
    lineas, extremos = generar_lineas(angulo, instr)
    generar_img(extremos, lineas, path_img)

main()