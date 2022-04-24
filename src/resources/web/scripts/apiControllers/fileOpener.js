async function openFile(file) {
    var response = await callEndpoint("GET", "/main/open?file=" + folder + "\\" + file);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR);
    }
}

function getTreePath(id) {
    var item = document.getElementById(id);
    var parent = item.parentNode;
    var path = "";

    while (parent.id != "treeTable") {
        if (parent.nodeName != "UL") {
            childSpan = parent.childNodes[0];
            path = childSpan.getAttribute("value") + "\\" + path;
        }
        parent = parent.parentNode;
    }

    return "C:\\" + path;
}