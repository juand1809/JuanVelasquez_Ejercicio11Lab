
import numpy as np
import matplotlib.pylab as plt
import pandas as pd
import scipy.signal as signal


#Concatenación de los datos


data1 = pd.read_csv("transacciones2008.txt",sep = ";",names=['Fecha','Hora','Conversion','Monto'],decimal =",")
data2 = pd.read_csv("transacciones2009.txt",sep = ";",names=['Fecha','Hora','Conversion','Monto'],decimal =",")
data3 = pd.read_csv("transacciones2010.txt",sep = ";",names=['Fecha','Hora','Conversion','Monto'],decimal =",")


a = data1["Fecha"].str.split(" ",expand = True)
b = data1["Hora"].str.split(" ",expand = True)
c = data2["Fecha"].str.split(" ",expand = True)
d = data2["Hora"].str.split(" ",expand = True)
e = data3["Fecha"].str.split(" ",expand = True)
f = data3["Hora"].str.split(" ",expand = True)



n1 = pd.DataFrame({'Fecha': a[0] + " " + b[1],'Conversion':data1["Conversion"],'Monto':data1["Monto"]})
n2 = pd.DataFrame({'Fecha': c[0] + " " + d[1],'Conversion':data2["Conversion"],'Monto':data2["Monto"]})
n3 = pd.DataFrame({'Fecha': e[0] + " " + f[1],'Conversion':data3["Conversion"],'Monto':data3["Monto"]})



data = pd.concat([n1,n2,n3],ignore_index = True)
data["Fecha"] = pd.to_datetime(data["Fecha"],format='%d/%m/%Y %H:%M:%S')
data.to_csv('datos.csv',index = False)


#Plot de los datos para la señal


plt.figure(figsize=(15,10))
plt.plot(data["Fecha"],data["Conversion"])
plt.savefig("Señal.png")


#Filtros


N1  = 1    
Wn1 = 0.1 
B1, A1 = signal.butter(N1, Wn1)
precio_filtrado1 = signal.filtfilt(B1,A1, data["Conversion"])

N2  = 2    
Wn2 = 0.01  
B2, A2 = signal.butter(N2, Wn2)
precio_filtrado2 = signal.filtfilt(B2,A2, data["Conversion"])

N3  = 3    
Wn3 = 0.01  
B3, A3 = signal.butter(N3, Wn3)
precio_filtrado3 = signal.filtfilt(B3,A3, data["Conversion"])

plt.figure(figsize=(10,15))
plt.subplot(3,1,1)
plt.plot(data["Fecha"],data["Conversion"], label = "Original")
plt.plot(data["Fecha"],precio_filtrado1, label = "Filtrado")
plt.xlabel("Fecha")
plt.ylabel("Precio")
plt.legend(loc=0.0)
plt.subplot(3,1,2)
plt.plot(data["Fecha"],data["Conversion"], label = "Original")
plt.plot(data["Fecha"],precio_filtrado2, label = "Filtrado")
plt.xlabel("Fecha")
plt.ylabel("Precio")
plt.legend(loc=0.0)
plt.subplot(3,1,3)
plt.plot(data["Fecha"],data["Conversion"], label = "Original")
plt.plot(data["Fecha"],precio_filtrado3, label = "Filtrado")
plt.xlabel("Fecha")
plt.ylabel("Precio")
plt.legend(loc=0.0)
plt.savefig("Filtros.png")


# Correlaciones

ruido1 = data["Conversion"]-precio_filtrado1
ruido2 = data["Conversion"]-precio_filtrado2
ruido3 = data["Conversion"]-precio_filtrado3

corr1=np.correlate(ruido1,ruido1,mode="full")
corr2=np.correlate(ruido2,ruido2,mode="full")
corr3=np.correlate(ruido3,ruido3,mode="full")

plt.figure(figsize=(10,15))
plt.subplot(3,1,1)
plt.plot(np.abs(corr1[len(corr1)//2:]))
plt.subplot(3,1,2)
plt.plot(np.abs(corr2[len(corr2)//2:]))
plt.subplot(3,1,3)
plt.plot(np.abs(corr3[len(corr3)//2:]))
plt.savefig("Correlaciones.png")

