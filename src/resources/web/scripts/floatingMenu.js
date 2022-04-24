async function openAs() {
    var item = document.getElementById(chosenItems[0]);

    var response = await callEndpoint("GET", "/file/openAs?file=" + folder + "\\" + item.innerHTML);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR);
    }
}

async function remove() {
    var request = {
        "FILES": []
    }

    for (var i = 0; i < chosenItems.length; i++) {
        var item = document.getElementById(chosenItems[i]);
        request.FILES.push(folder + "\\" + item.innerHTML);
    }

    var response = await callEndpoint("POST", "/file/remove", request);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR)
    }
    else {
        buildFolder();
    }
}