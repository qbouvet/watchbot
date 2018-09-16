const WebSocket = require('ws');

console.log("Starting...")

var ip = "192.168.1.37"
var port = "8384"
var ws = new WebSocket("ws://"+ip+":"+port+"/websocket");
ws.onopen = function() {
    ws.send("REQUESTSTREAM");
};
ws.onmessage = function (evt) {
    console.log(evt.data);
};
