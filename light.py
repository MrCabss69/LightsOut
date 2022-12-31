#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, random
import numpy as np
from pygame.locals import *
N = 9
lado_cuadrado= 100
R = [pygame.Rect( i * lado_cuadrado, 0, lado_cuadrado, lado_cuadrado) for i in range(N)] # inicialización y creación de N cuadrados con pygame.Rect
P = [random.randint(0, 1) for i in range(N)] #seteo aleatorio de los estados iniciales
VRD_CLR, VRD_OSC, BL = (0, 255, 153), (23, 63, 53), (250, 250, 250)
color = [VRD_OSC, VRD_CLR]

def marco(ventana):
    for i in range(N):
        pygame.draw.rect(ventana, color[P[i]], R[i])
    for i in range(1, N +1):
        pygame.draw.line(ventana, BL, [i*lado_cuadrado, 0], [i*lado_cuadrado, N*lado_cuadrado], 1)
    pygame.draw.polygon(ventana, BL, [[0,0],[0,lado_cuadrado],[N*lado_cuadrado,lado_cuadrado],[N*lado_cuadrado,0]], 15)
    
def movimiento(ventana):
    raton = pygame.mouse.get_pos()
    for i in range(N):
        if R[i].collidepoint(raton):
            P[i] = 1 - P[i]
            if i - 1 >= 0 : P[i-1] = 1 - P[i-1]
            if i + 1 < N : P[i+1] = 1 - P[i+1]
def main():
    ventana , final = pygame.display.set_mode((N*lado_cuadrado, lado_cuadrado)) , sum(P) == 0
    pygame.display.set_caption("Intenta Resolverlo")
    marco(ventana)
    pygame.display.update()
    while not final:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                final = True
            elif event.type == MOUSEBUTTONDOWN:
                movimiento(ventana)
                marco(ventana)
                valorJuego = sum(P)
                if valorJuego == 0:
                    pygame.display.set_caption("CONSEGUIDO")
        pygame.display.update()
    pygame.quit()

def matrizInterruptores():
    res, columna_00 , columna_01 = [], np.array([1,1]) , np.repeat(0, N-2)
    columna_0 = np.concatenate( [columna_00 , columna_01])
    res.append(columna_0)
    for s in range(1 , len(P) - 1 ):
        columna = np.zeros(len(P))
        columna[s-1] = 1
        columna[s] = 1
        columna[s+1] = 1
        res.append(columna)
    columna_f0 , columna_f1 = np.repeat(0, N-2) , np.array([1,1])
    columna_final = np.concatenate( [columna_f0 , columna_f1])
    res.append(columna_final)
    return np.array(res)

def calculaSolucion():
    C , S , A = P , np.zeros(len(P)) , matrizInterruptores()
    if(sum(P)==0):
        print("El estado inicial está solucionado")
    if( np.linalg.det(A) != 0):
        A1 = np.linalg.inv(A)
        print("Matriz de interruptores invertida:")
        print(A1)
        S = np.dot(A1, C)
        print("Secuencia solución:")
        f = lambda x: abs( x % 2 )
        S = f(S)
        print(S)
    else:
        print("No hay una solución válida")

if __name__ == '__main__':
    pygame.init()
    calculaSolucion()
    main()
