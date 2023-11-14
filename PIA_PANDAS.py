# -*- coding: utf-8 -*-
"""PIA_PANDAS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WmHbyUBw2ieFaytR6REARr8Rty_oWry_
"""

from google.colab import files

import pandas as pd
import io
import numpy as np
import matplotlib.pyplot as plt

uploaded = files.upload()

uploaded

dataframe = pd.read_csv(io.StringIO(uploaded['PIA (1).csv'].decode('latin-1')))

print(dataframe)

#Devuelve las primeras 5 filas del dataframe o del valor que lo indiques
dataframe.head(5)

#Filtrado de datos
condicional = dataframe['PrecioUnitario'] > 170
filtro = dataframe[condicional]

print(filtro)

#Filtrado booleano
condicion_booleana = (dataframe['PrecioTotal'] > 150) & (dataframe['PrecioTotal'] < 300)
resultado_filtrados = dataframe[condicion_booleana]
print(resultado_filtrados)

#Uso de groupby
venta_por_producto = dataframe.groupby('Producto')['Cantidad'].sum()
producto_mas_vendido = venta_por_producto.idxmax()
print(f"El producto más vendido es: {producto_mas_vendido}")

#Media. Mediana y moda
media = dataframe['PrecioTotal'].mean()
mediana = dataframe['PrecioTotal'].median()
moda = dataframe['PrecioTotal'].mode()
print(f"Media: {media}")
print(f"Mediana: {mediana}")
print(f"Moda: {moda}")

#Grafica de ventas
ventas_por_producto = dataframe.groupby('Producto')['Cantidad'].sum()
plt.bar(ventas_por_producto.index, ventas_por_producto.values, color='skyblue')


plt.xlabel('Producto')
plt.ylabel('Ventas')
plt.title('Ventas por Producto')


plt.show()
