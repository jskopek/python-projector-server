var c = document.querySelector('#draw');
var ctx = c.getContext('2d');

ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;


function drawDot(ctx, x, y) {
    var size = 15;
    ctx.fillStyle = 'rgba(0,0,0,1)';
    ctx.beginPath();
    console.log(x,y, size, 0, Math.PI*2, true);
    ctx.arc(x,y, size, 0, Math.PI*2, true);
    ctx.closePath();
    ctx.fill();


    var pctX = x / ctx.canvas.width;
    var pctY = y / ctx.canvas.height;
    var pctSize = size / ctx.canvas.width;
    sendDrawEvent(pctX, pctY, pctSize);
}

// handle mouse movement
var mouseDown, mouseX, mouseY;

function mouseDown() {
    console.log('mouseDown');
    mouseDown = 1;
    drawDot(ctx, mouseX, mouseY);
}
function mouseUp() {
    mouseDown = 0;
}
function mouseMove(e) {
    console.log('mouseMove');
    mouseX = e.offsetX;
    mouseY = e.offsetY;
    if(mouseDown == 1) {
        drawDot(ctx, mouseX, mouseY);
    }
}
c.addEventListener('mousedown', mouseDown, false);
c.addEventListener('mousemove', mouseMove, false);
c.addEventListener('mouseup', mouseUp, false);

//// socket io
//var port = location.port;
//var port = 5001;
//var socket = io.connect('http://' + document.domain + ':' + port);
//function sendDrawEvent(pctX,pctY,pctSize) {
//    //socket.on('connect', function() {
//    //    console.log('connected');
//    //    socket.emit('message', 'woah');
//    //});
//
//    socket.emit('drawEvent', [pctX,pctY,pctSize]);
//}

var connection = new WebSocket('ws://127.0.0.1:5002');
connection.onopen = function() {
    console.log('connection opened')
}
function sendDrawEvent(pctX, pctY, pctSize) {
    connection.send(JSON.stringify([pctX, pctY, pctSize]));
}
