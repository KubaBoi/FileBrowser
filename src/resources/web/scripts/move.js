function move(path) {
    folder = path;
    buildFolder();
}

function moveIn(folderName) {
    folder += "\\" + folderName;
    buildFolder();
}

function moveUp() {
    folderSplit = folder.split("\\");
    folder = "";
    for (let i = 0; i < folderSplit.length-1; i++) {
        folder += folderSplit[i];
        if (i < folderSplit.length-2)
            folder += "\\";
    }
    buildFolder();
}