async function openFolder(path, root, url="") {
    if (folders.length == 8) {
        showWrongAlert("Slow down", "That's too much, man<br>Close something boy", alertTime);
        return;
    }

    var divName = "window";
    if (url != "") {
        divName = "windowRemote";
    }
    var div = await getHtml(divName, "", "windowsDiv", "window");
    if (div == null) {
        showAlert("ERROR", "Error while creating div");
        return;
    } else {
        var id = 0;
        while (document.getElementById(`${divName}Div${id}`) != null) id++;

        var divId = `${divName}Div${id}`;

        div.setAttribute("id", divId);

        var div = await getHtml("folder", "", divId, "windowContent");
        if (div == null) {
            showAlert("ERROR", "Error while creating div");
            return;
        }

        folders.push(
            {
                "PATH": path,
                "DIV_ID": divId,
                "ROOT": root,
                "URL": url
            }
        );
        
        renameGridAreas();
        doGrid();
    
        buildFolder(divId);
        buildTree(divId);
        createFavorites(divId);
    }
}

function closeTab(e) {
    var parent = findParent(e);
    
    for (var i = 0; i < folders.length; i++) {
        if (folders[i].DIV_ID == parent.id) {
            folders.splice(i, 1);
            break;
        }
    }

    parent.remove();
    renameGridAreas();
    doGrid();
}

function renameGridAreas() {
    for (var i = 0; i < folders.length; i++) {
        var fold = document.getElementById(folders[i].DIV_ID);
        fold.style.gridArea = "win" + (i + 1);
    }
}

function getPath(divId) {
    for (var i = 0; i < folders.length; i++) {
        if (folders[i].DIV_ID == divId) return folders[i].PATH;
    }
    return null;
}

function getRoot(divId) {
    for (var i = 0; i < folders.length; i++) {
        if (folders[i].DIV_ID == divId) return folders[i].ROOT;
    }
    return null;
}

function getUrl(divId) {
    for (var i = 0; i < folders.length; i++) {
        if (folders[i].DIV_ID == divId) return folders[i].URL;
    }
    return null;
}

function changePath(divId, newPath) {
    for (var i = 0; i < folders.length; i++) {
        if (folders[i].DIV_ID == divId) {
            folders[i].PATH = newPath;
            return true;
        }
    }
    return false;
}

async function openNewTab() {
    var response = await callEndpoint("GET", "/main/init");
    if (response.ERROR == null) {
        openFolder(response.PATH, response.ROOT);
    }
    else {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
}

async function openNewRemoteTab() {
    var response = await callEndpoint("GET", `${remoteUrl}/main/init`);
    if (response.ERROR == null) {
        openFolder(response.PATH, response.ROOT, remoteUrl);
    }
    else {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
}

function findParent(self) {
    var parent = self.parentNode;

    while (!parent.id.startsWith("windowDiv") && !parent.id.startsWith("windowRemoteDiv")) {
        parent = parent.parentNode;
    }

    return parent;
}