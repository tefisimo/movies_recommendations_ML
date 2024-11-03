import pandas as pd

# load the data
movies = pd.read_csv('movies_limpio.csv')
credits = pd.read_csv('credits_limpio.csv')

# Join the datasets
df = pd.merge(movies, credits, on=['id', 'id'], how='inner')

# set the date format 
df['release_date'] = pd.to_datetime(df['release_date']).dt.strftime("%Y-%B-%d")
df['release_day'] = pd.to_datetime(df['release_date']).dt.strftime('%A')

# Create actor_name_funct for the API function
df['actor_name_funct'] = df['actor_name']
