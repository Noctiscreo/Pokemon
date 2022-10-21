from flask import Flask, render_template, request
import downloadDB
import pokemonDatabase
import logs
import gamePageBackEnd

app = Flask(__name__)


# Creates route (url)

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
        pokemonDeck = gamePageBackEnd.Deck()
        pokemonDeck.shuffleFullDeck()
        pokemonDeck.splitDeck()
        pokemonDeck.shuffleDeck1()
        pokemonDeck.shuffleDeck2()
        topDeck1 = pokemonDeck.getTopCardDeck1()
        topDeck2 = pokemonDeck.getTopCardDeck2()

        return render_template("pokemonGame.html", databaseCheck = databaseEmpty,
        pokemonArtwork1 = topDeck1.artwork,
        pokemonName1 = topDeck1.name,
        pokemonAttack1 = topDeck1.attack,
        pokemonDefence1 = topDeck1.defence,
        pokemonType1Deck1 = topDeck1.type1,
        pokemonType2Deck1 = topDeck1.type2,

        pokemonArtwork2 = topDeck2.artwork,
        pokemonName2 = topDeck2.name,
        pokemonAttack2 = topDeck2.attack,
        pokemonDefence2 = topDeck2.defence,
        pokemonType1Deck2 = topDeck2.type1,
        pokemonType2Deck2 = topDeck2.type2)
    else:
        return render_template("pokemonGame.html", databaseCheck = databaseEmpty)

if __name__ == '__main__':
    logs.clearLogs()
    app.run()
