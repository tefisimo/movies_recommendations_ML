![HenryLogo](https://assets.soyhenry.com/henry-landing/assets/Henry/logo-white.png)

# Proyecto Individual 1: Machine Learning Operations (MLOps)

## Alumno: Gustavo Gonzalez

## Introduccion

Esta aplicación web, desarrollada con FastAPI y desplegada en Render, ofrece una plataforma completa para explorar el mundo del cine. Con funciones como búsqueda avanzada, recomendaciones personalizadas y análisis de datos, los usuarios pueden descubrir nuevas películas, profundizar en sus favoritas y obtener información detallada sobre la industria cinematográfica. El sistema de recomendación, basado en algoritmos de similitud y machine learning, garantiza sugerencias precisas y relevantes.

## Requisitos previos

Tener instalado Python y un editor de texto como Visual Studio Code.

Clonar el repositorio del link https://github.com/tefisimo/movies_recommendations_ML

El cual posee los archivos:
* README.md : Readme del proyecto.
* movies_limpio.csv : Dataset para ser consumido por el modelo de ML.
* credits_limpio.csv : Dataset para ser consumido por el modelo de ML.
* data.py : Archivo python que contiene la creacion del dataframe utilizado en el archivo "main.py" a partir del merge por "id" de los datasets ya limpios.
* main.py : Archivo python que contiene el codigo con las funciones y endpoints de FastApi.
* requirements.txt : Archivo que contiene las librerias con la version necesaria de cada una para el proyecto.

Ademas, pero no necesarios para la ejecucion del modelo, los archivos ETL y EDA en formato "ipynb" con el procedimiento especificado para el tratado de "extraccion, transformacion y carga", asi como tambien "análisis exploratorio de datos" de los datasets originales.

## Instalación

Instalar dependencias ejecutando en una terminal: pip install -r requirements.txt

Asegúrate de ejecutar este comando desde la ubicación raíz del proyecto, donde se encuentra el archivo requirements.txt.

## Uso

Ejecutar el proyecto a partir del archivo "main.py" que importa el dataframe creado en el archivo "data.py", para asi de esta manera poder ejecutar las funciones requeridas por endpoint de FastApi

## Deployment

Para realizar el deployment utilice Render para poder utilizar la API en una pagina web. El link para ingresar es: https://movies-recommendations-ml.onrender.com/docs

En este link se encuentran las 7 funciones desarrolladas.

## Funciones desarrolladas

Para ejecutar los links de cada funcion debe estar en funcionamiento la API desde el archivo main.py

### 1° Función: Cantidad de filmaciones estrenadas por mes.

La funcion recibe un mes en español y devuelve la cantidad de películas estrenadas en ese mes.

Resumen de funcionamiento:

La función recibe el mes como un parámetro de tipo str en español, lo cual convierte a minúsculas y elimina los espacio. Luego, mapea dentro de un diccionario los nombres de los meses en español a los nombres de los meses en inglés y verifica si el mes ingresado es válido. A continuación, determina la cantidad de peliculas que contengan ese mes para la columna 'release_date' y retorna el mensaje para ese mes con la cantidad de peliculas estrenadas.

### 2° Función: Cantidad de filmaciones estrenadas por día de la semana.

La funcion recibe un día en español, por ejemplo "viernes", y devuelve la cantidad de películas estrenadas en ese día.

Resumen de funcionamiento:

La función recibe el dia como un parámetro de tipo str en español, lo cual convierte a minúsculas y elimina los espacio. Luego, mapea dentro de un diccionario los nombres de los dias en español a los nombres de los dias en inglés y verifica si el dia ingresado es válido. A continuación, determina la cantidad de peliculas que contengan ese dia para la columna 'release_day' y retorna el mensaje para ese dia con la cantidad de peliculas estrenadas.

### 3° Función: Score Titulo.

Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.

Resumen de funcionamiento:

Realiza la comparacion por el nombre especifico de la pelicula. Ordena las peliculas por el año de estreno en orden ascendente, iterando sobre ellas para extraer el titulo, el año de estreno y el valor de la popularidad agregandolos a una lista creada que luego sera retornada como respuesta.


### 4° Función: Cantidad de votos y valor promedio de las votaciones de la filmación.

Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario no se devuelve ningún valor. 

Resumen de funcionamiento:

Realiza la comparacion por el nombre especifico de la pelicula, crea una lista para almacenar las respuestas e itera sobre las peliculas filtradas en la comparacion a partir de la condicion de que sea mayor a 2000 valoraciones y extrae el titulo, el año de estreno y el promedio de votos

### 5° Función: Éxito de un actor.

Se ingresa el nombre de un actor que se encuentre dentro del dataset debiendo devolver el éxito del mismo medido a través del retorno, la cantidad de películas en las que ha participado y el promedio de retorno. 

Resumen de funcionamiento:

Filtra las peliculas basado en el nombre del actor y calcula el numero de peliculas para el actor. Luego realiza la suma de los retornos relacionados al actor y calcula el promedio de retornos.

### 6° Función: Éxito de un director.

Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

Resumen de funcionamiento:

Filtra las peliculas basandose en el nombre del director, calcula el numero de peliculas para el director y realiza la suma de los retornos. A continuacion procede a crear una tabla de peliculas con la extraccion del titulo de cada una de ellas, el año de estreno, el retorno individual, el budget y revenue.

### 7° Función: Recomendacion de peliculas.

La función recomendacion(titulo) tiene como objetivo recomendar películas similares a una película dada.Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

Resumen de funcionamiento:

Preprocesamiento de datos: Convierte los valores de la columna 'genre_id' y 'actor_id' en cadenas de textos limpias una vez pasadas por una funcion llamada 'clean_column_values'.
Crea una matriz para el texto del título de las películas, el genero, el actor, la popularidad y el promedio de votos utilizando la biblioteca CountVectorizer.
Calcula la similitud del coseno entre los títulos de las películas.

La función recomendacion realiza lo siguiente:

Principalmente parte de la ejecucion de una funcion llamada 'obtener_peliculas_similares', la cual consta de: 

Comparar el titulo ingresado con los titulos de la columna 'title' del DataFrame.

Encontar el índice de la película con el título dado.

Calcular las puntuaciones de similitud de todas las películas con la película dada utilizando cosine_similarity

Obtener los índices de las películas más similares (excluyendo la película dada).

Ordenar las películas por puntaje de similitud en orden descendente.

Para al final obtener una lista de las peliculas similares a partir de esos indices.

Una vez realizado este proceso, la funcion recomendacion devuelve una lista con los títulos de las 5 películas más similares como resultado.

## ETL 
Se realizó el análisis ETL a partir de las solicitudes planteadas por la plataforma, los cuales fueron:

* Desanidación de las columnas **`belongs_to_collection`**, **`production_companies`**, **`genres`**, **`production_countries`**, **`spoken_languages`**, **`cast`**, **`crew`**.
* Rellenar valores nulos de las columnas **`revenue`**, **`budget`**.
* Eliminación de los valores nulos de la columna **`release date`**.
* Formateo de las fechas y creación de la columna **`release_year`**.
* Creación de la columna **`return`** a partir de la división de las columnas **`revenue`** y **`budget`**
* Eliminación de las columnas innecesarias: **`video`**,**`imdb_id`**,**`adult`**,**`original_title`**,**`poster_path`** y **`homepage`**.

## EDA
Se realizó el análisis exploratorio de datos con el objetivo de identificar insights que permitieran orientar de mejor manera el proceso de elaboracion del modelo de recomendación de películas.

## Pagina Web API en Render
https://movies-recommendations-ml.onrender.com/docs

## Video del proyecto:
https://drive.google.com/file/d/1ZwJAUO-YFswxdj3uyGRyQ41iT2Y1RlWv/view?usp=drive_link

## Créditos
El recurso externo que mayormente use para crear mi proyecto fue chatGPT y la ayuda de mis compañeros de cohorte en los momentos dificiles. 

## Contacto
Email: gustavoadolfogonz@gmail.com
Linkedin: Gustavo Gonzalez, link: https://www.linkedin.com/in/gustavo-gonzalez-data/
