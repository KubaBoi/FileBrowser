
function chooseItem(id) {
    var item = document.getElementById(id);
    for (let i = 0; i < chosenItems.length; i++) {
        if (chosenItems[i] == id) return;
    }
    item.classList.add("chosenItem");
    chosenItems.push(id);
}

function unChooseItems(element) {
    if (window.event.ctrlKey) return;
    
    for (let i = 0; i < chosenItems.length; i++) {
        var item = document.getElementById(chosenItems[i]);

        if (item == element || item == null) continue

        item.classList.remove("chosenItem");
        chosenItems.splice(i, 1);
        i--;
    }
}

document.addEventListener("click", function (e) {
    unChooseItems(e.target);
});
