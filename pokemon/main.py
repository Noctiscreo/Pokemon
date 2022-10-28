from flask import Flask, render_template, request
import downloadDB
import pokemonDatabase
import logs
import json
from gamePageBackEnd import Deck, Game, Player

app = Flask(__name__)


# Creates route (url)

@app.route("/")
def menu():
    return render_template("pokemonMenu.html")


@app.route("/pokedex")
def main():
    if pokemonDatabase.Database().checkIfEmpty():
        return indexPage(None)
    else:
        return indexPage(True)


def indexPage(downloadSuccess):
    # Get list of pokemon from database.
    pokemonList = pokemonDatabase.findAllNames()

    return render_template("pokedex.html", pokemonList=pokemonList, downloadSuccess=downloadSuccess)


@app.route("/pokemonDownload")
def pokemonDownload():
    return render_template("pokemonDownload.html")


@app.route("/pokemonDownloadDoDownload")
def downloadPokemonData():
    # Returns true/false if the file has downloaded correctly.
    download = downloadDB.DownloadData()
    download.download()
    downloadSuccess = download.complete
    if downloadSuccess:
        return "1"
    else:
        return "0"


@app.route("/pokemonCard")
def produceCard():
    args = request.args
    pokemonName = args["pokemonList"]

    pokemonData = pokemonDatabase.findPokemonFromName(pokemonName)

    pokemonName = pokemonData.name
    pokemonArtwork = pokemonData.artwork
    pokemonAttack = pokemonData.attack
    pokemonDefence = pokemonData.defence
    pokemonType1 = pokemonData.type1
    pokemonType2 = pokemonData.type2

    return render_template("pokemonCard.html",
                           pokemonCardName=pokemonName,
                           pokemonArtwork=pokemonArtwork,
                           pokemonAttack=pokemonAttack,
                           pokemonDefence=pokemonDefence,
                           pokemonType1=pokemonType1,
                           pokemonType2=pokemonType2)


@app.route("/pokemonGame")
def pageSetup():
    databaseEmpty = pokemonDatabase.Database().checkIfEmpty()
    if not databaseEmpty:
        app.GAME = Game(Deck([], None))
        attackerDefenderCards = app.GAME.selectAttackStage()
        attackerCard = attackerDefenderCards[0]
        defenderCard = attackerDefenderCards[1]
        if app.GAME.currentAttacker == Player.PLAYER1:
            player1Card = attackerCard
            player2Card = defenderCard
        elif app.GAME.currentAttacker == Player.PLAYER2:
            player1Card = defenderCard
            player2Card = attackerCard
        return render_template("pokemonGame.html", databaseCheck=databaseEmpty,
                               player1Card=player1Card, player2Card=player2Card)
    else:
        return render_template("pokemonGame.html", databaseCheck=databaseEmpty)

@app.route("/newRound")
def newRound():
    attackerDefenderCards = app.GAME.selectAttackStage()
    attackerCard = attackerDefenderCards[0]
    defenderCard = attackerDefenderCards[1]
    if app.GAME.currentAttacker == Player.PLAYER1:
        player1Card = attackerCard
        player2Card = defenderCard
    elif app.GAME.currentAttacker == Player.PLAYER2:
        player1Card = defenderCard
        player2Card = attackerCard
    x = json.dumps([player1Card.tojson(), player2Card.tojson()])
    return x

@app.route("/noCards1")
def noCards1():
    if app.GAME.currentAttacker == Player.PLAYER1 and app.GAME.currentAttackerDeck.empty():
        return "1"
    elif app.GAME.currentDefender == Player.PLAYER1 and app.GAME.currentDefenderDeck.empty():
        return "1"
    else:
        return "0"


@app.route("/noCards2")
def noCards2():
    if app.GAME.currentAttacker == Player.PLAYER2 and app.GAME.currentAttackerDeck.empty():
        return "1"
    elif app.GAME.currentDefender == Player.PLAYER2 and app.GAME.currentDefenderDeck.empty():
        return "1"
    else:
        return "0"


@app.route("/displayNumberofCards1")
def displayNumberofCards1():
    if app.GAME.currentAttacker == Player.PLAYER1:
        return "Cards remaining: " + str(len(app.GAME.currentAttackerDeck.deck))
    elif app.GAME.currentDefender == Player.PLAYER1:
        return "Cards remaining: " + str(len(app.GAME.currentDefenderDeck.deck))


@app.route("/displayNumberofCards2")
def displayNumberofCards2():
    if app.GAME.currentAttacker == Player.PLAYER2:
        return "Cards remaining: " + str(len(app.GAME.currentAttackerDeck.deck))
    elif app.GAME.currentDefender == Player.PLAYER2:
        return "Cards remaining: " + str(len(app.GAME.currentDefenderDeck.deck))


@app.route("/hiddenStatusCard1")
def hiddenStatusCard1():
    cardStatus = app.GAME.getGameState()
    if app.GAME.currentAttacker == Player.PLAYER1:
        return str(cardStatus[0])
    elif app.GAME.currentDefender == Player.PLAYER1:
        return str(cardStatus[1])


@app.route("/hiddenStatusCard2")
def hiddenStatusCard2():
    cardStatus = app.GAME.getGameState()
    if app.GAME.currentAttacker == Player.PLAYER2:
        return str(cardStatus[0])
    elif app.GAME.currentDefender == Player.PLAYER2:
        return str(cardStatus[1])


@app.route("/attackerAndTypes/<playerAttacking>")
def attackerAndTypes(playerAttacking):
    attackList = []
    attackList.append(app.GAME.currentAttackerDeck.getTopCard().type1)
    attackerType2 = app.GAME.currentAttackerDeck.getTopCard().type2
    if attackerType2 is not None:
        attackList.append(attackerType2)

    return render_template("attackerFragment.html", attackList=attackList)


@app.route("/attacker")
def attacker():
    # Check for attacker returns PLAYER1 or PLAYER2
    attackerPlayer = app.GAME.currentAttacker.name
    return attackerPlayer


@app.route("/sendDamage")
def sendDamage():
    attackerType = request.args["attackList"]
    winState = app.GAME.doAttackStage(attackerType)
    attackerPlayer = app.GAME.currentAttacker.name
    return json.dumps([attackerPlayer, winState])

if __name__ == '__main__':
    logs.clearLogs()
    app.run()
