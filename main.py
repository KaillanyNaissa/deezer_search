import requests
import pandas as pd
import time

BASE_URL = "https://api.deezer.com"

GENEROS = [
    "rock",
    "pop",
    "rap",
    "jazz",
    "classical"
]


# Quantidade de músicas por gênero
LIMITE = 25

todas_musicas = []

# COLETA DOS DADOS

for genero in GENEROS:

    print(f"\nBuscando músicas de: {genero}")

    url = f"{BASE_URL}/search/track"

    parametros = {
        "q": genero,
        "limit": LIMITE
    }

    resposta = requests.get(
        url,
        params=parametros,
        timeout=10
    )

    print("Status:", resposta.status_code)

    # Verifica se a requisição deu certo
    resposta.raise_for_status()

    # Transforma JSON em Python
    dados = resposta.json()

    print("Resultados encontrados:", dados["total"])


    # Percorre as músicas retornadas
    for musica in dados["data"]:

        registro = {
            "id_musica": musica["id"],
            "musica": musica["title"],

            "id_artista": musica["artist"]["id"],
            "artista": musica["artist"]["name"],

            "id_album": musica["album"]["id"],
            "album": musica["album"]["title"],

            "duracao_segundos": musica["duration"],
            "rank": musica["rank"],

            # Gênero usado na pesquisa
            "genero_pesquisado": genero
        }

        todas_musicas.append(registro)


    # Pequena pausa entre as requisições
    time.sleep(1)


# CRIAR DATAFRAME

df = pd.DataFrame(todas_musicas)

# REMOVER DUPLICIDADES

df = df.drop_duplicates(
    subset=["id_musica", "genero_pesquisado"]
)

# SALVAR CSV

df.to_csv(
    "dados_deezer.csv",
    index=False,
    encoding="utf-8-sig"
)

# RESULTADO

print("\n===================================")
print("COLETA FINALIZADA")
print("===================================")

print("Total de registros:", len(df))

print("\nColunas:")
print(df.columns.tolist())

print("\nPrimeiras músicas:")
print(df.head())

print("\nArquivo criado:")
print("dados_deezer.csv")