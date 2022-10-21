from flask import Flask, render_template, request
import downloadDB
import pokemonDatabase
import logs
import gamePageBackEnd

app = Flask(__name__)


# Creates route (url)
@app.route("/")
def main():
    logs.clearLogs()
    
    if pokemonDatabase.Database().checkIfPopulated():
        return indexPage(None)
    else:
        return indexPage(True)


def indexPage(downloadSuccess):
    # Get list of pokemon from database.
    pokemonList = pokemonDatabase.findAllNames()
 
    return render_template("index.html", pokemonList=pokemonList, downloadSuccess=downloadSuccess)

@app.route("/pokemonDownload")
def pokemonDownload():
    return render_template("pokemonDownload.html")

@app.route("/pokemonDownloadDoDownload")
def downloadPokemonData():
    # Returns true/false if the file has downloaded correctly.
    downloadSuccess = downloadDB.downloadPokemonData()
    if downloadSuccess:
        return "1"
    else:
        return "0"


@app.route("/pokemonCard")
def produceCard():
    args = request.args
    pokemonName = args["pokemonList"]

    pokemonData = pokemonDatabase.findPokemonFromName(pokemonName)

    pokemonName = pokemonData["Name"]
    pokemonArtwork = pokemonData["Artwork"]
    pokemonAttack = pokemonData["Attack"]
    pokemonDefence = pokemonData["Defence"]
    pokemonType1 = pokemonData["Type1"]
    pokemonType2 = pokemonData["Type2"]

    return render_template("pokemonCard.html", 
    pokemonCardName=pokemonName, 
    pokemonArtwork=pokemonArtwork, 
    pokemonAttack=pokemonAttack, 
    pokemonDefence=pokemonDefence, 
    pokemonType1=pokemonType1, 
    pokemonType2=pokemonType2)

@app.route("/pokemonGame")
def pageSetup():
    pokemonDeck = gamePageBackEnd.Deck()
    pokemonDeck.shuffleFullDeck()
    pokemonDeck.splitDeck()
    pokemonDeck.shuffleDeck1()
    pokemonDeck.shuffleDeck2()
    topDeck1 = pokemonDeck.getTopCardDeck1()
    #pokemonArtwork1 = topDeck1.artwork
    pokemonAttack1 = topDeck1.attack
    pokemonDefence1 = topDeck1.defence
    pokemonType1Deck1 = topDeck1.type1
    pokemonType2Deck1 = topDeck1.type2

    topDeck2 = pokemonDeck.getTopCardDeck2()
    
    
    return render_template("pokemonGame.html", 
    pokemonAttack1 = pokemonAttack1, 
    pokemonDefence1 = pokemonDefence1,
    pokemonType1Deck1 = pokemonType1Deck1,
    pokemonType2Deck1 = pokemonType2Deck1)

if __name__ == '__main__':
    app.run()
