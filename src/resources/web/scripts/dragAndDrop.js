
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
    //if (e.target.classList.contains("folder"))
        //e.target.classList.add("dragOver");
}

var levitation = 0;
function dragOver(e) {
    e.preventDefault();
    if (e.target.classList.contains("folder")) {
        levitation++;
        e.target.classList.add("dragOver");
        label.innerHTML = levitation;
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

function drop(e) {
    levitation = 0;
    var pastePath;

    e.target.classList.remove("dragOver");
    if (e.target.classList.contains("folder")) {
        pastePath = folder + "\\" + e.target.innerHTML;
    }
    else {
        pastePath = folder;
    }
    console.log(pastePath);
    for (let i = 0; i < copiedPaths.length; i++) {
        console.log(copiedPaths[i]);
    }
}

document.addEventListener("dragstart", dragStart);

document.addEventListener("dragover", dragOver);
document.addEventListener("dragleave", dragLeave);
document.addEventListener("dragenter", dragEnter);
document.addEventListener("drop", drop);
