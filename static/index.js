function selectVisible() {
    selector = document.getElementById('musicSelector');
    if(selector.style.visibility == 'hidden') {
        selector.style.visibility = 'visible';
        selector.style.display = 'block';
    }
    else {
        selector.style.visibility = 'hidden';
        selector.style.display = 'none';
    }
}

function searchBtn() {
    searchInput = document.getElementById('searchInput');
    var url = '/select_music';
    var data = JSON.stringify({'music_name': searchInput.value});
    resultBox = document.getElementById('resultBox');
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