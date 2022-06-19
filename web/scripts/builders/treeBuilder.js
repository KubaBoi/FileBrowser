
async function buildTree(divId) {
    var parentDiv = document.getElementById(divId);
    var treeTable = parentDiv.querySelector("#treeTable");

    clearTable(treeTable);
    chosenItems = [];

    var response = await callEndpoint("GET", `${getUrl(divId)}/main/ls?path=${getRoot(divId)}`);
    if (response.ERROR == null) {
        var treeItems = response.FOLDER;

        createLis(treeTable, treeItems, divId);
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}

async function buildBranch(e, divId) {
    var parent = e.parentNode;

    var childNodes = parent.childNodes;
    if (childNodes.length > 1) {
        for (var i = 0; i < childNodes.length; i++) {
            var node = childNodes[i];
            if (node.nodeName == "SPAN") continue;
            node.remove();
        }
        return;
    }

    var path = getTreePath(e);
    var response = await callEndpoint("GET", `${getUrl(divId)}/main/ls?path=${path}`);
    if (response.ERROR == null) {
        var newUL = createElement("ul", parent);
        var treeItems = response.FOLDER;

        createLis(newUL, treeItems, divId);
    }
}

function createLis(parentUL, treeItems, divId) {
    for (let i = 0; i < treeItems.length; i++) {
        var item = treeItems[i];

        if (item.TYPE == "FILE") continue;

        var id = 0;
        while (document.getElementById("treeRow" + id) != null) id++;

        var newLI = createElement("li", parentUL, "",
            [
                {"name": "id", "value": "treeRow" + id}
            ]
        );

        createElement("span", newLI, stringShorter(item.NAME, 15),
            [
                {"name": "ondblclick", "value": `buildBranch(this, ${divId})`},
                {"name": "onclick", "value": `sglC(function(){moveDirectFromTree("${"treeSpan" + id}");})`},
                {"name": "id", "value": "treeSpan" + id},
                {"name": "value", "value": item.NAME},
                {"name": "title", "value": item.NAME}
            ]
        );
    }
}

async function createFavorites(divId) {
    var parentDiv = document.getElementById(divId);
    var treeTableFavorites = parentDiv.querySelector("#treeTableFavorites");
    clearTable(treeTableFavorites);
    if (getUrl(divId) != "") return;

    createElement("label", treeTableFavorites, "Favorites &#9733;");

    var response = await callEndpoint("GET", "/main/favorites");
    if (response.ERROR == null) {
        var treeItems = response.FAVOURITES;

        for (var i = 0; i < treeItems.length; i++) {
            var item = treeItems[i];

            var id = 0;
            while (document.getElementById("treeRow" + id) != null) id++;

            var newLI = createElement("li", treeTableFavorites, "",
                [
                    {"name": "id", "value": "treeRow" + id}
                ]
            );

            createElement("span", newLI, stringShorter(item.NAME, 15),
                [
                    {"name": "ondblclick", "value": `buildBranch(this)`},
                    {"name": "onclick", "value": `sglC(function(){moveDirectFromTree("${"treeSpan" + id}");})`},
                    {"name": "id", "value": "treeSpan" + id},
                    {"name": "value", "value": item.PATH},
                    {"name": "title", "value": getRoot(divId) + item.PATH}
                ]
            );
        }
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}