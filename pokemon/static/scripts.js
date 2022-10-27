function unghostButton() {
        document.getElementById("selectPokemon").disabled = false;
    }


fetch('/testing')
.then(data => data.text())
.then(data => {
    if (data == "1"){
        document.getElementById("cardBack").style.visibility = "hidden";
    }
    else {
        document.getElementById("cardBack").style.visibility = "visible";
    }
});

