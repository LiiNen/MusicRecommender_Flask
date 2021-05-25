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

searchInputListener();
function searchInputListener() {
    searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('keyup', function(event) {
        event.preventDefault();
        if (searchInput.value != "") {
            searchParser(searchInput.value);
        }
    })
}

function searchParser(searchValue) {
    musicSelector = document.getElementById('musicSelector');
    while(musicSelector.hasChildNodes()) {
        musicSelector.removeChild(musicSelector.firstChild);
    }
    searchValue_length = searchValue.length;
    for(var i = 0; music_list[i]; i++) {
        music_title_length = music_list[i].length;
        substr_bool = false;
        console.log(music_title_length, searchValue_length)
        for(var j = 0; j < music_title_length - searchValue_length + 1; j++) {
            console.log(searchValue[0], music_list[i][j])
            if (searchKoParser(searchValue[0], music_list[i][j])) {
                var k;
                for(k = 1; k < searchValue_length; k++) {
                    if (!searchKoParser(searchValue[k], music_list[i][j+k])) break;
                }
                if (k!=searchValue_length) continue;
                else {
                    substr_bool = true;
                    break;
                }
            }
        }
        if(substr_bool) {
            temp_option = document.createElement('option')
            temp_option.innerHTML = music_list[i].replace('\"', '');
            musicSelector.appendChild(temp_option)
        }
    }
}

function searchKoParser(str1, str2) {
    if(str1 == str2) return true;

    var ko_init = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];
    // var ko_mid = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"];
    // var ko_end = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"];
    remstr1 = str1;
    remstr2 = str2;
    str1 = str1.charCodeAt(0) - 0xAC00;
    str1end = str1 % 28;
    str1mid = ((str1-str1end)/28)%21;
    str1init = (((str1-str1end)/28)-str1mid)/21;
    str2 = str2.charCodeAt(0) - 0xAC00;
    str2end = str2 % 28;
    str2mid = ((str2-str2end)/28)%21;
    str2init = (((str2-str2end)/28)-str2mid)/21;

    if(str1init < -53 && str2init < -53) {
        if(str1 == str2) return true;
    }
    else if(str1init == -53) {
        //초성만 입력되면 확인하기
        if(remstr1 == ko_init[str2init]) return true;
    }
    else {
        //초성만 입력된게 아닐때 (초성, 중성만 비교)
        if(str1end != str2end) {
            if(str1end != 0) return false;
            else {
                if(str1mid == str2mid && str1init == str2init) return true
            }
        }
    }
    return false;
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