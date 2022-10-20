import logs
import pokemonDatabase
import pokemonCard
import random


class Deck:
    def __init__(self):
        DeckLogs = logs.Logger()
        try:
            pokemonDictList = pokemonDatabase.findAllPokemon()
            pokemonDeck = []
            for pokemon in pokemonDictList:
                tempCard = pokemonCard.Pokemon()
                tempCard.name = pokemon["Name"]
                tempCard.attack = pokemon["Attack"]
                tempCard.defence = pokemon["Defence"]
                tempCard.type1 = pokemon["Type1"]
                if pokemon["Type2"] != "None":
                    tempCard.type2 = pokemon["Type2"]
                pokemonDeck.append(tempCard)
            self.size = len(pokemonDeck)
            self.deck = pokemonDeck
        except Exception as e:
            DeckLogs.logger.error(e)
            self.size = None
            self.deck = [None]
        self.deck1 = [None]
        self.deck1Size = None
        self.deck2 = [None]
        self.deck2Size = None

    def splitDeck(self):
        fullDeck = Deck()
        numDecks = 2
        halfDeck = (fullDeck.size / numDecks) // 1
        self.deck1 = random.sample(fullDeck.deck, halfDeck)
        self.deck1Size = len(self.deck1)
        self.deck2 = [card for card in fullDeck.deck if card not in self.deck1]
        self.deck2Size = len(self.deck2)

    def shuffleFullDeck(self):
        random.shuffle(self.deck)

    def shuffleSubDecks(self):
        random.shuffle(self.deck1)
        random.shuffle(self.deck2)

    def getTopCardDeck1(self):
        return self.deck1[0]

    def getTopCardDeck2(self):
        return self.deck2[0]

    def cycleDeck1(self):
        self.deck1.append(self.deck1.pop(0))

    def cycleDeck2(self):
        self.deck2.append(self.deck2.pop(0))
