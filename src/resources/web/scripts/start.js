var folder = "";
var chosenItems = [];
var copiedPaths = [];

var startArray = [
    "folder",
    "tree",
    "fileMenu"
]

async function start() {
    var response = await callEndpoint("GET", "/main/init");
    if (response.ERROR == null) {
        folder = response.PATH;
        buildFolder();
    }
    else {
        showAlert("ERROR", response.ERROR);
    }
}

loadPage(startArray, function() {start();});