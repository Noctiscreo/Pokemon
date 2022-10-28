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

function nextRound() {
    
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
    fetch("/newRound")
    .then(data => data.json())
    .then(data => {
        console.log(data)
        document.getElementById("cardFront1").innerHTML =
        document.getElementById("cardFront2").innerHTML =
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

function showDefender(player) {
    if (player == "PLAYER1"){
        document.getElementById("cardBack2").style.visibility = "hidden"
    }
    else {
        document.getElementById("cardBack1").style.visibility = "hidden"
    }
}

function outcome(attackResult, player) {
    if (player == "PLAYER1") {
        if (attackResult == 0) {
            document.getElementById("player1Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-danger">Lose</span></h2>'
            document.getElementById("player2Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-success">Win</span></h2>'
        }
        else if (attackResult == 1) {
            document.getElementById("player1Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-warning">Draw</span></h2>'
            document.getElementById("player2Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-warning">Draw</span></h2>'
        }
        else {
            document.getElementById("player1Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-success">Win</span></h2>'
            document.getElementById("player2Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-danger">Lose</span></h2>' 
        }
        numberOfCards1()
        numberOfCards2()
        checkForNoCards1()
        checkForNoCards2()
    }   
    else {
        if (attackResult == 0) {
            document.getElementById("player1Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-success">Win</span></h2>'
            document.getElementById("player2Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-danger">Lose</span></h2>'
        }
        else if (attackResult == 1) {
            document.getElementById("player1Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-warning">Draw</span></h2>'
            document.getElementById("player2Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-warning">Draw</span></h2>'
        }
        else {
            document.getElementById("player1Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-danger">Lose</span></h2>'
            document.getElementById("player2Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-success">Win</span></h2>'
        }
        numberOfCards1()
        numberOfCards2()
        checkForNoCards1()
        checkForNoCards2()
    }
}

function attackTypeSelected() {
    attackType = document.getElementById("attackSelectField").value
    fetch("/sendDamage?attackList=" + attackType)
    .then(data => data.json())
    .then(data => {
        let player = data[0]
        let attackResult = data[1]
        showDefender(player)
        outcome(attackResult, player)
    });
}

function numberOfCards1() {
    fetch('/displayNumberofCards1')
        .then(data => data.text())
        .then(data => {
            document.getElementById("card1Counter").innerHTML = data
        });
}

function numberOfCards2() {
    fetch('/displayNumberofCards2')
        .then(data => data.text())
        .then(data => {
            document.getElementById("card2Counter").innerHTML = data
        });
    }

// Below is from the pokemonGame.html page
fetch('/displayNumberofCards1')
    .then(data => data.text())
    .then(data => {
        document.getElementById("card1Counter").innerHTML = data
    });

fetch('/displayNumberofCards2')
    .then(data => data.text())
    .then(data => {
        document.getElementById("card2Counter").innerHTML = data
    });

function checkForNoCards1() {
    fetch('/noCards1')
        .then(data => data.text())
        .then(data => {
            if (data == "1"){
                document.getElementById("player1").innerHTML = `
                    <h2><span class="badge rounded-pill bg-danger" style="width: 288px">No Cards in Deck</span></h2>
                    `;
                    console.log(document.getElementById("disappear"));
                    document.getElementById("disappear").style.display="none";
                loseFunction1()
            }
            else {
                nextRound()
            }
        });
}

function checkForNoCards2() {
    fetch('/noCards2')
        .then(data => data.text())
        .then(data => {
            if (data == "1"){
                document.getElementById("player2").innerHTML = `
                    <h2><span class="badge rounded-pill bg-danger" style="width: 288px">No Cards in Deck</span></h2>
                    `;
                    console.log(document.getElementById("disappear"));
                    document.getElementById("disappear").style.display="none";
                loseFunction2()

            }
            else {
                nextRound()
            }
        });
}  

function loseFunction1() {
    document.getElementById("player1Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-danger">You lose!</span></h2>'
    document.getElementById("player2Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-success">You win!</span></h2>'
}

function loseFunction2() {
    document.getElementById("player2Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-danger">You lose!</span></h2>'
    document.getElementById("player1Attack").innerHTML = '<h2><span id="p2Label" class="center badge rounded-pill bg-success">You win!</span></h2>'
}
