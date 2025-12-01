# Importar librerias
import numpy as np
import matplotlib.pyplot as plt
import sys  # para salir si error

# Definir constantes
g = 9.8  # aceleracion de gravedad en m/s^2

# Solicitar datos al usuario
h_str = input("Ingrese la altura inicial h en metros: ")
h = float(h_str)

# Validar h
if h <= 0:
    print("Error: la altura h debe ser mayor que 0.")
    sys.exit(1)  # salir del programa

masa_str = input("Ingrese la masa m en kg (default 1.0 si vacio): ")
m = float(masa_str) if masa_str else 1.0

# Validar m
if m <= 0:
    print("Error: la masa m debe ser mayor que 0.")
    sys.exit(1)  # salir del programa

# Funcion para calcular posicion y(t), evita negativos por precision
def posicion(t, h):
    y = h - 0.5 * g * t**2
    return np.maximum(0, y)  # usa max para array o scalar

# Funcion para calcular velocidad v(t)
def velocidad(t):
    return -g * t

# Funcion para calcular energia cinetica Ec(t)
def energia_cinetica(t, m):
    v = velocidad(t)
    return 0.5 * m * v**2

# Funcion para calcular energia potencial Ep(t)
def energia_potencial(t, h, m):
    y = posicion(t, h)
    return m * g * y

# Funcion para calcular energia mecanica Em(t)
def energia_mecanica(t, h, m):
    ec = energia_cinetica(t, m)
    ep = energia_potencial(t, h, m)
    return ec + ep

# Calcular tiempo maximo para impacto (cuando y=0)
t_max = np.sqrt(2 * h / g)

# Crear arreglo de tiempos desde 0 a t_max con paso adecuado
t = np.linspace(0, t_max, 500)  # mas puntos para mejor resolucion

# Calcular energias de forma vectorizada
ec = energia_cinetica(t, m)
ep = energia_potencial(t, h, m)
em = energia_mecanica(t, h, m)

# Mostrar conservacion numericamente
print(f"Energia mecanica inicial: {em[0]:.2f} J")
print(f"Energia mecanica final: {em[-1]:.2f} J")
print("Si son aproximadamente iguales, la energia se conserva.")

# Graficar en una figura
plt.figure()
plt.plot(t, ec, label='Energia Cinetica')
plt.plot(t, ep, label='Energia Potencial')
plt.plot(t, em, label='Energia Mecanica')
plt.xlabel('Tiempo (s)')
plt.ylabel('Energia (J)')
plt.title('Energias vs Tiempo')
plt.legend()
plt.grid(True)
plt.show()
