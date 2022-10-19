import pokemonDatabase
import random


class Pokemon:
    def __init__(self):
        self.name = None
        self.attack = None
        self.defence = None
        self.type1 = None
        self.type2 = None


class Deck:
    def __init__(self):
        # self.size = int(((len(makeDeck())) / 2) // 1)
        # self.deck = random.sample(makeDeck(), self.size)
        self.size = None
        self.deck = None


def splitDeck():
    pass


def makeDeck() -> list:
    pokemonDictList = pokemonDatabase.findAllPokemon()
    pokemonDeck = []
    for pokemon in pokemonDictList:
        pokemonDeck.append(makeCard(pokemon))
    return pokemonDeck


def makeCard(pokemon: dict):
    tempCard = Pokemon()
    tempCard.name = pokemon["Name"]
    tempCard.attack = pokemon["Attack"]
    tempCard.defence = pokemon["Defence"]
    tempCard.type1 = pokemon["Type1"]
    if pokemon["Type2"] != "None":
        tempCard.type2 = pokemon["Type2"]
    return tempCard
