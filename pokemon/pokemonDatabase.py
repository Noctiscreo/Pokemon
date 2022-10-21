import sqlite3
import pandas as pd
import logs


class Database:
    _instance = None

    def __init__(self):
        self.databaseLogs = logs.Logger()
        try:
            self.conn = sqlite3.connect('../Pokemon/Pokemon.db')
            self.cursor = self.conn.cursor()
        except Exception as e:
            self.databaseLogs.logger.error(e)
        self.empty = None
        self.checkIfPopulated()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            databaseConstructLogs = logs.Logger()
            try:
                conn = sqlite3.connect('../Pokemon/Pokemon.db')
                cursor = conn.cursor()
                createPokemonDatabase = '''
                    CREATE TABLE IF NOT EXISTS "PokemonDatabase" (
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
                conn.close()
                selectData = "SELECT * FROM PokemonDatabase"
                pokemonDatabaseDF = pd.read_sql_query(selectData, conn)
                if pokemonDatabaseDF.empty:
                    databaseConstructLogs.logger.info("PokemonDatabase Table created.")
            except Exception as e:
                databaseConstructLogs.logger.error(e)
        return cls._instance

    def commitToDatabase(self, command: str, data: tuple) -> sqlite3.Connection.cursor:
        try:
            self.cursor.execute(command, data)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            self.databaseLogs.logger.error(e)

    def checkIfPopulated(self):
        selectData = f'''
                SELECT * FROM PokemonDatabase
                '''
        pokemonDatabaseDF = pd.read_sql_query(selectData, self.conn)
        if pokemonDatabaseDF.empty:
            self.empty = True
        else:
            self.empty = False
        return self.empty


def addPokemonToDatabase(pokemonData: list):
    addPokemonToDatabaseLogs = logs.Logger()
    for pokemon in pokemonData:
        try:
            pokemonInsertSQL = '''
                    INSERT INTO PokemonDatabase
                    (Name, Artwork, Attack, Defence, Type1, Type2)
                    VALUES (?, ?, ?, ?, ?, ?)
                    '''
            pokemonInsertSQLData = (pokemon["Name"], pokemon["Artwork"],
                                    pokemon["Attack"], pokemon["Defence"],
                                    pokemon["Type1"], pokemon["Type2"])
            Database().commitToDatabase(pokemonInsertSQL, pokemonInsertSQLData)
        except Exception as e:
            addPokemonToDatabaseLogs.logger.error(e)


def findPokemonFromName(pokemonName: str) -> dict:
    findPokemonFromNameLogs = logs.Logger()
    selectData = f'''
        SELECT * FROM PokemonDatabase
        WHERE Name = "{pokemonName}"
        '''
    pokemonNameDF = pd.read_sql_query(selectData, Database().conn)
    if pokemonNameDF.empty:
        findPokemonFromNameLogs.logger.info(f"No pokemon with name: {pokemonName}")

    pokemon = {"Name": pokemonNameDF["Name"][0], "Artwork": pokemonNameDF["Artwork"][0],
               "Attack": pokemonNameDF["Attack"][0], "Defence": pokemonNameDF["Defence"][0],
               "Type1": pokemonNameDF["Type1"][0], "Type2": pokemonNameDF["Type2"][0]}
    return pokemon


def findAllPokemon() -> list:
    findAllPokemonLogs = logs.Logger()
    selectData = f'''
        SELECT * FROM PokemonDatabase
        '''
    allPokemonDF = pd.read_sql_query(selectData, Database().conn)
    if allPokemonDF.empty:
        findAllPokemonLogs.logger.info("No pokemon in database")
    allPokemonDataList = []
    for row in allPokemonDF.itertuples():
        try:
            pokemon = {"Name": row.Name, "Artwork": row.Artwork,
                       "Attack": row.Attack, "Defence": row.Defence,
                       "Type1": row.Type1, "Type2": row.Type2}
            allPokemonDataList.append(pokemon)
        except Exception as e:
            findAllPokemonLogs.logger.error(e)
    return allPokemonDataList


def findAllNames() -> list:
    findAllPokemonLogs = logs.Logger()
    selectData = f'''
        SELECT * FROM PokemonDatabase
        ORDER BY Name;
        '''
    allPokemonDF = pd.read_sql_query(selectData, Database().conn)
    if allPokemonDF.empty:
        findAllPokemonLogs.logger.info("No pokemon in database")
    allPokemonNamesList = []
    for row in allPokemonDF.itertuples():
        try:
            pokemon = {"Name": row.Name}
            allPokemonNamesList.append(pokemon)
        except Exception as e:
            findAllPokemonLogs.logger.error(e)
    return allPokemonNamesList
