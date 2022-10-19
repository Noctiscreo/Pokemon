import sqlite3
import pandas as pd
import logs


def databaseConnect() -> sqlite3.Connection:
    databaseConnectLogs = logs.Logger()
    try:
        conn = sqlite3.connect('Pokemon.db')
        return conn
    except Exception as e:
        databaseConnectLogs.logger.error(e)


def createTable():
    createTableLogs = logs.Logger()
    conn = databaseConnect()
    cursor = conn.cursor()
    try:
        createPokemonDatabase = '''
            CREATE TABLE "PokemonDatabase" (
                "Name"	TEXT,
                "Artwork"	TEXT,
                "Attack"	INTEGER,
                "Defence"	INTEGER,
                "Type1"	TEXT,
                "Type2"	TEXT,
                PRIMARY KEY("Name")
            );
            '''
        cursor.execute(createPokemonDatabase)
        conn.commit()
    except sqlite3.OperationalError as e:
        createTableLogs.logger.error(e)
    conn.close()


def commitToDatabase(command: str) -> sqlite3.Connection.cursor:
    commitToDatabaseLogs = logs.Logger()
    conn = databaseConnect()
    cursor = conn.cursor()
    try:
        cursor.execute(command)
        conn.commit()
    except sqlite3.IntegrityError as e:
        commitToDatabaseLogs.logger.error(e)
    conn.close()
    return cursor


def findPokemonFromName(pokemonName: str) -> dict:
    findPokemonFromNameLogs = logs.Logger()
    conn = databaseConnect()
    selectData = f'''
        SELECT * FROM PokemonDatabase
        WHERE Name = "{pokemonName}"
        '''
    pokemonNameDF = pd.read_sql_query(selectData, conn)
    if pokemonNameDF.empty:
        findPokemonFromNameLogs.logger.info(f"No pokemon with name: {pokemonName}")

    pokemon = {"Name": pokemonNameDF["Name"][0], "Artwork": pokemonNameDF["Artwork"][0],
               "Attack": pokemonNameDF["Attack"][0], "Defence": pokemonNameDF["Defence"][0],
               "Type1": pokemonNameDF["Type1"][0], "Type2": pokemonNameDF["Type2"][0]}
    conn.close()
    return pokemon


def addPokemonToDatabase(pokemonData: list):
    addPokemonToDatabaseLogs = logs.Logger()
    createTable()
    for pokemon in pokemonData:
        try:
            pokemonInsertSql = f'''
                    INSERT INTO PokemonDatabase
                    (Name, Artwork, Attack, Defence, Type1, Type2)
                    VALUES ('{pokemon["Name"]}', '{pokemon["Artwork"]}', 
                    '{pokemon["Attack"]}', '{pokemon["Defence"]}', 
                    '{pokemon["Type1"]}', '{pokemon["Type2"]}')
                    '''
            commitToDatabase(pokemonInsertSql)
        except Exception as e:
            addPokemonToDatabaseLogs.logger.error(e)


def findAllPokemon() -> list:
    findAllPokemonLogs = logs.Logger()
    conn = databaseConnect()
    selectData = f'''
        SELECT * FROM PokemonDatabase
        '''
    allPokemonDF = pd.read_sql_query(selectData, conn)
    if allPokemonDF.empty:
        findAllPokemonLogs.logger.info("No pokemon in database")
    allPokemonList = []
    for row in allPokemonDF.itertuples():
        try:
            pokemon = {"Name": row.Name, "Artwork": row.Artwork,
                       "Attack": row.Attack, "Defence": row.Defence,
                       "Type1": row.Type1, "Type2": row.Type2}
            allPokemonList.append(pokemon)
        except Exception as e:
            findAllPokemonLogs.logger.error(e)
    conn.close()
    return allPokemonList


def findAllNames() -> list:
    findAllPokemonLogs = logs.Logger()
    conn = databaseConnect()
    selectData = f'''
        SELECT * FROM PokemonDatabase
        ORDER BY Name;
        '''
    allPokemonDF = pd.read_sql_query(selectData, conn)
    if allPokemonDF.empty:
        findAllPokemonLogs.logger.info("No pokemon in database")
    allPokemonList = []
    for row in allPokemonDF.itertuples():
        try:
            pokemon = {"Name": row.Name}
            allPokemonList.append(pokemon)
        except Exception as e:
            findAllPokemonLogs.logger.error(e)
    conn.close()
    return allPokemonList
