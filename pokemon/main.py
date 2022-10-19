from flask import Flask, render_template, request
import downloadDB
import pokemonDatabase

app = Flask(__name__)


# Creates route (url)
@app.route("/")
def main():
    return indexPage(None)


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

    # conn = pokemonDatabase.databaseConnect()
    # pokemonData = pokemonDatabase.findPokemonFromName(conn, args)
    # conn.close()
    pokemonData = {"Name": "", "Artwork": ""}
    pokemonName = pokemonData["Name"]
    pokemonArtwork = pokemonData["Artwork"]
    # pokemonAttack = pokemonData["Attack"]
    # pokemonDefence = pokemonData["Defence"]
    # pokemonType1 = pokemonData["Type1"]
    # pokemonType2 = pokemonData["Type2"]
    # 
    return render_template("pokemonCard.html", pokemonCardName=pokemonName, pokemonArtwork=pokemonArtwork,
                           )


if __name__ == '__main__':
    app.run()
