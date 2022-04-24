function move(path) {
    folder = path;
    buildFolder();
}

function moveIn(folderName) {
    folder += "\\" + folderName;
    buildFolder();
}

function moveUp() {
    folder = getFolder(folder);
    buildFolder();
}

function moveDirectFromTree(spanId) {
    var path = getTreePath(spanId);
    move(path);
}

function getFolder(fldr) {
    folderSplit = fldr.split("\\");
    fldr = "";
    for (let i = 0; i < folderSplit.length-1; i++) {
        fldr += folderSplit[i];
        if (i < folderSplit.length-2) {
            fldr += "\\";
        }
    }
    return fldr;
}