
function updateLists() {
    fetch('/pokeList')
        .then(data => data.text())
        .then(data => {
            element = document.getElementById("pokeList");
            element.innerHTML = data
        });