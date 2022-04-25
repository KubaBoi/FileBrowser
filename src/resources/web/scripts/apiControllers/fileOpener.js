async function openFile(e, file) {
    var parent = findParent(e);
    var path = getPath(parent.id);

    var response = await callEndpoint("GET", `/main/open?file=${path}\\${file}`);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR);
    }
}

function getTreePath(e) {
    var parent = e.parentNode;
    var path = "";
    
    while (!parent.id.startsWith("treeTable")) {
        if (parent.nodeName != "UL") {
            childSpan = parent.childNodes[0];
            path = "\\" + childSpan.getAttribute("value") + path;
        }
        parent = parent.parentNode;
    }

    return "C:" + path;
}