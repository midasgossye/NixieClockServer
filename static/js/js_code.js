function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('time').innerHTML =
        h + ":" + m + ":" + s;
}
function checkTime(i) {
    if (i < 10) { i = "0" + i };  // add zero in front of numbers < 10
    return i;
}
$(document).ready(function () {
    startTime();
});

function editAPIkey() {

    let name = $('#api_key').text();
    $('#api_key').html('');
    $('<input></input> <img src="static/img/check.svg" id="edit_api_key" onclick="confirmAPIkey()" />')
        .attr({
            'type': 'text',
            'name': 'fname',
            'id': 'txt_apikey',
            'size': '34',
            'value': name
        })
        .appendTo('#api_key');
    $('#api_key').focus();
}

function confirmAPIkey() {
    let api_key_val = $('#txt_apikey').val();
    let confirmed_api_key = "";
    let new_temp = -1000;
    $.getJSON($SCRIPT_ROOT + '/_change_api_key', {
        api_key: api_key_val
    }, function (data) {
        confirmed_api_key = data.api_key;
        new_temp = data.temp;

        const para = document.querySelector('#api_key');
        para.innerHTML = `${confirmed_api_key} <img src="static/img/edit.svg" id="edit_api_key" onclick="editAPIkey()" />`;

        const temp_span = document.querySelector('#temp');
        if (new_temp > -100) {
            temp_span.innerHTML = `${new_temp} C`;
        }
        else {
            temp_span.innerHTML = 'Unable to fetch temperature';
        }
    })
}

function editCity() {
    let city_name = $('#weather_city').text();
    $('#weather_city').html('');
    $('<input></input> <img src="static/img/check.svg" id="edit_city_name" onclick="confirmCity()" />')
        .attr({
            'type': 'text',
            'name': 'fname',
            'id': 'txt_city',
            'size': '20',
            'value': city_name
        })
        .appendTo('#weather_city');
    $('#weather_city').focus();
}

function confirmCity() {
    let city_name = $('#txt_city').val();

    $.getJSON($SCRIPT_ROOT + '/_change_city', {
        city_name: city_name
    }, function (data) {
        $('#weather_city_2').html(`${city_name}`);
        new_temp = data.temp;

        const para = document.querySelector('#weather_city');
        para.innerHTML = `${city_name} <img src="static/img/edit.svg" id="edit_city" onclick="editCity()" />`;

        const temp_span = document.querySelector('#temp');
        if (new_temp > -100) {
            temp_span.innerHTML = `${new_temp} C`;
            
        }
        else {
            temp_span.innerHTML = 'Unable to fetch temperature';
        }
    })

}


