
var older_colors = [
    '#FFB399', '#FF6633', '#FF33FF', '#FFFF99', '#00B3E6', 
    '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
    '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
    '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
    '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
    '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
    '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
    '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
    '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
    '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];

var old_colors = ['#103531', '#1e605a','#339890'];
var colors = ['#1f6a64', '#1d5b56','#1f605b'];
var wheelsize = 800;

var wheelEl = document.getElementById("wheel");

var rotation = 0;
var speed = 0;
var candidates = {};

setInterval(update, 20);


function testCandidates(dict)
{
    dict["Delta"] = 5;
    dict["Omega"] = 10;
    dict["Elektra"] = 7;
    dict["Smørekoppen"] = 1;
    dict["A"] = 6;
    dict["B"] = 5;
    dict["C"] = 4;
    dict["D"] = 3;
    dict["E"] = 2;
    dict["F"] = 1;
    //dict["B1"] = 5;dict["C1"] = 4;dict["D1"] = 3;dict["E1"] = 2;dict["F1"] = 1;dict["B2"] = 5;dict["C2"] = 4;dict["D2"] = 3;dict["E2"] = 2;dict["F2"] = 1;dict["B3"] = 5;dict["C3"] = 4;dict["D3"] = 3;dict["E3"] = 2;dict["F3"] = 1;dict["B4"] = 5;dict["C4"] = 4;dict["D4"] = 3;dict["E4"] = 2;dict["F4"] = 1;dict["B5"] = 5;dict["C5"] = 4;dict["D5"] = 3;dict["E5"] = 2;dict["F5"] = 1;dict["B6"] = 5;dict["C6"] = 4;dict["D6"] = 3;dict["E6"] = 2;dict["F6"] = 1;dict["B7"] = 5;dict["C7"] = 4;dict["D7"] = 3;dict["E7"] = 2;dict["F7"] = 1;dict["B8"] = 5;dict["C8"] = 4;dict["D8"] = 3;dict["E8"] = 2;dict["F8"] = 1;
    //dict["Test"] = 7;
    //dict["Test2"] = 7;
    //dict["Test3"] = 7;
}


function startSpin()
{
    speed = 20 + Math.random()*20 ;
    var startBtn = document.getElementById("startButton");
    startBtn.style.visibility = "hidden";
    const arrowText = document.getElementById("arrowtext")
    arrowText.style.visibility = "visible";
    hasSpun = 1
}

function update()
{
    rotate();
    updateArrowText();
}

var hasSpun = 0
function rotate()
{
    rotation += speed;
    
    const arrowText = document.getElementById("arrowtext")
    const startBtn  = document.getElementById("startButton");
    if (speed <= 0 && !hasSpun) {
        speed = 0; 
        startBtn.style.visibility = "visible";
        arrowText.style.visibility = "hidden";

    }
    else if (hasSpun && speed <= 0) {
        party.confetti(startBtn)
        startBtn.style.visibility = "hidden";
        arrowText.style.visibility = "visible";
    }
    else if (speed < .02)  speed = 0;
    else if (speed < .1)   speed *= .97;
    // else if (speed < .2)   speed *= .99;
    else if (speed < .5)   speed *= .997;
    else                   speed *= .99;

    console.log(speed)
    move();


}

function move()
{
    document.getElementById("wheel").style.transform = "translateY(-50%) rotate("+ rotation + "deg)";
    
}


