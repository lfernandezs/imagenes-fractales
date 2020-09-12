# Imágenes Fractales
Se modelan imágenes fractales utilizando el sistema de Lindenmayer

## Sistemas-L
Los sistemas de Lindenmayer o sistemas-L, son definidos por un conjunto G = {V, S, ω, P).
* V: Conjunto de variables.
* S: Conjunto de constantes.
* ω: Cadena de símbolos de V que definen el estado inicial del sistema.
* P: Conjunto de reglas que definen la forma en la que las variables pueden ser reemplazadas por combinaciones de constantes y variables.

## Modo de Uso
### Reglas

Los posibles movimientos son:
* F ó G: hacia adelante (pluma abajo).
* f ó g: hacia adelante (pluma arriba).
* +: rotación horario.
* -: rotación antihorario.
* |: rotación antihorario 90 grados.
* [: Se apila una nueva pluma.
* ]: Se desapila la pluma del tope.


Dentro de un archivo <reglas>.sl se definen las reglas del sistema. Por ejemplo, en arbol.sl:
```
36 # Ángulo de rotación
F  # Estado inicial del sistema
F F[+F]F  # Cómo se reemplazan las variables
```
### Ejecución
```
python3 imagenes_fractales.py <path_reglas>.sl <número_de_iteraciones> <path_imagen>.svg 
```
Ejemplo
```
python3 imagenes_fractales.py reglas/copo_de_nieve.sl 3 copo_de_nieve.svg
```
  
<img src="https://github.com/lfernandezs/Imagenes-Fractales/blob/master/fractales/copo_de_nieve.svg" alt="Copo de nieve" width="200"/>
