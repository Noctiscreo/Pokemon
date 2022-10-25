from gamePageBackEnd import Deck, Game, Player
import random

gameDeck = Deck()
gameDeck.splitDeck()
deck1 = gameDeck.deck1
deck2 = gameDeck.deck2

test = random.sample([Player.PLAYER1, Player.PLAYER2], 1)
game1 = Game(Player.PLAYER1)
print(game1.getGameState())

if game1.selectAttack() == Player.PLAYER1:
    attackerPokemon = gameDeck.getTopCardDeck1()
    print(f"Player 1 Pokemon {attackerPokemon.name}")
    defenderPokemon = gameDeck.getTopCardDeck2()
elif game1.selectAttack() == Player.PLAYER2:
    attackerPokemon = gameDeck.getTopCardDeck2()
    print(f"Player 2 Pokemon {attackerPokemon.name}")
    defenderPokemon = gameDeck.getTopCardDeck1()
if game1.getGameState().attacker == 1 and game1.getGameState().defender == 0:
    print(f"{game1.currentAttacker}: {attackerPokemon.name} and ({game1.currentAttacker.opponent()}: {defenderPokemon.name})")


userSelectedAttackType = attackerPokemon.type1
winState = game1.doAttack(userSelectedAttackType, attackerPokemon, defenderPokemon)
if winState == 2:
    print(f"{game1.currentAttacker} WIN!")
    gameDeck.deck2Lose()
    gameDeck.cycleDeck1()
elif winState == 1:
    print("DRAW")
elif winState == 0:
    print(f"{game1.currentAttacker} WIN!")
    gameDeck.deck1Lose()
    gameDeck.cycleDeck2()

print(game1.currentAttacker)


