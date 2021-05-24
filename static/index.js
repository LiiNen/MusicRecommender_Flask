music_list = document.getElementById('music_list');

console.log('hello');

function selectVisible() {
    selector = document.getElementById('musicSelector');
    if(selector.style.visibility == 'hidden') selector.style.visibility = 'visible';
    else selector.style.visibility = 'hidden';
}

function search() {
    console.log('search')
}