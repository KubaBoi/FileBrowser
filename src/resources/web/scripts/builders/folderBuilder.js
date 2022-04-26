
async function buildFolder(divId) {
    var parentDiv = document.getElementById(divId);
    var folderTable = parentDiv.querySelector("#folderTable");

    var folder = getPath(divId);
    parentDiv.querySelector("#folderPathLabel").innerHTML = folder;

    clearTable(folderTable);
    chosenItems = [];

    var response = await callEndpoint("GET", "/main/ls?folder=" + folder);
    if (response.ERROR == null) {
        var folderItems = response.FOLDER;
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
                {"text": "<img src='images/" + item.IMAGE + "'>", "attributes": [
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
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
}