import ctypes
import math
import random
import pygame
import sys
from tkinter import *
import time
import threading
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QDialog
from PySide2.QtCore import QFile

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
SW_HIDE = 0
hWnd = kernel32.GetConsoleWindow()
user32.ShowWindow(hWnd, SW_HIDE)

root = Tk()
root.geometry("250x200")
root.title("Simulacion")
canvas = Canvas(root, width=250, height=200)
Label(root,text=" ").pack()
l0 = StringVar()
l1 = StringVar()
l2 = StringVar()

Label(root,textvariable=l0).pack()
Label(root,textvariable=l1).pack()
Label(root,textvariable=l2).pack()

canvas.pack()

cajon = []
global i
i = 0
global sumPerdida, sumPromedioDisponible
global porcentajeClientesPerdidos, probabilidadDisponible, promedioDisponible
sumPerdida = 0
sumPromedioDisponible = 0.0
porcentajeClientesPerdidos = 0.0
probabilidadDisponible = 0.0
promedioDisponible = 0.0

cajon.append(canvas.create_rectangle(77, 40, 87,  65, fill='green'))
cajon.append(canvas.create_rectangle(97, 40, 107, 65, fill='green'))
cajon.append(canvas.create_rectangle(117, 40, 127, 65, fill='green'))
cajon.append(canvas.create_rectangle(137, 40, 147, 65, fill='green'))
cajon.append(canvas.create_rectangle(157, 40, 167, 65, fill='green'))
cajon.append(canvas.create_rectangle(177, 40, 187, 65, fill='green'))

canvas.create_rectangle(70, 30, 73,  70, fill='black')
canvas.create_rectangle(90, 30, 93,  70, fill='black')
canvas.create_rectangle(110, 30, 113,  70, fill='black')
canvas.create_rectangle(130, 30, 133,  70, fill='black')
canvas.create_rectangle(150, 30, 153,  70, fill='black')
canvas.create_rectangle(170, 30, 173,  70, fill='black')
canvas.create_rectangle(190, 30, 193,  70, fill='black')
canvas.create_rectangle(70, 70, 193,  73, fill='black')

def renueva_carros():
	
	global i
	global sumPerdida, sumPromedioDisponible
	
	txtHora = "Horas: \t\t{0}".format(i+1)
	
	if(ncarros[i] > 6):
		txtSeFueron = "Se fueron: \t{0}".format(ncarros[i] - 6)
		sumPerdida = sumPerdida + (ncarros[i]-6)
	elif(ncarros[i] <= 6):
		txtSeFueron = "Se fueron: \t0".format()
		sumPromedioDisponible += (6-ncarros[i])/6

	txtTiempoEstadia = "Tiempo de estadía: \t{0} minutos".format(round(tpromedio[i]))
	
	l0.set(txtHora)
	l1.set(txtSeFueron)
	l2.set(txtTiempoEstadia)
	
	time.sleep(1)
	
	for x in range(0,6):
		canvas.itemconfigure(cajon[x], fill='white');
	
	time.sleep(1)
	
	for x in range(0,ncarros[i]):
		if(x >= 6):
			break
		canvas.itemconfigure(cajon[x], fill='red');
	
	i = i+1

	if(i != int(horas_activo)):
		renueva_carros()
	else:
		global porcentajeClientesPerdidos, probabilidadDisponible, promedioDisponible
	
		porcentajeClientesPerdidos = ((sumPerdida/dt)*100)
		probabilidadDisponible = (((dt-sumPerdida)/dt)*100)
		promedioDisponible = ((sumPromedioDisponible/N)*100)

		txtHora = "Clientes perdidos: {0}%".format(round(porcentajeClientesPerdidos,2))
		txtSeFueron = "Lugares disponibles: {0}%".format(round(probabilidadDisponible,2))
		txtTiempoEstadia = "Promedio de lugares disponibles: {0}%".format(round(promedioDisponible,2))

		l0.set(txtHora)
		l1.set(txtSeFueron)
		l2.set(txtTiempoEstadia)
	
class SimulacionDeEstacionamiento ():
	def __init__(self):
		super(SimulacionDeEstacionamiento, self).__init__()
		self.ui = QUiLoader().load(QFile("interfaz.ui"))
		self.ui.pushButton.clicked.connect(self.procesarDatos)

	def procesarDatos(self):
		global media_est
		global horas_activo
		global min_act
		global max_act

		media_est = self.ui.lineEdit.text()
		horas_activo = self.ui.lineEdit_2.text()
		min_act = self.ui.lineEdit_3.text()
		max_act = self.ui.lineEdit_4.text()
		myapp.ui.close()
		self.ejecutarPrograma()

	def ejecutarPrograma(self):
	    global a, ncarros, tpromedio, ab, b, dt, fact, m, distribucion, distribucionAcumulada, N, x, unidades, xTotal, xPromedio
	    ab = 1
	    b = 0
	    dt = 0
	    fact = 1
	    #print("Distribución de Poisson")
	    #raw_m = input("Ingrese el valor de la media estadística: ")
	    m = int(media_est)
	    distribucion = []
	    distribucionAcumulada = []
	    #print("\nX    Ditribución estadística f(xi) | Distribución estadística acumulada F(xi) |")
	    while b <= ab:
	        for i in range(0,100000):
	            if i == 0:
	                distribucion.append((math.exp(-m)*pow(m,i))/fact)
	                distribucionAcumulada.append(distribucion[i])
	                #print("\n", i, "   \tf(xi)=",distribucion[i],"              |\t\tF[xi]=",distribucionAcumulada[i],"\t\t      |")
	                if distribucionAcumulada[i] >= 0.99995:
	                    b = 2
	                    break

	            if i>=1:
	                distribucion.append((math.exp(-m) * pow(m, i)) / fact)
	                distribucionAcumulada.append(distribucion[i] + distribucionAcumulada[i - 1])
	                #print("\n",i,"   \tf(xi)=",distribucion[i],"              |\t\tF[xi]=",distribucionAcumulada[i],"\t\t      |")
	                fact = fact * (i + 1)
	                if distribucionAcumulada[i] >= 0.99995:
	                    b = 2
	                    break


	    b = 0;
	    #print("\n")
	    while b <= ab:
	        for i in range(0,100000):
	            #if i == 0:
	                #print("\nSi R es > 0 y <= ",distribucionAcumulada[i]," entonces X = ",i,"")
	            if i >= 1:
	               #print("\nSi R es > ",distribucionAcumulada[i - 1]," y <= ",distribucionAcumulada[i]," entonces ",i,"")
	            	if distribucionAcumulada[i] >= 0.99995:
	                    b = 2
	                    break


	    #raw_N=input("\n\nIngrese la cantidad de números aleatorios a generar para comprobar su rango\nN = ")
	    N=int(horas_activo)
	    #print("\n")

	    a = []
	    ncarros = []
	    for i in range(0,N):
	        b=0
	        a.append(random.random())
	        while b <= ab:
	            for j in range(0, 100000):
	                if j == 0:
	                    if a[i] > 0 and a[i] <= distribucionAcumulada[j]:
	                        #print("[",(i+1),"] = ",a[i],"\tX = ",j,"\n")
	                        b = 2
	                        dt = dt + j
	                        ncarros.append(j)
	                        break
	                if j > 0:
	                    if a[i] > distribucionAcumulada[j - 1] and a[i] <= distribucionAcumulada[j]:
	                        #print("[", (i + 1),"] = ",a[i],"\tX = ",j,"\n")
	                        b = 2
	                        dt = dt + j
	                        ncarros.append(j)
	                        break
	    #print("\n\n\t\t\tDemanda total: ",dt,"\n")
	    #print("\n\n\n")
	    #print("\t\tDistribución Uniforme")
	    #raw_min=input("\nIngrese el valor minimo\na = ")
	    #raw_max=input("\nIngrese el valor maximo\nb = ")
	    min=int(min_act)
	    max = int(max_act)
	    unidades="min"
	    xTotal = 0
	    x=[]
	    tpromedio = []
	    for i in range(0,N):
	        x.append(min + ((max - min) * a[i]))
	        #print("\nTE",i," = ",min," + (",max," - ",min,")(",a[i],") = ",x[i]," " +unidades)
	        xTotal += x[i];
	        tpromedio.append(x[i])

	    xPromedio = xTotal / N;
	    #print("\n\n\t\tTiempo total: ",xTotal," " +unidades)
	    #print("\n\t\tTiempo promedio: ", xPromedio," "+ unidades)
	    self.simulacion()

	def simulacion(self):
		renueva_carros_thread = threading.Thread(target=renueva_carros)
		renueva_carros_thread.start()
		root.mainloop()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	myapp=SimulacionDeEstacionamiento()
	myapp.ui.show()
	sys.exit(app.exec_())

