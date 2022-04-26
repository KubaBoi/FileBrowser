
function dragStart(e) {
    if (e.target.nodeName == "DIV") {
        parentTree = findParent(e.target);
        parentTree = findByParent("class", "treeDiv", parentTree);

        resizeDefX = e.clientX - parseInt(getComputedStyle(parentTree).getPropertyValue("width").replace("px", ""));
        return;
    }

    nameCell = e.path[0].cells[1];
    chooseItem(nameCell.id);

    copiedPaths = [];
    for (let i = 0; i < chosenItems.length; i++) {
        var item = document.getElementById(chosenItems[i]);
        
        var parent = findParent(item);
        var path = getPath(parent.getAttribute("id"));
        copiedPaths.push(path + "\\" + item.innerHTML);
    }
    e.dataTransfer.setData("text/plain", copiedPaths);
}


function dragEnter(e) {
    if (resizeDefX != null) {
        parentTree.style.width = (e.clientX - resizeDefX) + "px";
        return;
    }

    levitation = 0;
    e.preventDefault();
    if (e.target.classList.contains("folder"))
        e.target.classList.add("dragOver");
}

var levitation = 0;
function dragOver(e) {
    if (resizeDefX != null) {
        parentTree.style.width = (e.clientX - resizeDefX) + "px";
        return;
    }

    e.preventDefault();
    if (e.target.classList.contains("folder")) {
        levitation++;
        e.target.classList.add("dragOver");

        if (levitation >= 100) {
            levitation = 0;
            if (e.target.innerHTML != "..") {
                moveIn(e.target.innerHTML);
            }
            else {
                moveUp();
            }
        }
    } else {
        levitation = 0;
    }
}

function dragLeave(e) {
    if (resizeDefX != null) {
        parentTree.style.width = (e.clientX - resizeDefX) + "px";
        return;
    }

    levitation = 0;
    e.target.classList.remove("dragOver");
}

async function drop(e) {
    if (resizeDefX != null) {
        resizeDefX = null;
        return;
    }

    levitation = 0;
    var pastePath;

    copiedPaths = e.dataTransfer.getData("text/plain").split(",");
    var parent = findParent(e.target);
    var path = getPath(parent.getAttribute("id"));

    unChooseItems(null, true);

    e.target.classList.remove("dragOver");
    if (e.target.classList.contains("folder")) {
        pastePath = path + "\\" + e.target.innerHTML;
    }
    else {
        pastePath = path;
    }

    if (pastePath == getFolder(copiedPaths[0])) {
        return;
    }

    var endpoint = "move";

    if (!window.event.ctrlKey) {
        endpoint = "copy";
    }

    var response = await callEndpoint("POST", "/file/" + endpoint, prepareCopyRequest(pastePath));
    if (response.ERROR != null) {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
    else {
        buildFolder(parent.id);
    }
}

function prepareCopyRequest(pastePath) {
    return {
        "FOLDER": pastePath,
        "ITEMS": copiedPaths
    }
}

document.addEventListener("dragstart", dragStart);

document.addEventListener("dragover", dragOver);
document.addEventListener("dragleave", dragLeave);
document.addEventListener("dragenter", dragEnter);
document.addEventListener("drop", drop);
