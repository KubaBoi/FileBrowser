
async function buildFolder() {
    var folderTable = document.getElementById("folderTable");
    document.getElementById("folderPathLabel").innerHTML = folder;

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

        addRow(folderTable, [
            {"text": "<img src='images/up.png'>"},
            {"text": "..", "attributes": [
                {"name": "class", "value": "folder"},
                {"name": "id", "value": "row-1"}
            ]},
            {"text": "", "attributes": []}
        ],
        [
            {"name": "ondblclick", "value": "moveUp()"}
        ]);

        for (let i = 0; i < folderItems.length; i++) {
            var item = folderItems[i];

            var ondblclick = "moveIn('" + item.NAME + "')";

            if (item.TYPE == "FILE") {
                ondblclick = "openFile('" + item.NAME + "')";
            }

            addRow(folderTable, [
                {"text": "<img src='images/" + item.IMAGE + "'>"},
                {"text": item.NAME, "attributes": [
                    {"name": "class", "value": item.TYPE.toLowerCase()},
                    {"name": "id", "value": "row" + i}
                ]},
                {"text": item.SIZE, "attributes": []}
            ],
            [
                {"name": "ondblclick", "value": ondblclick},
                {"name": "onclick", "value": "chooseItem('row" + i + "')"},
                {"name": "draggable", "value": "true"}
            ]);
        }
    }
    else {
        showAlert("ERROR", response.ERROR);
    }
}