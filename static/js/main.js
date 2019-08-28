function writeToPage(text) {
    var paragraph = document.createElement("p");
    paragraph.innerText = (new Date()).toLocaleTimeString() + ": " + text;

    var dir = document.getElementById("response");
    dir.insertBefore(paragraph, dir.childNodes[0]);
}

var socket = new Socket("/ws");

socket.onRecv(e => {
    var msg = JSON.parse(event.data);
    writeToPage(msg.text);
});

function updateSlider(value) {
    socket.send({ number: value })
}