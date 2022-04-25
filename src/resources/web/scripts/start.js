var folder = "";
var chosenItems = [];
var copiedPaths = [];

var startArray = [
    "folder",
    "tree",
    "fileMenu"
];

var renameDialogParent = null;
var renameDialogTd = null;
var fileNameOriginal = "";

var itemForFloatMenu = null;

var resizeDefX = null;

async function start() {
    var response = await callEndpoint("GET", "/main/init");
    if (response.ERROR == null) {
        folder = response.PATH;
        buildFolder();
        buildTree();
        createFavorites();
    }
    else {
        showAlert("ERROR", response.ERROR);
    }
}

loadPage(startArray, function() {start();});