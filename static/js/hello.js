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
