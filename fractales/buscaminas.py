from random import randrange

# La cantidad de minas debe ser menor o igual a la cantidad de espacios disponibles.
CANT_MINAS = 10
COLUMNAS = 8
FILAS = 8


def main():
	"""Función principal del juego"""
	minas = crear_minas()
	tablero_main = crear_tablero_main(minas) # El usuario no lo podrá ver
	tablero = crear_tablero() # El tablero que podrá ver el usuario
	jugada = 0
	reglas_del_juego()
	while seguir_jugando(jugada, tablero, minas, tablero_main):
		mostrar_tablero(tablero)
		jugada = pedir_jugada(tablero)
		procesar_jugada(tablero, tablero_main, jugada, minas)
	mostrar_tablero(tablero)

def crear_minas():
	"""Devuelve una tupla con las coordenadas de las minas"""
	minas = [] # Acá guardo las coordenadas de las minas.
	while len(minas) != CANT_MINAS:
		mina = (randrange(FILAS), randrange(COLUMNAS))
		if mina in minas: # Para verificar que no haya más de una mina en una misma coordenada.
			continue
		minas.append(mina)
	minas = tuple(minas) # Para que sean inmutables.
	return minas

def crear_tablero_main(minas):
	"""Devuelve el tablero_main al descubierto como tupla de tuplas con los respectivos números y minas"""
	tablero_main = []
	for i in range(FILAS):
		fila = []
		for j in range(COLUMNAS):
			numero = 0 # Cantidad de minas en el perímetro.
			if (i, j) in minas:
				fila.append("x")
				continue
			if (i + 1, j) in minas:
				numero += 1
			if (i, j + 1) in minas:
				numero += 1
			if (i + 1, j + 1) in minas:
				numero += 1
			if (i - 1, j) in minas:
				numero += 1
			if (i, j - 1) in minas:
				numero += 1
			if (i - 1, j - 1) in minas:
				numero += 1
			if (i + 1, j - 1) in minas:
				numero += 1
			if (i - 1, j + 1) in minas:
				numero += 1
			fila.append(numero)
		fila = tuple(fila) # Para que la fila sea inmutable.
		tablero_main.append(fila)
	tablero_main = tuple(tablero_main) # Para que el tablero sea inmutable.
	return tablero_main

def crear_tablero(): # Este tablero sí es mutable.
	"""Devuelve el tablero cubierto como una lista de listas"""
	tablero = []
	for i in range(FILAS):
		fila = []
		for j in range(COLUMNAS):
			fila.append("•")
		tablero.append(fila)
	return tablero

def seguir_jugando(jugada, tablero, minas, tablero_main):
	"""Devuelve False si el jugador ganó o perdió, sino True"""
	if jugada in minas:
		print("¡BOOOOOOOM! Perdiste.")
		return False
	for i in range(len(tablero)): # Verifica si se descubrieron todos las casillas excepto las minas
		for j in range(len(tablero)):
			if (i, j) in minas:
				continue
			if tablero[i][j] != str(tablero_main[i][j]):
				return True
	print("¡Ganaste!")
	return False
	

def reglas_del_juego():
	"""Imprime las reglas del juego"""
	print("¡Bienvenido al Buscaminas!")

	a = input(">>>ENTER")
	
	print("""INSTRUCCIONES:
	
	•Si se quiere descubrir una casilla, se ingresa primero el número de la fila

	y luego el numero de la columna separados por un punto. Ej: 8.4

	•Si se quiere colocar una bandera, se ingresa el número de la casilla en donde

	se quiera colocar, anteponiendo un asterisco (*). Ej: *8.4

	""")
	a = input(">>>ENTER")

def mostrar_tablero(tablero):
	"""Imprime el tablero que el jugador debe ver"""
	print("  ", end = " ")
	for n in range(COLUMNAS - 1):
		print(str(n)[-1], end = " ") # Le pido que imprima sólo el último dígito porque sino el tablero se deforma cuando supera 10x10.
	print(str(COLUMNAS - 1)[-1]) # Imprimo la última por separado sin en el end.
	for i in range(len(tablero)):
		print(str(i)[-1] + ".", " ".join(tablero[i]))

def pedir_jugada(tablero):
	"""Le pide una jugada al jugador y si es válida, la devuelve"""
	while True:
		jugada = input("Ingrese su jugada: ")
		if validar_escritura(jugada):
			if jugada[0] == "*":
				jugada = ("*", int(jugada[1:jugada.index(".")]), int(jugada[jugada.index(".") + 1:]))
			else:
				jugada = (int(jugada[0:jugada.index(".")]), int(jugada[jugada.index(".") + 1:]))
			if validar_jugada(jugada, tablero):
				return jugada
			

def validar_escritura(jugada):
	""" Devuelve True si la jugada está escrita correctamente, sino, False"""
	if len(jugada) == 0:
		print("""Ingrese una fila y columna separadas por un punto. Ej: 8.4
Si quiere colocar una bandera, anteponga un *. Ej *8.4""")
		return False
	if not ("." in jugada):
		print("Recuerde separar filas y columnas con un punto. Ej: 8.4")
		return False
	if jugada[0] == "*":	
		fila = jugada[1:jugada.index(".")]
	else:
		fila = jugada[0:jugada.index(".")]
	columna = jugada[jugada.index(".") + 1:]
	if not(fila.isdigit() and columna.isdigit()):
		print("""Ingrese únicamente números para indicar fila y columna. Ej: 8.4
Para colocar una bandera, anteponga * .""")
		return False
	if not(int(fila) < FILAS and int(columna) < COLUMNAS):
		print("Ingrese un número acorde al número de columnas y filas existentes.")
		return False
	return True


def validar_jugada(jugada, tablero):
	"""Devuelve True si es posible realizar la jugada, sino False"""
	if jugada[0] == "*" :
		if tablero[jugada[1]][jugada[2]].isdigit():
			print("No se puede colocar una bandera en un espacio ya descubierto")
			return False
	else:
		if tablero[jugada[0]][jugada[1]] == "*":
			print(f"Debe quitar la bandera antes. Ingrese *{jugada[0]}.{jugada[1]}")
			return False
		if tablero[jugada[0]][jugada[1]].isdigit():
			print("Usted ya descubrió esta sección, ingrese una coordenada diferente")
			return False
	return True


def procesar_jugada(tablero, tablero_main, jugada, minas):
	"""Cambia el tablero que ve el usuario de acuerdo a la jugada realizada"""
	if jugada[0] == "*":
		if tablero[jugada[1]][jugada[2]] == "*":
			tablero[jugada[1]][jugada[2]] = "•"
		elif tablero[jugada[1]][jugada[2]] == "•":
			tablero[jugada[1]][jugada[2]] = "*"
	else:
		tablero[jugada[0]][jugada[1]] = str(tablero_main[jugada[0]][jugada[1]]) # Convierto a String para luego poder imprimirlos con .join

main()
