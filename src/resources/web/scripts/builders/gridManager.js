
var gridStyle = 0;
var gridStyles = [
    [ // normal
        ["100%", "100%", '"fold1"'],
        ["50% 50%", "100%", '"fold1 fold2"'],
        ["50% 50%", "50% 50%", '"fold1 fold2" "fold3 fold3"'],
        ["50% 50%", "50% 50%", '"fold1 fold2" "fold3 fold4"'],
        ["33% 33% 33%", "50% 50%", '"fold1 fold1 fold2" "fold3 fold4 fold5"'],
        ["33% 33% 33%", "50% 50%", '"fold1 fold2 fold3" "fold4 fold5 fold6"'],
        ["25% 25% 25% 25%", "50% 50%", '"fold1 fold1 fold2 fold3" "fold4 fold5 fold6 fold7"'],
        ["25% 25% 25% 25%", "50% 50%", '"fold1 fold2 fold3 fold4" "fold5 fold6 fold7 fold8"']
    ],
    [ // top
        ["100%", "100%", '"fold1"'],
        ["100%", "50% 50%", '"fold1" "fold2"'],
        ["50% 50%", "50% 50%", '"fold1 fold1" "fold2 fold3"'],
        ["33% 33% 33%", "50% 50%", '"fold1 fold1 fold1" "fold2 fold3 fold4"'],
        ["25% 25% 25% 25%", "50% 50%", '"fold1 fold1 fold1 fold1" "fold2 fold3 fold4 fold5"'],
        ["25% 25% 25% 25%", "50% 50%", '"fold1 fold1 fold1 fold2" "fold3 fold4 fold5 fold6"'],
        ["25% 25% 25% 25%", "50% 50%", '"fold1 fold1 fold2 fold3" "fold4 fold5 fold6 fold7"'],
        ["25% 25% 25% 25%", "50% 50%", '"fold1 fold2 fold3 fold4" "fold5 fold6 fold7 fold8"']
    ],
    [ // right
        ["100%", "100%", '"fold1"'],
        ["50% 50%", "100%", '"fold1 fold2"'],
        ["50% 50%", "50% 50%", '"fold2 fold1" "fold3 fold1"'],
        ["50% 50%", "33% 33% 33%", '"fold2 fold1" "fold3 fold1" "fold4 fold1"'],
        ["33% 33% 33%", "50% 50%", '"fold1 fold1 fold2" "fold3 fold4 fold5"'],
        ["33% 33% 33%", "50% 50%", '"fold1 fold2 fold3" "fold4 fold5 fold6"'],
        ["25% 25% 25% 25%", "50% 50%", '"fold1 fold1 fold2 fold3" "fold4 fold5 fold6 fold7"'],
        ["25% 25% 25% 25%", "50% 50%", '"fold1 fold2 fold3 fold4" "fold5 fold6 fold7 fold8"']
    ]
]

function setGridStyle(style) {
    gridStyle = style;
    doGrid();
}

function doGrid() {

    switch (folders.length) {
        case 1: 
            changeGrid();
            break;
        case 2:
            changeGrid();
            break;
        case 3:
            changeGrid();
            break;
        case 4:
            changeGrid();
            break;
        case 5:
            changeGrid();
            break;
        case 6:
            changeGrid();
            break;
        case 7:
            changeGrid();
            break;
        case 8:
            changeGrid();
            break;
    }
}

function changeGrid() {
    var openFoldersDiv = document.getElementById("openFoldersDiv");

    openFoldersDiv.style.gridTemplateColumns = gridStyles[gridStyle][folders.length-1][0];
    openFoldersDiv.style.gridTemplateRows = gridStyles[gridStyle][folders.length-1][1];
    openFoldersDiv.style.gridTemplateAreas = gridStyles[gridStyle][folders.length-1][2];
}