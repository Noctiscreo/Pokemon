from flask import Flask, render_template, request
import downloadDB
import pokemonDatabase
import logs

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
    pokemonList = []
    if downloadSuccess:
        pokemonList = pokemonDatabase.findAllNames()
 
    return render_template("index.html", pokemonList=pokemonList, downloadSuccess=downloadSuccess)

@app.route("/downloadPokemon")
def downloadPokemonData():
    # Returns true/false if the file has downloaded correctly.
    downloadSuccess = downloadDB.downloadPokemonData()
    return indexPage(downloadSuccess)


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


if __name__ == '__main__':
    app.run()
