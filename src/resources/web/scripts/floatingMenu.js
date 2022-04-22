async function openAs() {
    var item = document.getElementById(chosenItems[0]);

    var response = await callEndpoint("GET", "/file/openAs?file=" + folder + "\\" + item.innerHTML);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR);
    }
}