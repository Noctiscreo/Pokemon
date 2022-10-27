from flask import Flask, render_template, request
import downloadDB
import pokemonDatabase
import logs
import gamePageBackEnd

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
    if databaseEmpty == False:
        # We need top card of each deck (pokemon class)
        artwork = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"
        name = "Pikachu"
        attack = "33"
        defence = "72"
        type1 = "electric"
        type2 = "water"
        #pokemon1 = imported from deck 1
        #pokemon2 = imported from deck 2
        return render_template("pokemonGame.html", databaseCheck = databaseEmpty, 
        artwork = artwork, name = name, attack = attack, defence = defence, type1 = type1, type2 = type2)
    else:
        return render_template("pokemonGame.html", databaseCheck = databaseEmpty)

# @app.route("/cycleCards1")
# def cycleCards1():
#     databaseEmpty = pokemonDatabase.Database().checkIfEmpty()
#     app.pokemonDeck.cycleDeck1()
#     topDeck1 = app.pokemonDeck.getTopCardDeck1()
#     return render_template("singleCard.html", databaseCheck = databaseEmpty, pokemon = topDeck1)

# @app.route("/cycleCards2")
# def cycleCards2():
#     databaseEmpty = pokemonDatabase.Database().checkIfEmpty()
#     app.pokemonDeck.cycleDeck2()
#     topDeck2 = app.pokemonDeck.getTopCardDeck2()
#     return render_template("singleCard.html", databaseCheck = databaseEmpty, pokemon = topDeck2)

@app.route("/noCards1")
def noCards1():
    # If the player 1 deck is empty, return '1' as a string.
    return "0"

@app.route("/noCards2")
def noCards2():
    # If the player 2 deck is empty, return '1' as a string.
    return "0"

@app.route("/displayNumberofCards1")
def displayNumberofCards1():
    # Requires an input of number of cards in deck one, in a string.
    cardsDeck1 = "Cards Remaining: " + "10"
    return cardsDeck1

@app.route("/displayNumberofCards2")
def displayNumberofCards2():
    # Requires an input of number of cards in deck two, in a string.
    cardsDeck2 = "Cards Remaining: " + "9"
    return cardsDeck2

@app.route("/hiddenStatusCard1")
def hiddenStatusCard1():
    # Check for hidden status. Return card 1 status
    hide = "0"
    return hide
@app.route("/hiddenStatusCard2")
def hiddenStatusCard2():
    # Check for hidden status. Return card 2 status
    hide = "0"
    return hide

@app.route("/attackerAndTypes/<playerAttacking>")
def attackerAndTypes(playerAttacking):
    attackList = ["fire", "water"] # backEndFunction() which takes PLAYER1/PLAYER2 as an input and returns a list of types
    return render_template("attackerFragment.html", attackList = attackList)

@app.route("/attacker")
def attacker():
    # Check for attacker returns PLAYER1 or PLAYER2
    attacker = "PLAYER1"
    return attacker


if __name__ == '__main__':
    logs.clearLogs()
    app.run()
