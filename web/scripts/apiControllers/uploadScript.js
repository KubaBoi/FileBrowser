
var sessions = [];

function startChecking(window) {
    let spn = getUploadSpan(window);
    spn.style.visibility = "visible";

    let lbl = getUploadLabel(window);
    lbl.setAttribute("class", "");

    folderObj = getFolderObject(window.id);
    if (folderObj.SESSION == null)
        folderObj.SESSION = window.id;
        
    sessions.push({"ID": folderObj.SESSION, "OLD_COMM": null, "WINDOW": window})
    setFoldersCookies();
    setTimeout(checkStatus, 1000);
}

function stopChecking(session, clear=true) {
    if (clear) {
        let spn = getUploadSpan(session.WINDOW);
        spn.style.visibility = "hidden";
    }
    else {
        let lbl = getUploadLabel(session.WINDOW);
        lbl.setAttribute("class", "killed");
    }
    folderObj = getFolderObject(session.WINDOW.id);
    folderObj.SESSION = null;
    setFoldersCookies();

    index = sessions.indexOf(session);
    sessions.splice(index, 1);
}

async function checkStatus() {
    for (let i = 0; i < sessions.length; i++) {
        session = sessions[i];

        if (session.OLD_COMM == null) session.OLD_COMM = "old";

        let response = await callEndpoint("GET", `/file/uploadStatus?windowId=${session.ID}&oldComment=${session.OLD_COMM}`);
        if (response.ERROR == null) {
            if (response.STATUS == "Killed") {
                showWrongAlert("Killed", "Connection with cloud has been killed :(");
                stopChecking(session, false);
            }
            else if (response.STATUS != "Upload done") {
                if (response.STATUS != session.OLD_COMM) {
                    buildFolder(session.WINDOW.id);
                }
                let lbl = getUploadLabel(session.WINDOW);
                let status = response.STATUS;
                if (status.length > 15) {
                    end = status.split(".");
                    if (end.length > 1) {
                        end = " ." + end[end.length-1];
                    }
                    else end = "";
                    status = status.substring(0, 14) + "..." + end;
                }

                lbl.innerHTML = `${status} ${response.PERCENT}% Total: <label class="transfered">${response.TRANSFERED}</label> / ${response.SIZE} - ${response.SPEED}/s`;

                session.OLD_COMM = response.STATUS;
                setTimeout(checkStatus, 1000);
            }
            else {
                showOkAlert("Upload done :)", `Upload of ${response.SIZE} has been succesfully done`);
                stopChecking(session);
            }
        }
        else {
            stopChecking(session);
        }
    }
}

function getSessionId(window) {
    folderObj = getFolderObject(window.id);
    return folderObj.SESSION;
}

function getUploadSpan(window) {
    return window.querySelector("#uploadSpan");
}

function getUploadLabel(window) {
    return window.querySelector("#uploadSpanLabel");
}