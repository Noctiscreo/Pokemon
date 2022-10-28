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

function startGame() {
    document.getElementById("startButton").style.display = "none"
    fetch("/attacker")
    .then(data => data.text())
    .then(data => {
        if (data == "PLAYER1"){
            document.getElementById("cardBack1").style.visibility = "hidden"
        }
        else {
            document.getElementById("cardBack2").style.visibility = "hidden"
        }
    attackers(data)
    })
}

function attackers(playerAttacking) {
    fetch("/attackerAndTypes/" + playerAttacking)
    .then(data => data.text())
    .then(data => {
        if (playerAttacking == "PLAYER1"){
            document.getElementById("player1Attack").innerHTML = data  
        }
        else {
            document.getElementById("player2Attack").innerHTML = data
        }
    })
}

function revealCard1() {
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
}
   
function revealCard2() {
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
}

function attackTypeSelected() {
    attackType = document.getElementById("attackSelectField").value
    fetch("/sendDamage?attackList=" + attackType)
    .then(data => data.json())
    .then(data => {
        console.log(data)
    });
}