function selectVisible() {
    selector = document.getElementById('musicSelector');
    if(selector.style.visibility == 'hidden') selector.style.visibility = 'visible';
    else selector.style.visibility = 'hidden';
}

function searchBtn() {
    searchInput = document.getElementById('searchInput');
    var url = '/select_music';
    var data = JSON.stringify({'music_name': searchInput.value});

    var xhr = new XMLHttpRequest();
    xhr.open('POST', url);
    xhr.onreadystatechange = function() {
        if (xhr.readyState>3 && xhr.status==200) console.log(xhr.responseText);
    };
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(data);
}