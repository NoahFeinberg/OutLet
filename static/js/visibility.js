
$("#searchButton").click( function () {
    controlHidden();
});

function controlHidden() {
    var checkSearchStatus = document.getElementById('searchBar').value;
    if(checkSearchStatus !== undefined && checkSearchStatus !== "") {
        document.getElementById('table-control').classList.remove("hidden");
        document.getElementById('table-control').classList.remove("hidden");
    } else {
        document.getElementById('table-control').classList.add("hidden");
        document.getElementById('table-control').classList.add("hidden");
    }
}

