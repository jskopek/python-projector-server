var c = document.querySelector('#draw');
var ctx = c.getContext('2d');

ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;


function drawDot(ctx, x, y) {
    var size = 15;
    ctx.fillStyle = 'rgba(0,0,0,1)';
    ctx.beginPath();
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
    mouseDown = 1;
    drawDot(ctx, mouseX, mouseY);
}
function mouseUp() {
    mouseDown = 0;
}
function mouseMove(e) {
    mouseX = e.offsetX;
    mouseY = e.offsetY;
    if(mouseDown == 1) {
        drawDot(ctx, mouseX, mouseY);
    }
}
c.addEventListener('mousedown', mouseDown, false);
c.addEventListener('mousemove', mouseMove, false);
c.addEventListener('mouseup', mouseUp, false);

var address = document.location.hostname;
var connection = new WebSocket('ws://' + address + ':5002');
connection.onopen = function() {
    console.log('connection opened')
}
var msgId = 0
function sendDrawEvent(pctX, pctY, pctSize) {
    connection.send(JSON.stringify([pctX, pctY, pctSize, msgId]));
    console.log('drawEvent sent with ID:', msgId);
    msgId++;
}
