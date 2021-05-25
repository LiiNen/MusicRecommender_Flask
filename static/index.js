function selectVisible() {
    var selector = document.getElementById('musicSelector');
    if(selector.style.visibility == 'hidden') {
        selector.style.visibility = 'visible';
        selector.style.display = 'block';
    }
    else {
        selector.style.visibility = 'hidden';
        selector.style.display = 'none';
    }
}

searchInputListener();
function searchInputListener() {
    var searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('keyup', function(event) {
        event.preventDefault();
        if (searchInput.value != "") {
            searchParser(searchInput.value);
        }
        else {
            var musicSelector = document.getElementById('musicSelector');
            while(musicSelector.hasChildNodes()) {
                musicSelector.removeChild(musicSelector.firstChild);
            }
            for(var i = 0; i < music_list_length; i++) {
                var temp_option = document.createElement('option')
                temp_option.innerHTML = music_list[i].replace('\"', '');
                musicSelector.appendChild(temp_option)
            }
        }
    })
}

function searchParser(searchValue) {
    var musicSelector = document.getElementById('musicSelector');
    musicSelector.style.visibility = 'visible';
    musicSelector.style.display = 'block';
    while(musicSelector.hasChildNodes()) {
        musicSelector.removeChild(musicSelector.firstChild);
    }
    var searchValue_length = searchValue.length;
    for(var i = 0; music_list[i]; i++) {
        if (music_list[i].includes(searchValue)) {
            var temp_option = document.createElement('option')
            temp_option.innerHTML = music_list[i].replace('\"', '');
            musicSelector.appendChild(temp_option)
            if (musicSelector.childElementCount < 10) musicSelector.size = musicSelector.childElementCount
        }
    }
}

function searchBtn() {
    var searchInput = document.getElementById('searchInput');
    var url = '/select_music';
    var data = JSON.stringify({'music_name': searchInput.value});
    var resultBox = document.getElementById('resultBox');
    while(resultBox.hasChildNodes()) {
        resultBox.removeChild(resultBox.firstChild);
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url);
    xhr.onreadystatechange = function() {
        if (xhr.readyState>3 && xhr.status==200){
            var responseText = xhr.responseText;
            console.log(responseText);
            if(responseText == 'not exist') {
                temp = document.createElement('div');
                temp.innerHTML = 'not in database';
                resultBox.appendChild(temp);
            }
            else {
                responseJSON = JSON.parse(responseText);
                Object.keys(responseJSON).forEach(function(key){
                    Object.keys(responseJSON[key]).forEach(function(index){
                        temp = document.createElement('div');
                        temp.innerHTML = key + '<br>' + responseJSON[key][index] + '<br><br>';
                        resultBox.appendChild(temp);
                    })
                })
            }
        }
    };
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(data);
}