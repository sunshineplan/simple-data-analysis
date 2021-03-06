function copyResult() {
    if ($('#output').val().trim() !== '') {
        navigator.clipboard.writeText($('#output').val())
            .then(() => alert('Text has been copied to clipboard.'))
            .catch(() => alert('Unable to copy to clipboard.'));
    };
}

function clearAll() {
    inputA.setValue('');
    inputB.setValue('');
    $('#output').val('');
}

function swap() {
    var data1 = inputA.getValue();
    var data2 = inputB.getValue();
    inputA.setValue(data2);
    inputB.setValue(data1);
}

function processing() {
    $('#output').val('Processing');
    setTimeout(function () {
        $('#output').val('Processing.');
    }, 250);
    setTimeout(function () {
        $('#output').val('Processing..');
    }, 500);
    setTimeout(function () {
        $('#output').val('Processing...');
    }, 750);
}

$(document).ajaxSend(function () {
    processing();
    process = setInterval(function () {
        processing();
    }, 1000);
}).ajaxComplete(function () {
    clearInterval(process);
}).ajaxError(function () {
    setTimeout(function () {
        $('#output').val('Oops, we encountered a problem! Please contact your administrator for assistance.');
        $('button').attr('disabled', false);
    }, 800);
});

window.onload = function () {
    var data1 = localStorage.getItem('data1');
    if (data1 !== null) inputA.setValue(data1);
    var data2 = localStorage.getItem('data2');
    if (data2 !== null) inputB.setValue(data2);
}

window.onbeforeunload = function () {
    localStorage.setItem('data1', inputA.getValue());
    localStorage.setItem('data2', inputB.getValue());
}
