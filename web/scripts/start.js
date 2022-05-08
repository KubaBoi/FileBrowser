var folders = [];
var chosenItems = [];
var copiedPaths = [];
var debug = false;

var alertTime = 3000;

var remoteUrl = "http://frogie.cz:7999";

var startArray = [
    "menu",
    "fileMenu"
];

var renameDialogParent = null;
var renameDialogTd = null;
var fileNameOriginal = "";

var itemForFloatMenu = null;

var resizeDefX = null;
var parentTree = null;

async function start() {
    var response = await callEndpoint("GET", "/main/init");
    if (response.ERROR == null) {
        foldersCookies = getCookie("openFolders");
        //foldersCookies = "";
        if (foldersCookies == "") {
            openFolder(response.PATH, response.ROOT);
        }
        else {
            foldersCookiesArray = foldersCookies.split(",");
            for (var i = 0; i < foldersCookiesArray.length; i++) {
                foldRoot = foldersCookiesArray[i].split("|");
                openFolder(foldRoot[0], foldRoot[1], foldRoot[2]);
            }
        }

        var gridType = getCookie("gridType");
        if (gridType == "") setGridStyle("nGrid");
        else setGridStyle(gridType);
    }
    else {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
}

loadPage(startArray, function() {start();});