
var checkedWindow = null;
var oldComment = null;

function startChecking(window) {
    checkedWindow = window;
    let spn = getUploadSpan(window);
    spn.style.visibility = "visible";

    setTimeout(checkStatus, 1000);
}

function stopChecking(window) {
    let spn = getUploadSpan(window);
    spn.style.visibility = "hidden";
    oldComment = null;
}

async function checkStatus() {
    if (oldComment == null) oldComment = "old";
    let response = await callEndpoint("GET", `/file/uploadStatus?windowId=${checkedWindow.id}&oldComment=${oldComment}`);
    if (response.ERROR == null) {
        if (response.STATUS != "Upload done") {
            if (response.STATUS != oldComment) {
                buildFolder(checkedWindow.id);
            }
            let lbl = getUploadLabel(checkedWindow);
            lbl.innerHTML = `${response.STATUS} ${response.PERCENT}% Total: <label class="transfered">${response.TRANSFERED}</label> / ${response.SIZE} - ${response.SPEED}/s`;

            oldComment = response.STATUS;
            setTimeout(checkStatus, 1000);
        }
        else {
            showOkAlert("Upload done :)", `Upload of ${response.SIZE} has been succesfully done`);
            stopChecking(checkedWindow);
        }
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
        setTimeout(checkStatus, 1000);
    }
}

function getUploadSpan(window) {
    return window.querySelector("#uploadSpan");
}

function getUploadLabel(window) {
    return window.querySelector("#uploadSpanLabel");
}