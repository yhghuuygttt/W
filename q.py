import streamlit as st
import requests
from bs4 import BeautifulSoup

def buscar_referencias(url, palabra_clave):
    """
    Busca referencias de una palabra clave en una página web.

    Args:
        url (str): La URL de la página web.
        palabra_clave (str): La palabra que se va a buscar.

    Returns:
        list: Una lista de strings con el texto encontrado donde aparece la palabra clave, o un mensaje si no hay resultados.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción si la solicitud falla
        soup = BeautifulSoup(response.content, 'html.parser')

        resultados = []
        for elemento in soup.find_all(text=True):
            if palabra_clave.lower() in elemento.lower():
                resultados.append(elemento.strip())  # Agrega el texto y remueve espacios al inicio y final

        if not resultados:
          return ["No se encontraron referencias para esta palabra."]
        return resultados
    
    except requests.exceptions.RequestException as e:
       return [f"Error al acceder a la página: {e}"]
    except Exception as e:
       return [f"Error inesperado: {e}"]
    

def main():
    st.title("Buscador de Referencias en Página Web")

    url_pagina = st.text_input("Ingresa la URL de la página web:", "https://mi.tv")
    palabra_busqueda = st.text_input("Ingresa la palabra que quieres buscar:")

    if st.button("Buscar"):
      if palabra_busqueda:
        with st.spinner("Buscando..."): # Agrega un spinner
            referencias = buscar_referencias(url_pagina, palabra_busqueda)
        st.subheader("Resultados de la búsqueda:")
        for ref in referencias:
            st.markdown(f"- {ref}")
      else:
        st.warning("Por favor, ingresa una palabra de búsqueda")

if __name__ == "__main__":
    main()