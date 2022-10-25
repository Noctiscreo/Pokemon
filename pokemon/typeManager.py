from pokemon.pokemonCard import Pokemon
import logs
import requests
import json
import pandas as pd
import pokemonDatabase


class TypesManager:
    _instance = None

    def __init__(self):
        self.typesManagerLogs = logs.Logger()
        self.URL = "https://pokeapi.co/api/v2/type/"
        self.df = pd.read_sql_query("SELECT * FROM PokemonType", pokemonDatabase.Database().conn)
        self.multiplier = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TypesManager, cls).__new__(cls)
            databaseTypeConstructLogs = logs.Logger()
            try:
                createPokemonDatabase = '''
                                CREATE TABLE "PokemonType" (
                                    "Type"	TEXT,
                                    "DDFrom"	TEXT,
                                    "DDTo"	TEXT,
                                    "HDFrom"	TEXT,
                                    "HDTo"	TEXT,
                                    "NDFrom"	TEXT,
                                    "NDTo"	TEXT,
                                    PRIMARY KEY("Type")
                                );
                                '''
                pokemonDatabase.Database().cursor.execute(createPokemonDatabase)
                selectData = "SELECT * FROM PokemonType"
                pokemonDatabaseDF = pd.read_sql_query(selectData, pokemonDatabase.Database().conn)
                if pokemonDatabaseDF.empty:
                    databaseTypeConstructLogs.logger.info("PokemonDatabase Table created.")
            except Exception as e:
                databaseTypeConstructLogs.logger.error(e)
        return cls._instance

    def downloadTypeData(self):
        try:
            content = requests.get(self.URL)
            parsedJson = json.loads(content.text)
            typeTuples = []
            for pokemonType in parsedJson["results"]:
                typeTuples.append((pokemonType["name"], pokemonType["url"]))

            typeDamageRelations = []
            for pokemonType in typeTuples:
                pokemonTypeName = pokemonType[0]
                pokemonTypeData = requests.get(pokemonType[1])
                parsedType = json.loads(pokemonTypeData.text)
                damageRelations = parsedType["damage_relations"]
                tempDamageTypesStrList = []
                for damage in damageRelations.values():
                    tempDamageTypesList = []
                    for damageTypes in damage:
                        tempDamageTypesList.append(damageTypes["name"])
                    tempDamageTypesStr = ",".join(tempDamageTypesList)
                    tempDamageTypesStrList.append(tempDamageTypesStr)
                typeDamageRelations.append(
                    {"damageRelation": {"DDF": tempDamageTypesStrList[0], "DDT": tempDamageTypesStrList[1],
                                        "HDF": tempDamageTypesStrList[2], "HDT": tempDamageTypesStrList[3],
                                        "NDF": tempDamageTypesStrList[4], "NDT": tempDamageTypesStrList[5]
                                        }, "type": pokemonTypeName})
                self.__addTypeDamageRelationsToDatabase(typeDamageRelations)
        except Exception as e:
            self.typesManagerLogs.logger.error(e)

    def __addTypeDamageRelationsToDatabase(self, typeDamageRelations: list):
        for pokemonType in typeDamageRelations:
            try:
                pokemonTypeInsertSQL = '''
                        INSERT INTO PokemonType
                        (Type, DDFrom, DDTo, HDFrom, HDTo, NDFrom, NDTo)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        '''
                pokemonTypeInsertSQLData = (pokemonType["type"], pokemonType["damageRelation"]["DDF"],
                                            pokemonType["damageRelation"]["DDT"], pokemonType["damageRelation"]["HDF"],
                                            pokemonType["damageRelation"]["HDT"], pokemonType["damageRelation"]["NDF"],
                                            pokemonType["damageRelation"]["NDT"])
                pokemonDatabase.Database().commitToDatabase(pokemonTypeInsertSQL, pokemonTypeInsertSQLData)
                self.df = pd.read_sql_query("SELECT * FROM PokemonType", pokemonDatabase.Database().conn)
            except Exception as e:
                self.typesManagerLogs.logger.error(e)

    def getDamagerMultiplier(self, attackType: str, defenderPokemon: Pokemon) -> float:
        self.multiplier = 1
        for defenderPokemonType in [defenderPokemon.type1, defenderPokemon.type2]:
            selectHalfDamageData = f'''
                    SELECT * FROM PokemonType
                    WHERE Type = "{attackType}"
                    AND DDTo LIKE "%{defenderPokemonType}%"
                    '''
            if not pd.read_sql_query(selectHalfDamageData, pokemonDatabase.Database().conn).empty:
                self.multiplier *= 2

            selectHalfDamageData = f'''
                            SELECT * FROM PokemonType
                            WHERE Type = "{attackType}"
                            AND HDTo LIKE "%{defenderPokemonType}%"
                            '''
            if not pd.read_sql_query(selectHalfDamageData, pokemonDatabase.Database().conn).empty:
                self.multiplier *= 0.5

            selectDoubleDamageData = f'''
                            SELECT * FROM PokemonType
                            WHERE Type = "{attackType}"
                            AND NDTo LIKE "%{defenderPokemonType}%"
                            '''
            if not pd.read_sql_query(selectDoubleDamageData, pokemonDatabase.Database().conn).empty:
                self.multiplier *= 0
        return self.multiplier
