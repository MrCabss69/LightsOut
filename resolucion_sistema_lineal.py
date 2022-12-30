#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, random
import numpy as np
from pygame.locals import *
import scipy as sc
#N = random.randint(3, 10) +1
N = 5
lado_cuadrado = 100
R = [pygame.Rect( i * lado_cuadrado, 0, lado_cuadrado, lado_cuadrado) for i in range(N)] #inicialización y creación de N cuadrados con pygame.Rect
P = [1,1,1,1,1]
# P,P1,P2 = [random.randint(0, 1) for i in range(N)], [1,0,1,0,1], [1,0,0,0,0] #seteo aleatorio de los estados iniciales
VRD_CLR, VRD_OSC, BL = (0, 255, 153), (23, 63, 53), (250, 250, 250)
color = [VRD_OSC, VRD_CLR]

def matriz_ampliada(A,b):
    # Dada la matriz de coeficientes de un sistema A y un vector fila b, se calcula la matriz ampliada del sistema
    Amp=[]
    for i in range(len(A)):
        filaI=[]
        for j in range(len(A[0])):
            filaI.append(A[i][j])
        filaI.append(b[i])
        Amp.append(filaI)
    return Amp

def inverso(x,p):
    inv , encontrado = 1 , False
    while inv < p and (not encontrado):
        if sc.mod( inv*x, p) == 1:
            encontrado = True
        else:
            inv = inv + 1
    return inv

def matrizCanFil(A,b,p):
    #Dada la matriz de coeficientes de un sistema A y un vector fila b, se obtiene la forma canonica por filas de la matriz ampliada,modulo p.
    nfilas, ncolumnas = len(A), len(A[0])
    Amp = matriz_ampliada(A,b)
    fil, col, par, lig = 0, 0, [], []
    while col < ncolumnas and fil < nfilas:
        for i in range(  fil + 1, nfilas):
            cond_1 = (sc.mod(Amp[fil][col],p)!=1 and sc.mod(Amp[i][col],p)==1)
            cond_2 = (sc.mod(Amp[fil][col],p)==0 and sc.mod(Amp[i][col],p)!=0)
            if cond_1 or cond_2:
                Amp[fil], Amp[i] = Amp[i], Amp[fil]
        if Amp[fil][col] != 0:
            pivote = Amp[fil][col]
            if pivote != 1:
                inv = inverso(pivote,p)
                for s in range(col,ncolumnas+1):
                    Amp[fil][s] = sc.mod(inv*Amp[fil][s],p)
            for r in range(nfilas):
                if r != fil and Amp[r][col] != 0:
                    aux = Amp[r][col]
                    for s in range(col,ncolumnas+1):
                        Amp[r][s] = sc.mod(Amp[r][s]-aux*Amp[fil][s],p)
            lig.append([fil,col])
            fil += 1
            col += 1
        else:
            par.append(col)
            col += 1
    while col < ncolumnas:
        par.append(col)
        col += 1
    return sc.remainder(Amp,p),par,lig

def resol_sist_mod_p(A,b,p):
    #Resuelve el sistema Ax=b mdulo p. Da una solucion particular y subespacio asociado para el resto de las soluciones
    matCF,par,lig = matrizCanFil(A,b,p)
    control = True
    for i in range(len(A))[len(lig):len(A)]:
        if matCF[i][-1] != 0:
            control = False
    if control:
        solu1 = [0]*len(A[0])
        for j in range(len(lig)):
            fil = lig[j][0]
            col = lig[j][1]
            solu1[col] = matCF[fil][-1]
        if len(par) == 0:
            return solu1
        else:
            solu2 = []
            for i in range(len(par)):
                solu2.append([0]*len(A[0]))
            for k in range(len(par)):
                VarP = par[k]
                solu2[k][VarP] = 1
                for j in range(len(lig)):
                    fil = lig[j][0]
                    col = lig[j][1]
                    solu2[k][col] = sc.mod(-matCF[fil][par[k]],p)
                return solu1,solu2
    else:
        return []

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

def existeSolucion():
    A = matrizInterruptores();print("");print(A);print("")
    S = resol_sist_mod_p(A,P,2)
    res = S == []
    if not res:
        print("Hay solución")
        print(S[0])
    else:
        print("No hay solución para el sistema dado")

if __name__ == '__main__':
    pygame.init()
    existeSolucion()
    main()
