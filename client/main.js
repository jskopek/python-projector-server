var c = document.querySelector('#draw');
var ctx = c.getContext('2d');

ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;


function drawDot(ctx, x, y) {
    var size = parseInt(document.getElementById('size').value);
    var color = document.getElementById('color').value;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x,y, size, 0, Math.PI*2, true);
    ctx.closePath();
    ctx.fill();


    var pctX = x / ctx.canvas.width;
    var pctY = y / ctx.canvas.height;
    var pctSize = size / ctx.canvas.width;
    sendDrawEvent(pctX, pctY, pctSize, color);
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
function sendDrawEvent(pctX, pctY, pctSize, color) {
    var rgbColorComponents = color.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
    var msgColor = rgbColorComponents ? [rgbColorComponents[1],rgbColorComponents[2],rgbColorComponents[3]] : '';
    connection.send(JSON.stringify([pctX, pctY, pctSize, msgColor, msgId]));
    console.log('drawEvent sent with ID:', msgId, [pctX, pctY, pctSize, msgColor, msgId]);
    msgId++;
}

$("#color").spectrum({
    flat: true,
    preferredFormat: "rgb",
    showInput: true
});
