
function chooseItem(id) {
    var item = document.getElementById(id);
    if (doesRenamingExists()) {
        if (isRenaming(item)) {
            return;
        } else {
            rename();
        }
    }

    for (let i = 0; i < chosenItems.length; i++) {
        if (chosenItems[i] == id) return;
    }
    item.classList.add("chosenItem");
    chosenItems.push(id);
}

function unChooseItems(element) {

    var floatingFileMenu = document.getElementById("fileMenuTable");
    floatingFileMenu.classList.remove("floatingMenuShow");

    if (window.event.ctrlKey) return;
    
    for (let i = 0; i < chosenItems.length; i++) {
        var item = document.getElementById(chosenItems[i]);

        if (item == element || item == null) continue

        item.classList.remove("chosenItem");
        chosenItems.splice(i, 1);
        i--;
    }
}

function doesRenamingExists() {
    if (document.getElementById("renameInput") != null) {
        return true;
    }
    return false;
}

function isRenaming(item) {
    if (document.getElementById("renameInput").parentNode == item) {
        return true;
    }
    return false;
}

document.addEventListener("click", function (e) {
    unChooseItems(e.target);
});

// cancel browser menu
window.oncontextmenu = function (e)
{
    var elem = e.target;
    if (!elem.classList.contains("file") && 
        !elem.classList.contains("folder") ||
        elem.innerHTML == "..") 
        return;

    chooseItem(e.target.id);
    if (!window.event.ctrlKey) unChooseItems(e.target);
    itemForFloatMenu = e.target;

    var r = document.querySelector(":root");
    r.style.setProperty("--floatingMenuPositionX", e.clientX + "px");
    r.style.setProperty("--floatingMenuPositionY", (e.clientY + 15) + "px");

    var floatingFileMenu = document.getElementById("fileMenuTable");
    floatingFileMenu.classList.add("floatingMenuShow");

    return false;
}