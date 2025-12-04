# -*- coding: utf-8 -*-
"""
Programa: Conservacion de Energia en Caida Libre
Descripcion: Modela la caida libre de un cuerpo y visualiza la evolucion de
             las energias cinetica, potencial y mecanica, demostrando el
             principio de conservacion de la energia.
Ecuaciones principales:
    y(t) = h - (1/2)gt^2
    v(t) = -gt
    Ec(t) = (1/2)mv(t)^2
    Ep(t) = mgy(t)
    Em(t) = Ec(t) + Ep(t)
Autor: [Nombre del grupo]
Fecha: [Fecha]
"""

# Importar librerias
import numpy as np
import matplotlib.pyplot as plt
import sys  # para salir si error

# Definir constantes fisicas
g = 9.8  # aceleracion de gravedad en m/s^2

# Funcion para validar entrada numerica
def validar_entrada_numerica(mensaje, valor_por_defecto=None):
    """
    Solicita y valida una entrada numerica del usuario.
    Args:
        mensaje: Mensaje a mostrar al usuario
        valor_por_defecto: Valor a usar si la entrada esta vacia
    Returns:
        Valor numerico validado
    """
    while True:
        entrada = input(mensaje)
        
        # Si hay valor por defecto y la entrada esta vacia, usar el valor por defecto
        if valor_por_defecto is not None and entrada == "":
            return valor_por_defecto
        
        try:
            valor = float(entrada)
            if valor > 0:
                return valor
            else:
                print("Error: El valor debe ser mayor que 0.")
        except ValueError:
            print("Error: Debe ingresar un numero valido.")

# Solicitar datos al usuario con validacion mejorada
print("=" * 50)
print("CONSERVACION DE ENERGIA EN CAIDA LIBRE")
print("=" * 50)

h = validar_entrada_numerica("Ingrese la altura inicial h en metros: ")

m = validar_entrada_numerica("Ingrese la masa m en kg (ENTER para usar 1.0 kg): ", 1.0)

# Mostrar parametros seleccionados
print(f"\nParametros del modelo:")
print(f"  Altura inicial: {h} m")
print(f"  Masa del cuerpo: {m} kg")
print(f"  Aceleracion gravitacional: {g} m/s^2")

# Funcion para calcular posicion y(t)
def posicion(t, h):
    """
    Calcula la posicion vertical del cuerpo en funcion del tiempo.
    La posicion se limita a valores no negativos para evitar errores numericos.
    """
    y = h - 0.5 * g * t**2
    return np.maximum(0, y)  # Evita valores negativos por precision numerica

# Funcion para calcular velocidad v(t)
def velocidad(t):
    """Calcula la velocidad del cuerpo en funcion del tiempo."""
    return -g * t

# Funcion para calcular energia cinetica Ec(t)
def energia_cinetica(t, m):
    """Calcula la energia cinetica en funcion del tiempo."""
    v = velocidad(t)
    return 0.5 * m * v**2

# Funcion para calcular energia potencial Ep(t)
def energia_potencial(t, h, m):
    """Calcula la energia potencial en funcion del tiempo."""
    y = posicion(t, h)
    return m * g * y

# Funcion para calcular energia mecanica Em(t)
def energia_mecanica(t, h, m):
    """Calcula la energia mecanica total en funcion del tiempo."""
    ec = energia_cinetica(t, m)
    ep = energia_potencial(t, h, m)
    return ec + ep

# Calcular tiempo maximo hasta el impacto (cuando y=0)
# Usamos la ecuacion cuadratica: 0 = h - (1/2)gt^2
t_max = np.sqrt(2 * h / g)
print(f"  Tiempo hasta el impacto: {t_max:.3f} s")

# Crear arreglo de tiempos desde 0 a t_max
# Usamos 500 puntos para una buena resolucion grafica
num_puntos = 500
t = np.linspace(0, t_max, num_puntos)

# Calcular energias usando operaciones vectorizadas (eficiente)
ec = energia_cinetica(t, m)
ep = energia_potencial(t, h, m)
em = energia_mecanica(t, h, m)

# Analisis de la conservacion de energia
print("\n" + "=" * 50)
print("ANALISIS DE CONSERVACION DE ENERGIA")
print("=" * 50)

em_inicial = em[0]
em_final = em[-1]
diferencia_relativa = abs(em_final - em_inicial) / em_inicial * 100

print(f"Energia mecanica inicial (t=0): {em_inicial:.6f} J")
print(f"Energia mecanica final (t={t_max:.3f}s): {em_final:.6f} J")
print(f"Diferencia relativa: {diferencia_relativa:.6f} %")

if diferencia_relativa < 0.1:  # Umbral del 0.1%
    print("CONCLUSION: La energia mecanica se conserva (dentro de la precision numerica).")
else:
    print("CONCLUSION: Se detecto una pequena variacion en la energia mecanica.")

# Generar grafico
print("\nGenerando grafico...")

plt.figure(figsize=(10, 6))

# Graficar las tres energias
plt.plot(t, ec, 'b-', linewidth=2, label='Energia Cinetica Ec(t)')
plt.plot(t, ep, 'r-', linewidth=2, label='Energia Potencial Ep(t)')
plt.plot(t, em, 'g--', linewidth=2.5, label='Energia Mecanica Em(t)')

# Agregar linea horizontal para enfatizar la conservacion
plt.axhline(y=em_inicial, color='k', linestyle=':', linewidth=1, 
            alpha=0.5, label=f'Em inicial = {em_inicial:.2f} J')

# Configuracion del grafico
plt.xlabel('Tiempo (s)', fontsize=12)
plt.ylabel('Energia (J)', fontsize=12)
plt.title('Evolucion de las Energias en Caida Libre', fontsize=14, fontweight='bold')

# Mostrar tiempo de impacto en el grafico
plt.axvline(x=t_max, color='gray', linestyle=':', linewidth=1, alpha=0.5)
plt.text(t_max, em_inicial/2, f'Impacto: {t_max:.2f} s', 
         rotation=90, verticalalignment='center', fontsize=10)

plt.legend(loc='best', fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Guardar el grafico como archivo PNG
nombre_archivo = f"energia_h{h:.1f}m_m{m:.1f}kg.png"
plt.savefig(nombre_archivo, dpi=150)
print(f"Grafico guardado como: {nombre_archivo}")

# Mostrar el grafico en pantalla
plt.show()

# Informacion adicional para el usuario
print("\n" + "=" * 50)
print("INFORMACION ADICIONAL")
print("=" * 50)
print(f"1. Energia inicial total: {em_inicial:.2f} J")
print(f"2. Esta energia se transforma de potencial a cinetica durante la caida.")
print(f"3. La energia mecanica total debe permanecer constante (principio de conservacion).")
print(f"4. El grafico muestra:")
print(f"   - Linea azul: Energia cinetica (aumenta con el tiempo)")
print(f"   - Linea roja: Energia potencial (disminuye con el tiempo)")
print(f"   - Linea verde punteada: Energia mecanica total (debe ser constante)")
print(f"   - Linea punteada negra: Valor inicial de la energia mecanica")

print("\nPrograma ejecutado exitosamente.")
