from flask import Flask, render_template, request
import downloadDB
import pokemonDatabase
import logs
import gamePageBackEnd

app = Flask(__name__)

@app.route("/")
def menu():
    pass

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
        pokemonDeck = gamePageBackEnd.Deck()
        app.pokemonDeck = pokemonDeck
        pokemonDeck.splitDeck()
        pokemonDeck.shuffleDeck1()
        pokemonDeck.shuffleDeck2()
        topDeck1 = app.pokemonDeck.getTopCardDeck1()
        topDeck2 = app.pokemonDeck.getTopCardDeck2()
        return render_template("pokemonGame.html", databaseCheck = databaseEmpty, pokemon1 = topDeck1, pokemon2 = topDeck2)
    else:
        return render_template("pokemonGame.html", databaseCheck = databaseEmpty)

@app.route("/cycleCards1")
def cycleCards1():
    databaseEmpty = pokemonDatabase.Database().checkIfEmpty()
    app.pokemonDeck.cycleDeck1()
    topDeck1 = app.pokemonDeck.getTopCardDeck1()
    return render_template("singleCard.html", databaseCheck = databaseEmpty, pokemon = topDeck1)

@app.route("/cycleCards2")
def cycleCards2():
    databaseEmpty = pokemonDatabase.Database().checkIfEmpty()
    app.pokemonDeck.cycleDeck2()
    topDeck2 = app.pokemonDeck.getTopCardDeck2()
    return render_template("singleCard.html", databaseCheck = databaseEmpty, pokemon = topDeck2)
    
@app.route("/noCards1")
def noCards1():
    # If the player 1 deck is empty, return '1' as a string.
    return "0"

@app.route("/noCards2")
def noCards2():
    # If the player 2 deck is empty, return '1' as a string.
    return "1"

if __name__ == '__main__':
    logs.clearLogs()
    app.run()
