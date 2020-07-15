from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2
import ctypes
import glob
import numpy as np
import pyautogui
import threading
import os


#Clase principal de la grabadora


class Grabadora:

	def __init__(self, master):
		#|objeto para manejar ss|
		self.frame = master
		self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
		self.hora = 0
		self.minutos = 0
		self.segundos = 0
		self.grabando = False #Esta variable nos dira si estamos grabando o no
		self.PintarInterfaz()
	
	def LimpiarContadores(self):
		#Funcion que limpia todos los contadores |hora,minuto,segundos| al comenzar
		self.hora = 0
		self.minutos = 0
		self.segundos = 0


	def FormatoHora(self, c):
		#Esta funcion nos da formato al medidor de tiempo
		if c < 10:
			c = "0"+ str(c)
		return c	
	
	def ObtenerPantalla(self):
		#creamos una instancia del modulo ctypes 
		pantalla = ctypes.windll.user32
		pantalla.SetProcessDPIAware()
		#Obtenemos las medidas de x(0) - y(1) por medio de nuestra instancia 
		tamanio = pantalla.GetSystemMetrics(0), pantalla.GetSystemMetrics(1)
		return tamanio

	def Archivo(self, tex, ext):
		count = 0
		#Este metodo verifica si existe un archivo con el mismo nombre
		#En el mismo directorio, si los hay, debemos colocar el mismo nombre
		#Pero colocarle el numero de archivo repetido que es: copia-copia2
		for x in glob.glob('*'+ext):
			if tex in x:
				count += 1
		if count > 0:
			#Si tenemos dos o mas concidencias de nombre agregamos el numero al nombre
			nombre = tex+" "+str(count)+ext
		else:
			nombre = tex+ext
		#Retornamos nombre
		return nombre


	def screen_shot(self):
		#Este metodo toma una fotografia y la guarda en el directorio
		#Para el nombre llamamos a nuestro metodo 'Archivo' y ver si es unico
		#O si tenemos mas archivos con el mismo nombre
		pyautogui.screenshot(self.Archivo('captura_pantalla', '.jpg'))


	def Tiempo(self):
		self.time['text'] = str(self.FormatoHora(self.hora)) + str(self.FormatoHora(self.minutos)) + str(self.FormatoHora(self.segundos)) 
		self.segundos += 1
		if self.segundos == 60:
			self.segundos = 0
			self.minutos += 1
		if self.minutos == 60:
			self.minutos = 0
			self.hora += 1
		#	-DESFACE-
		self.proceso = self.time.after(886, self.Tiempo)	



	def EstadoGrabacion(self):
		if self.grabando == True:
			self.grabando = False
			self.time.after_cancel(self.proceso)
			self.LimpiarContadores()
		else:
			self.grabando = True
			self.btn_grabar.configure(text="Pausa")
			t1 = threading.Thread(target= lambda:self.Grabar())
			t2 = threading.Thread(target=lambda:self.Tiempo())
			t1.start()
			t2.start()	


	def BuscarDirectorio(self):
		self.directorio = filedialog.askdirectory()
		if self.directorio != "":
			os.chdir(self.directorio)



	def Grabar(self):
		self.salida = cv2.VideoWriter(self.Archivo("Video", ".mp4"), self.fourcc, 20.0,(self.ObtenerPantalla()))
		while self.grabando == True:
			img = pyautogui.screenshot()
			frame_ = np.array(img)
			frame_ = cv2.cvtColor(frame_,cv2.COLOR_BGR2RGB)
			self.salida.write(frame_)
		self.btn_grabar.configure(text="Grabar")
		self.salida.release()	




	def PintarInterfaz(self):
		self.label = Label(self.frame, relief="flat", text="Grabadora de Pantalla",bg="gray", font=("","15"))
		self.label.pack(padx=10,pady=1)
		self.time = Label(self.frame, fg='black', width=22, text="00:00:00", bg="gray", font=("","14"))
		self.time.pack()
		self.btn_grabar = Button(self.frame,text="Grabar", relief="ridge", borderwidth=2, overrelief="flat",bg="white",fg="black",width=8,command= lambda:self.EstadoGrabacion())#gray66
		self.btn_grabar.place(x=20,y=60, width=175)
		self.shoot = Button(self.frame,text="Capura de Pantalla", relief="ridge", borderwidth=2, overrelief="flat",bg="white",fg="black",width=8,command= lambda:self.screen_shot())
		self.shoot.place(x=20,y=90, width=175)
		self.folder = Button(self.frame, text="Seleccionar Archivo", relief="ridge", borderwidth=2, overrelief="flat",bg="white",width=10,command= lambda:self.BuscarDirectorio())
		self.folder.place(x=20,y=120, width=175)


root = Tk()
root.geometry("220x170")
root.config(bg="gray")
root.title("Olsgrab")
aplication = Grabadora(root)
root.mainloop()