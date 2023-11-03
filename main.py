# Desarrolo del API

import pandas as pd
import numpy as np
from fastapi import FastAPI

## Carga de dataset

items_games_df = pd.read_parquet('datasets/items_games.parquet')
reviews_games_items_df = pd.read_parquet('datasets/reviews_games_items.parquet')
ml_games = pd.read_parquet('datasets/ml_games.parquet')
similarity_matrix = np.load('datasets/similarity_matrix.npz')['arr_0']

## Creación de las funciones del API

app = FastAPI()

### Obtener el año con más horas jugadas por género

@app.get('/playtime_by_genre/')
async def playTimeByGenre(genre:str):
    year = items_games_df.query('genre == @genre').groupby('release_date').agg({'item_playtime': 'sum'}).sort_values(by='item_playtime', ascending=False).index[0]

    return {f"Año con más horas jugadas para el género {genre}": int(year)}

### Obtener el usuario con más horas jugadas acumuladas por género.

@app.get('/user_for_genre/')
async def userForGenre(genre:str):
    user_id = items_games_df.query('genre == @genre').groupby('user_id').agg({'item_playtime': 'sum'}).sort_values(by='item_playtime', ascending=False).index[0]
    temp = items_games_df.query('user_id == @user_id & genre == @genre').groupby('release_date').agg({'item_playtime': 'sum'}).to_dict()['item_playtime']
    playtime_by_year = [{"Año": int(year), "Horas": round(time, 2)} for year, time in temp.items() if time > 0]

    return {f"Usuario con más horas jugadas en el género {genre}": user_id,
            "Horas jugadas": playtime_by_year}

### Obtener el top 3 de los juegos más recomendados en un año dado.

@app.get('/user_recommended/')
async def userRecommended(anio: int):
  top_3 = reviews_games_items_df.query("release_date==@anio & recommend==True & sentiment>=1").groupby('item_name').agg({'recommend': 'count'}).sort_values(by='recommend', ascending=False).iloc[:3].to_dict()['recommend']
  top_3 = list(top_3.keys())
  return {f'Puesto {idx}': title for idx, title in enumerate(top_3, start=1)}

### Obtener el top 3 de los juegos menos recommendados en un año dado.

@app.get('/user_not_recommended/')
async def userNotRecommended(anio: int):
  top_3 = reviews_games_items_df.query("release_date==@anio & recommend==False & sentiment<1").groupby('item_name').agg({'recommend': 'count'}).sort_values(by='recommend', ascending=False).iloc[:3].to_dict()['recommend']
  top_3 = list(top_3.keys())
  return {f'Puesto {idx}': title for idx, title in enumerate(top_3, start=1)}

### Obtener la cantidad de reseñas por categoria de acuerdo con un año dado.

@app.get('/sentiment_by_year/')
async def sentimentPolarityByYear(anio:int):
  polarities = reviews_games_items_df.query('release_date==@anio').sentiment.value_counts().to_dict()
  return {'Negative': polarities[0], 'Neutral': polarities[1], 'Positive': polarities[2]}

## Función de recomendación por id del juego.

@app.get('/user_recommendation/')
async def gameRecommendation(id:int):
  similarity_matrix_idx = ml_games.query('id == @id').index[0]
  similarity_matrix_row = similarity_matrix[similarity_matrix_idx]
  game_row_idxs = similarity_matrix_row.argsort()[-6:-1][::-1]

  ref_game = ml_games.query('id == @id')[['id', 'item_name']].to_dict(orient='records')[0]
  top_5 = ml_games[['id', 'item_name']].iloc[game_row_idxs].to_dict(orient='records')
  return {'game':ref_game, 'top_5': top_5}