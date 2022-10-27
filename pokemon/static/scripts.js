function unghostButton() {
        document.getElementById("selectPokemon").disabled = false;
    }


fetch('/hiddenStatusCard1')
.then(data => data.text())
.then(data => {
    if (data == "1"){
        document.getElementById("cardBack1").style.visibility = "hidden";
    }
    else {
        document.getElementById("cardBack1").style.visibility = "visible";
    }
});

fetch('/hiddenStatusCard2')
.then(data => data.text())
.then(data => {
    if (data == "1"){
        document.getElementById("cardBack2").style.visibility = "hidden";
    }
    else {
        document.getElementById("cardBack2").style.visibility = "visible";
    }
});

