async function openFile(file) {
    console.log(file);
    var response = await callEndpoint("GET", "/main/open?file=" + folder + "\\" + file);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR);
    }
}