# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 22:13:18 2021

@author: Napoleón Pérez
"""

# import the streamlit library
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from textblob import TextBlob 
from PIL import Image

# give a title to our app
st.title('RAVN CRMB Sentimental Analysis')

from PIL import Image
image = Image.open('/Users/napoleonperez/Desktop/sentiment_app/TIK-TOK-ANALISIS-NLP/crmb.png')

st.image(image, caption='Logo de CRMB', use_column_width=True)



# TAKE WEIGHT INPUT in kgs

st.subheader("Enter your text to verify ")
comment  = st.text_input(" ", "please type here...")


# compare status value
x=TextBlob(comment)
sentiment_polarity=x.sentiment.polarity

# check if the button is pressed or not
if(st.button('Submit')):
    
    #result = x.title()
    
    if(sentiment_polarity < 0):
        st.error("The given comment is Negative")
    elif(sentiment_polarity ==0):
        st.warning("The given comment is Neutral")
    elif(sentiment_polarity > 0 ):
        st.success("The given comment is Positive ")
        
# Para obtener la lista de "stopwords" y asi descartarlas
import nltk
from nltk.corpus import stopwords

#Generación de lista de signos de puntuación
import string  

def limpiar_puntuacion_stopwords(texto):
  """
  
  """
  puntuacion = []
  for s in string.punctuation:
      puntuacion.append(str(s))
  sp_puntuacion = ["¿", "¡", "“", "”", "…", ":", "–", "»", "«", "?", "!"]    

  puntuacion += sp_puntuacion

  #Reemplazamos signos de puntuación por "":
  for p in puntuacion:
      texto_limpio = texto.lower().replace(p,"")

  for p in puntuacion:
      texto_limpio = texto_limpio.replace(p,"")

  #Reemplazamos stop_words por "":    
  for stop in stop_words:
      texto_limpio_lista = texto_limpio.split()
      texto_limpio_lista = [i.strip() for i in texto_limpio_lista]
      try:
          while stop in texto_limpio_lista: texto_limpio_lista.remove(stop)
      except:
          print("Error")
          pass
      texto_limpio= " ".join(texto_limpio_lista)

  return texto_limpio


def generar_nube_de_palabras(input, uploded_file = None):  
  """
  Funcion para hacer la nube de palabras en base a un .csv especifico que tenga una columna "ShareCommentary" como se encuentra
  en el archivo Share.csv que nos proporciona LinkedIn
  
  Parameters
  ------------------
  input        -> Para decidir si se usa el 'template' o se toma el archivo cargandolo ('file')
  uploded_file -> Informacion el csv cargado
  
  
  Returns
  ------------------
  None
  """
  if input == 'file':
    df_shares = pd.read_csv(uploded_file)
  elif input == 'template':
    url = 'https://github.com/crmbhq/crmb-phyton-machinelearning/blob/main/datasets/comments/cleancomments.csv'
    df_shares = pd.read_csv(url)
    
  texto_de_publicaciones = df_shares['message']
  texto_de_publicaciones = [i for i in texto_de_publicaciones if type(i) == str]

  # Uso set para borrar repetidos
  texto = [i for i in set(texto_de_publicaciones) if type(i) == str]

  texto = ''.join(texto)

  # Limpiamos
  clean_texto = limpiar_puntuacion_stopwords(texto)

  # Hacemos el wordcloud
  word_cloud = WordCloud(height=800, width=800, background_color='white',max_words=100, min_font_size=5).generate(clean_texto)
  fig, ax = plt.subplots()

  # Sacamos los ticks de los ejes 
  ax.axis('off')

  ax.imshow(word_cloud)
  title_alignment = """
  <style> #the-title { 
  text-align: center
  }
  </style>"""

  st.markdown(title_alignment, unsafe_allow_html=True)

  st.title("Tu nube de palabras ")
  fig  # 👈 Draw a Matplotlib chart
  
  fig.savefig("nube.png")
  
  st.markdown('### Descargar la imagen')
  with open("nube.png", "rb") as file:
    btn = st.download_button(
      label="Guardar imagen",
      data=file,
      file_name="nube.png",
      mime="image/png"
    )
 
# Obtengo la lista de stopwords (conectores, preposiciones, etc) en espanol gracias a nltk
nltk.download('stopwords')
stop_words = stopwords.words('spanish')


if __name__ == "__main__": 

  st.title('☁️ Wordcloud Comments ☁️')
  st.markdown("Creado por [Napoleon Perez]")

  st.markdown('## Presioná el botón **Browse files** y luego seleccioná tu archivo *Comment.csv*')
  pressed = st.button('Ver archivo actual')

  # Cargamos template
  if pressed:
     generar_nube_de_palabras('template')
  
  # Subir archivo
  uploaded_file = st.file_uploader("Select a file", type=["csv"])

  # Cargamos desde archivo
  if uploaded_file is not None:
    generar_nube_de_palabras('file', uploaded_file)

        
