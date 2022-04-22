
function dragStart(e) {
    nameCell = e.path[0].cells[1];
    chooseItem(nameCell.id);

    copiedPaths = [];
    for (let i = 0; i < chosenItems.length; i++) {
        var item = document.getElementById(chosenItems[i]);

        copiedPaths.push(folder + "\\" + item.innerHTML);
    }
}


function dragEnter(e) {
    levitation = 0;
    e.preventDefault();
    if (e.target.classList.contains("folder"))
        e.target.classList.add("dragOver");
}

var levitation = 0;
function dragOver(e) {
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
    levitation = 0;
    e.target.classList.remove("dragOver");
}

async function drop(e) {
    levitation = 0;
    var pastePath;

    e.target.classList.remove("dragOver");
    if (e.target.classList.contains("folder")) {
        pastePath = folder + "\\" + e.target.innerHTML;
    }
    else {
        pastePath = folder;
    }

    if (pastePath != getFolder(copiedPaths[0])) {
        var response = await callEndpoint("POST", "/file/copy", prepareCopyRequest(pastePath));
        if (response.ERROR != null) {
            showAlert("ERROR", response.ERROR);
        }
        else {
            buildFolder();
        }
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
