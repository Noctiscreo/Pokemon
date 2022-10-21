import logs
import pokemonDatabase
import pokemonCard
import random


class Deck:
    def __init__(self):
        self.deckLogs = logs.Logger()
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
            self.deckLogs.logger.error(e)
            self.size = None
            self.deck = [None]
        self.deck1 = [None]
        self.deck1Size = None
        self.deck2 = [None]
        self.deck2Size = None

    def splitDeck(self):
        fullDeck = Deck()
        numDecks = 2
        halfDeck = int((fullDeck.size / numDecks) // 1)
        self.deck1 = random.sample(fullDeck.deck, halfDeck)
        self.deck1Size = len(self.deck1)
        self.deck2 = [card for card in fullDeck.deck if card not in self.deck1]
        if len(self.deck1) != len(self.deck2):
            self.deck2.pop(random.randrange(halfDeck + 1))
        self.deck2Size = len(self.deck2)
        self.deckLogs.logger.info("Deck was split and assigned to deck 1 and deck 2")

    def shuffleFullDeck(self):
        random.shuffle(self.deck)
        self.deckLogs.logger.info("Full deck was shuffled")

    def shuffleDeck1(self):
        random.shuffle(self.deck1)
        self.deckLogs.logger.info("Deck 1 was shuffled")

    def shuffleDeck2(self):
        random.shuffle(self.deck2)
        self.deckLogs.logger.info("Deck 2 was shuffled")

    def getTopCardDeck1(self):
        self.deckLogs.logger.info("Retrieving top card of deck 1")
        return self.deck1[0]

    def getTopCardDeck2(self):
        self.deckLogs.logger.info("Retrieving top card of deck 2")
        return self.deck2[0]

    def cycleDeck1(self):
        self.deck1.append(self.deck1.pop(0))
        self.deckLogs.logger.info("Moving top card of deck 1 to bottom")

    def cycleDeck2(self):
        self.deck2.append(self.deck2.pop(0))
        self.deckLogs.logger.info("Moving top card of deck 2 to bottom")
