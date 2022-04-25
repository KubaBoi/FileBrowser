
function dragStart(e) {
    if (e.target.nodeName == "DIV") {
        console.log(e);

        var r = document.querySelector(":root");
        var rs = getComputedStyle(r);

        resizeDefX = e.clientX - parseInt(rs.getPropertyValue("--tree-width").replace("px", ""));
        return;
    }

    nameCell = e.path[0].cells[1];
    chooseItem(nameCell.id);

    copiedPaths = [];
    for (let i = 0; i < chosenItems.length; i++) {
        var item = document.getElementById(chosenItems[i]);

        copiedPaths.push(folder + "\\" + item.innerHTML);
    }
    e.dataTransfer.setData("text/plain", copiedPaths);
}


function dragEnter(e) {
    if (resizeDefX != null) {
        var r = document.querySelector(":root");

        r.style.setProperty("--tree-width", (e.clientX - resizeDefX) + "px");
        return;
    }

    levitation = 0;
    e.preventDefault();
    if (e.target.classList.contains("folder"))
        e.target.classList.add("dragOver");
}

var levitation = 0;
function dragOver(e) {
    if (resizeDefX != null) return;

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
    if (resizeDefX != null) return;

    levitation = 0;
    e.target.classList.remove("dragOver");
}

async function drop(e) {
    if (resizeDefX != null) {
        console.log("END");
        resizeDefX = null;
        return;
    }

    levitation = 0;
    var pastePath;

    copiedPaths = e.dataTransfer.getData("text/plain").split(",");

    e.target.classList.remove("dragOver");
    if (e.target.classList.contains("folder")) {
        pastePath = folder + "\\" + e.target.innerHTML;
    }
    else {
        pastePath = folder;
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
        showAlert("ERROR", response.ERROR);
    }
    else {
        buildFolder();
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
