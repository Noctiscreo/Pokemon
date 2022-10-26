from gamePageBackEnd import Deck, Game, Player
import random

#
# gameDeck = Deck()
# gameDeck.splitDeck()
# deck1 = gameDeck.deck1
# deck2 = gameDeck.deck2
#
# test = random.sample([Player.PLAYER1, Player.PLAYER2], 1)
# game1 = Game(Player.PLAYER1)
# print(game1.getGameState())
#
# if game1.selectAttackStage() == Player.PLAYER1:
#     attackerPokemon = gameDeck.getTopCardDeck1()
#     print(f"Player 1 Pokemon {attackerPokemon.name}")
#     defenderPokemon = gameDeck.getTopCardDeck2()
# elif game1.selectAttackStage() == Player.PLAYER2:
#     attackerPokemon = gameDeck.getTopCardDeck2()
#     print(f"Player 2 Pokemon {attackerPokemon.name}")
#     defenderPokemon = gameDeck.getTopCardDeck1()
# if game1.getGameState().attacker == 1 and game1.getGameState().defender == 0:
#     print(f"{game1.currentAttacker}: {attackerPokemon.name} and ({game1.currentAttacker.opponent()}: {defenderPokemon.name})")
#
#
# userSelectedAttackType = attackerPokemon.type1
# winState = game1.doAttackStage(userSelectedAttackType, attackerPokemon, defenderPokemon)
# if winState == 2:
#     print(f"{game1.currentAttacker} WIN!")
#     gameDeck.deck2Lose()
#     gameDeck.cycleDeck1()
# elif winState == 1:
#     print("DRAW")
# elif winState == 0:
#     print(f"{game1.currentAttacker} WIN!")
#     gameDeck.deck1Lose()
#     gameDeck.cycleDeck2()
#
# print(game1.currentAttacker)
#
#

# game made
game1 = Game(Deck([], None))

if game1.currentStage == 0:  # game initiate stage 0
    gameState = game1.getGameState()
    print(f"Attacker: {gameState.attacker} | Defender: {gameState.defender}")

    game1.currentStage = 1 # press start
    gameOver = False
    while not gameOver:
        if game1.currentAttackerDeck.empty():
            loser = game1.currentAttacker
            gameOver = True
        elif game1.currentDefenderDeck.empty():
            loser = game1.currentDefender
            gameOver = True
        else:
            if game1.currentStage == 1:  # game start stage 1
                print(f"Stage 1 ---------- Round {game1.round}")
                gameState = game1.getGameState()
                attackerDefenderCards = game1.selectAttackStage()
                attackerCard = attackerDefenderCards[0]
                defenderCard = attackerDefenderCards[1]
                print(f"Attacker: {gameState.attacker} | Defender: {gameState.defender}")
                if gameState.attacker == 1:
                    print(f"Attacker Pokemon: {attackerCard.name}")
                if gameState.defender == 1:
                    print(f"Defender Pokemon: {defenderCard.name}")
            elif game1.currentStage == 2:  # game attack stage 2
                print(f"Stage 2 ---------- Round {game1.round}")
                gameState = game1.getGameState()
                winState = game1.doAttackStage(game1.currentAttackerDeck.getTopCard().type1)
                print(f"Attacker: {gameState.attacker} | Defender: {gameState.defender}")
                if gameState.attacker == 1:
                    print(f"Attacker Pokemon: {attackerCard.name}")
                if gameState.defender == 1:
                    print(f"Defender Pokemon: {defenderCard.name}")
                if winState == 2:
                    print(f"{game1.currentAttacker} WIN!")
                elif winState == 1:
                    print("DRAW")
                elif winState == 0:
                    print(f"{game1.currentAttacker} WIN!")
                print("-------Deck Sizes-------")
                print(f"Attacker: {len(game1.currentAttackerDeck.deck)} | Defender: {len(game1.currentDefenderDeck.deck)}")
                print("------------------------")

# check who won
if loser == Player.PLAYER1:
    print("---------------------------------------------------------")
    print(f"PLAYER 1 LOST THE GAME")
    print("---------------------------------------------------------")
else:
    print("---------------------------------------------------------")
    print(f"PLAYER 2 LOST THE GAME")
    print("---------------------------------------------------------")
