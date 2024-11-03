from fastapi import FastAPI
from data import df
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Instance api
app = FastAPI()

dias = {
        "lunes": "Monday",
        "martes": "Tuesday",
        "miércoles": "Wednesday",
        "jueves": "Thursday",
        "viernes": "Friday",
        "sábado": "Saturday",
        "domingo": "Sunday"
    }

meses = {
        "enero": "January",
        "febrero": "February",
        "marzo": "March",
        "abril": "April",
        "mayo": "May",
        "junio": "June",
        "julio": "July",
        "agosto": "August",
        "septiembre": "September",
        "octubre": "October",
        "noviembre": "November",
        "diciembre": "December"
    }

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    # Convierte el input en minusculas y elimina los espacios
    mes = mes.lower().strip()

    # Verifica si el mes esta en el diccionario
    if mes in meses:
        # Obtiene el correspondiente nombre del mes en ingles
        mes_en_ingles = meses[mes]
        # Cuenta las peliculas que contienen releas_dates en el nombre del mes en ingles
        cantidad = len(df[df["release_date"].str.contains(mes_en_ingles, case=False)])
    else:
        # Retorna un mensaje indicando que no se estrenaron peliculas en ese mes
        return {'mes': mes, 'cantidad': f"No se encontraron películas estrenadas en el mes de {mes}"}

    # Retorna el mes y la cantidad de peliculas estrenadas
    return {'En el mes de': mes, 'Esta fue la cantidad de peliculas estrenadas': cantidad}

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    # Convierte el input en minusculas y elimina los espacios
    dia = dia.lower().strip()

    if dia in dias: # Verifica si dia existe dentro de nuestro diccionario
        dia_en_ingles = dias[dia] # Convierte el dia a ingles
        peliculas = df[df["release_day"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower().str.contains(dia_en_ingles, case=False)]

        if peliculas.empty:
            return {'Para el dia': dia, 'cantidad': f"No se encontraron películas estrenadas en los días {dia}"}

        # Retorna el dia y la cantidad de peliculas estrenadas
        return {'Para el dia': dia, 'Esta fue la cantidad de peliculas estrenadas': len(peliculas)} 
    else:
        # Retorna un mensaje con un dia no reconocido
        return {'dia': dia, 'mensaje': f"No se reconoce el día '{dia}'. Por favor, ingresa un día de la semana válido en español o capaz olvidaste el acento."}

@app.get("/score_titulo/{titulo_pelicula}")
def score_titulo(titulo_pelicula: str):
    # Filtrar las peliculas por el nombre especifico de la pelicula
    peliculas = df[df["title"].str.lower() == titulo_pelicula.lower()]
    # Chequea si consiguio la pelicula
    if peliculas.empty:
        return {'titulo': titulo_pelicula, 'año': None, 'popularidad': "No se encontró la filmación especificada."}
    # Ordena las peliculas el año de estreno en orden ascendente
    peliculas_ordenadas = peliculas.sort_values(by="release_year")
    # Crea una lista vacia para almacenar las respuestas
    respuesta = []
    # Itera sobre las peliculas ordenadas
    for index, row in peliculas_ordenadas.iterrows():
        # Extrae el titulo, año de estreno, y el valor de popularidad para cada pelicula
        title = row["title"]
        year_released = row["release_year"]
        score = row["popularity"]
        # Crea un diccionario para la pelicula y lo agrega a la respuesta
        respuesta.append({'titulo': title, 'año': year_released, 'popularidad': score})

    return respuesta

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo:str):
    # Filter films based on the specified film title
    peliculas = df[df["title"].str.lower() == titulo.lower()]
    # Check if films are found
    if peliculas.empty:
        return "No se encontró la filmación especificada."
    
    # Initialize an empty list to store the responses
    respuestas = []
    
    # Iterate over the filtered films
    for _, row in peliculas.iterrows():
        cantidad_votos = row["vote_count"]
        
        if cantidad_votos < 2000:
            continue  # Skip this movie if you don't meet the minimum number of votes
        
        # Extract the vote count, title, release year, and average vote of each film
        titulo = row["title"]
        anio = row["release_year"]
        promedio_votos = row["vote_average"]

        # Create a dictionary for the film with its information
        respuesta = {'titulo': titulo, 'anio': anio, 'voto_total': cantidad_votos, 'voto_promedio': promedio_votos}
        respuestas.append(respuesta)

    # Check if no films meet the minimum vote count requirement
    if not respuestas:
        return "No se encontraron peliculas que cumplan con la cantidad mínima de votos requerida (2000 votos)."
    
    return respuesta

@app.get("/get_actor/{actor_name}")
def get_actor(actor_name: str):
    # Filter films based on the specified actor name
    peliculas_actor = df[df["actor_name_funct"].str.contains(fr"\b{actor_name}\b", case=False, regex=True, na=False)]
    
    # Check if films are found for the actor
    if peliculas_actor.empty:
        return "The specified actor was not found."
    
    # Calculate the number of films for the actor
    film_count = len(peliculas_actor)
    
    # Calculate the total return of the actor's films
    total_return = round(peliculas_actor["return"].sum(),2)
    
    # Calculate the average return per film
    average_return = round(total_return / film_count,2)
    
    # Return a dictionary containing the actor's name, the number of films, total return, and average return
    return {'actor': actor_name, 'film_count': film_count, 'total_return': total_return, 'average_return': average_return}

@app.get("/get_director/{director_name}")
def get_director(director_name: str):
    # Filter movies based on the specified director name
    director_peliculas = df[df['Director'].str.contains(fr"\b{director_name}\b", case=False, regex=True, na=False)]

    # Check if movies are found for the director
    if director_peliculas.empty:
        return "The specified director was not found."

    # Calculate the number of movies for the director
    film_count = len(director_peliculas)

    # Calculate the total return of the director's movies
    total_return = round(director_peliculas['return'].sum(), 2)

    # Create a table of movies with selected columns and round the values to 2 decimal places
    movies_table = round(director_peliculas[['title', 'release_year', 'return', 'budget', 'revenue']], 2)

    
    return {'Director': director_name,
            'retorno_total_director': total_return,
            'total_peliculas': film_count,
            'peliculas': movies_table.to_dict(orient='records')}

# Function to transform the columns for the vectrizer
def clean_column_values(df, column_name):
    df[column_name] = df[column_name].astype(str).str.replace('[', '', regex=False)
    df[column_name] = df[column_name].astype(str).str.replace(']', '', regex=False)
    df[column_name] = df[column_name].astype(str).str.replace("'", '', regex=False)
    df[column_name] = df[column_name].astype(str).str.replace(",", '', regex=False)
    return df

clean_column_values(df,'actor_id')
clean_column_values(df,'genre_id')


# Create a term frequency matrix using CountVectorizer for relevant columns
vectorizer = CountVectorizer()
term_matrix = vectorizer.fit_transform(df['genre_id'] + ' ' + df['actor_id'] + ' ' + df['title'] + ' ' + df['popularity'].astype(str) + ' ' + df['vote_average'].astype(str))

# Function to get movies similar to a given movie
def obtener_peliculas_similares(titulo, n=5):
    titulo = titulo.lower()
    indice_pelicula = df[df['title'].str.lower() == titulo].index
    if len(indice_pelicula) == 0:
        return 'No se encontró la película, revisa si está bien escrita'

    indice_pelicula = indice_pelicula[0]
    vector_pelicula = term_matrix[indice_pelicula]
    similaridades = cosine_similarity(vector_pelicula, term_matrix)[0]
    indices_similares = similaridades.argsort()[::-1][1:n+1]  # Exclude the given movie

    # Sort the similar movies based on similarity score
    indices_similares_sorted = sorted(indices_similares, key=lambda x: similaridades[x], reverse=True)
    peliculas_similares = df.iloc[indices_similares_sorted]['title'].tolist()
    return peliculas_similares

@app.get('/recomendacion/{titulo}')
def recomendacion(titulo: str):
    peliculas_recomendadas = obtener_peliculas_similares(titulo)
    return {'lista recomendada': peliculas_recomendadas}