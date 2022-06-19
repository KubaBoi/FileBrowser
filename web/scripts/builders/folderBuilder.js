
async function buildFolder(divId) {
    var parentDiv = document.getElementById(divId);
    var folderTable = parentDiv.querySelector("#folderTable");

    var folder = getPath(divId);
    var url = getUrl(divId);
    if (url != "") {
        parentDiv.querySelector("#remoteUrlLabel").innerHTML = url;
        var root = getRoot(divId);
        folder = folder.replace(root.substring(0, root.length-1), "/");
    }

    parentDiv.querySelector("#folderPathLabel").innerHTML = folder;
    folder = getPath(divId);

    clearTable(folderTable);
    chosenItems = [];

    var response = await callEndpoint("GET", `${url}/main/ls?path=${folder}`);
    if (response.ERROR == null) {
        var folderItems = response.FOLDER;
        
        if (folderItems.length == 0) {
            var response2 = await callEndpoint("GET", `${url}/main/exists?path=${folder}`)
            if (response2.ERROR == null) {
                if (!response2.EXISTS) {
                    showWrongAlert("Not found", "Folder was not found", alertTime);
                    folderTable.innerHTML = "Folder was not found";
                    return;
                } else {
                    folderTable.innerHTML = "There are not any files";
                    return;
                }
            } 
        }

        addHeader(folderTable, [
            {"text": "", "attributes":[]},
            {"text": "Name", "attributes":[]},
            {"text": "Size", "attributes":[]}
        ],[]);

        for (let i = 0; i < folderItems.length; i++) {
            var item = folderItems[i];

            var ondblclick = "moveIn(this, '" + item.NAME + "')";

            if (item.TYPE == "FILE") {
                ondblclick = "openFile(this, '" + item.NAME + "')";
            }

            var id = i;
            while (document.getElementById("row" + id) != null) id++;

            addRow(folderTable, [
                {"text": "<img class='iconImg' src='images/" + item.IMAGE + "'>", "attributes": [
                    {"name": "class", "value": "iconCell"}
                ]},
                {"text": item.NAME, "attributes": [
                    {"name": "class", "value": item.TYPE.toLowerCase()},
                    {"name": "id", "value": "row" + id}
                ]},
                {"text": item.SIZE, "attributes": [
                    {"name": "class", "value": "sizeCell"}
                ]}
            ],
            [
                {"name": "ondblclick", "value": ondblclick},
                {"name": "onclick", "value": "chooseItem('row" + id + "')"},
                {"name": "draggable", "value": "true"}
            ]);
        }
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
    setFoldersCookies();
}

function setFoldersCookies() {
    var foldersString = "";
    for (var i = 0; i < folders.length; i++) {
        foldersString += folders[i].PATH + "|" + folders[i].ROOT + "|" + folders[i].URL + "|" + folders[i].SESSION + ",";
    }
    foldersString = foldersString.substring(0, foldersString.length - 1);
    setCookie("openFolders", foldersString, 300);
}