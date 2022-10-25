from logs import Logger
from pokemonDatabase import findAllPokemon
from pokemonCard import Pokemon
from typeManager import TypesManager
import random
from enum import Enum, auto
from dataclasses import dataclass


class Deck:
    def __init__(self):
        self.deckLogs = Logger()
        try:
            pokemonDeck = findAllPokemon()
            self.deck = random.sample(pokemonDeck, 10)
            self.size = len(self.deck)
        except Exception as e:
            self.deckLogs.logger.error(e)
            self.size = None
            self.deck = [None]
        self.deck1 = [None]
        self.deck1Size = None
        self.deck2 = [None]
        self.deck2Size = None

    def splitDeck(self):
        numDecks = 2
        halfDeck = int((self.size / numDecks) // 1)
        self.deck1 = random.sample(self.deck, halfDeck)
        self.deck1Size = len(self.deck1)
        self.deck2 = [card for card in self.deck if card not in self.deck1]
        # if len(self.deck1) != len(self.deck2):
        #     self.deck2.pop(random.randrange(halfDeck + 1))
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


class Player(Enum):
    PLAYER1 = auto()
    PLAYER2 = auto()

    def opponent(self):
        if self == Player.PLAYER1:
            return Player.PLAYER2
        else:
            return Player.PLAYER1


@dataclass(frozen=True)
class AttackerDefenderCardState:
    attacker: int
    defender: int


class Game:
    def __init__(self, attackerPlayer: Player):
        self.gameLogs = Logger()
        self.currentAttacker = attackerPlayer
        self.currentStage = 0

    def getHiddenState(self):
        hide = 0
        show = 1
        if self.currentStage == 0:
            return AttackerDefenderCardState(hide, hide)
        if self.currentStage == 1:
            return AttackerDefenderCardState(show, hide)
        if self.currentStage == 2:
            return AttackerDefenderCardState(show, show)

    def selectAttack(self):
        self.currentStage = 1
        return self.currentAttacker

    def doAttack(self, attackTypeSelected: str, attackerPokemon: Pokemon, defenderPokemon: Pokemon) -> int:
        self.currentStage = 2
        attackMulti = TypesManager().getAttackMultiplier(attackTypeSelected, defenderPokemon)
        fight = int(defenderPokemon.defence) - int(attackerPokemon.attack) * attackMulti
        self.currentAttacker = self.currentAttacker.opponent()
        attackerWin = 2
        draw = 1
        defenderWin = 0
        if fight < 0:
            return attackerWin
        elif fight == 0:
            return draw
        elif fight > 0:
            return defenderWin
