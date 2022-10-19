import sqlite3
import pandas as pd

# import logs
import logging

# logger = logging.getLogger("logs.pokemonDatabase")


def databaseConnect() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect('Pokemon.db')
        return conn
    except KeyError as e:
        # logger.error(e)
        print(e)


def createTable(conn: sqlite3.Connection):
    cursor = conn.cursor()
    try:
        createPokemonDatabase = '''
            CREATE TABLE "PokemonDatabase" (
            "Name"	TEXT,
            "Artwork"	TEXT,
            "Attack"	INTEGER,
            "Defence"	INTEGER,
            "Type1"	TEXT,
            "Type2"	TEXT
            PRIMARY KEY("Name")
            );
            '''
        cursor.execute(createPokemonDatabase)
        conn.commit()
    except sqlite3.OperationalError as e:
        # logger.error(e)
        print(e)


def commitToDatabase(conn: sqlite3.Connection, command: str) -> sqlite3.Connection.cursor:
    cursor = conn.cursor()
    try:
        cursor.execute(command)
        conn.commit()
    except sqlite3.IntegrityError as e:
        # logger.error(e)
        print(e)
    return cursor


def findPokemonFromName(conn: sqlite3.Connection, pokemonName: str) -> dict:
    selectData = f'''
        SELECT * FROM PokemonDatabase
        WHERE Name = "{pokemonName}"
        '''
    pokemonNameDF = pd.read_sql_query(selectData, conn)
    pokemon = {"Name": pokemonNameDF["Name"][0], "Artwork": pokemonNameDF["Artwork"][0],
               "Attack": pokemonNameDF["Attack"][0], "Defence": pokemonNameDF["Defence"][0],
               "Type1": pokemonNameDF["Type1"][0], "Type2": pokemonNameDF["Type2"][0]}
    return pokemon


def addPokemonToDatabase(conn: sqlite3.Connection, pokemonData: list):
    for pokemon in pokemonData:
        try:
            pokemonInsertSql = f'''
                    INSERT INTO PokemonDatabase
                    (Name, Artwork, Attack, Defence, Type1, Type2)
                    VALUES ('{pokemon["Name"]}', '{pokemon["Artwork"]}', 
                    '{pokemon["Attack"]}', '{pokemon["Defence"]}', 
                    '{pokemon["Type1"]}', '{pokemon["Type2"]}')
                    '''
            commitToDatabase(conn, pokemonInsertSql)
        except KeyError as e:
            # logger.error(e)
            print(e)


def findAllPokemon(conn: sqlite3.Connection) -> list:
    selectData = f'''
        SELECT * FROM PokemonDatabase
        '''
    allPokemonDF = pd.read_sql_query(selectData, conn)
    allPokemonList = []
    for row in allPokemonDF.itertuples():
        pokemon = {"Name": row.Name, "Artwork": row.Artwork,
                   "Attack": row.Attack, "Defence": row.Defence,
                   "Type1": row.Type1, "Type2": row.Type2}
        allPokemonList.append(pokemon)
    return allPokemonList
