from logs import Logger
from pokemonDatabase import findAllPokemon
from pokemonCard import Pokemon
from typeManager import TypesManager
import random
from enum import Enum, auto
from dataclasses import dataclass


class Player(Enum):
    PLAYER1 = auto()
    PLAYER2 = auto()

    def opponent(self):
        if self == Player.PLAYER1:
            return Player.PLAYER2
        else:
            return Player.PLAYER1


class Deck:
    def __init__(self, pokemonDeck: list, player: Player):
        self.deckLogs = Logger()
        if len(pokemonDeck) == 0:
            self.deck = random.sample(findAllPokemon(), 10)
        elif len(pokemonDeck) == 5:
            self.deck = pokemonDeck
        self.size = len(self.deck)
        self.player = player

    def splitDeck(self) -> tuple:
        try:
            numDecks = 2
            halfDeck = int((self.size / numDecks) // 1)
            deck1 = Deck(random.sample(self.deck, halfDeck), Player.PLAYER1)
            deck2 = Deck([card for card in self.deck if card not in deck1.deck], Player.PLAYER2)
            self.deckLogs.logger.info("Deck was split and assigned deck 1 to Player 1 and deck 2 to Player 2")
            return deck1, deck2
        except Exception as e:
            self.deckLogs.logger.error(e)

    def shuffleDeck(self):
        random.shuffle(self.deck)
        self.deckLogs.logger.info("Deck was shuffled")

    def getTopCard(self) -> Pokemon:
        self.deckLogs.logger.info("Retrieving top card of deck 1")
        return self.deck[0]

    def cycleDeck(self):
        self.deck.append(self.deck.pop(0))
        self.deckLogs.logger.info("Moving top card of deck 1 to bottom")

    def deckLoseRound(self):
        return self.deck.pop(0)

    def empty(self):
        self.size = len(self.deck)
        if self.size == 0:
            return True
        else:
            return False


@dataclass(frozen=True)
class AttackerDefenderCardState:
    attacker: int
    defender: int


class Game:
    def __init__(self, gameDeck: Deck):
        self.gameLogs = Logger()
        self.gameDeck = gameDeck
        decks = self.gameDeck.splitDeck()
        random.sample(decks, 1)
        self.currentAttackerDeck = decks[0]
        self.currentAttacker = self.currentAttackerDeck.player
        self.currentDefenderDeck = decks[1]
        self.currentDefender = self.currentDefenderDeck.player
        self.tableCards = []
        self.currentStage = 0
        self.round = 1

    def getGameState(self):
        hide = 0
        show = 1
        if self.currentStage == 0:
            return AttackerDefenderCardState(hide, hide)
        if self.currentStage == 1:
            return AttackerDefenderCardState(show, hide)
        if self.currentStage == 2:
            return AttackerDefenderCardState(show, show)

    def selectAttackStage(self):
        self.currentStage = 2
        return self.currentAttackerDeck.getTopCard(), self.currentDefenderDeck.getTopCard()

    def doAttackStage(self, attackType: str) -> int:
        self.currentStage = 1
        self.round += 1
        attackMulti = TypesManager().getAttackMultiplier(attackType, self.currentDefenderDeck.getTopCard())
        fight = int(self.currentDefenderDeck.getTopCard().defence) - int(
            self.currentAttackerDeck.getTopCard().attack) * attackMulti
        attackerWin = 2
        draw = 1
        defenderWin = 0
        if fight < 0:
            self.currentAttackerDeck.deck.append(self.currentDefenderDeck.deckLoseRound())
            self.currentAttackerDeck.cycleDeck()
            return attackerWin
        elif fight == 0:
            self.tableCards.append(self.currentDefenderDeck.getTopCard())
            self.tableCards.append(self.currentAttackerDeck.getTopCard())
            return draw
        elif fight > 0:
            self.currentDefenderDeck.deck.append(self.currentAttackerDeck.deckLoseRound())
            self.currentDefenderDeck.cycleDeck()
            switchDecks = self.currentAttackerDeck
            self.currentAttackerDeck = self.currentDefenderDeck
            self.currentDefenderDeck = switchDecks
            self.currentAttacker = self.currentAttacker.opponent()
            self.currentDefender = self.currentDefender.opponent()
            return defenderWin
