function createWheel(radius)
{
    wheelEl.style.width = 2*radius + "px";
    wheelEl.style.height = 2*radius + "px";
    //wheelEl.style.top = (window.innerHeight - radius) + "px";
    
    var total = 0;
    var candidateKeys = Object.keys(candidates);
    for (var i = 0; i < candidateKeys.length; i++)
    {
        total += candidates[candidateKeys[i]].tickets;
    }
    
    wheelEl.innerHTML = "";
    var totalDeg = 0;
    const candidatesInOrder = [];
    for (var i = 0; i < candidateKeys.length; i++){
        candidatesInOrder[i] = i;
    }
    const shuffledCandidates = candidatesInOrder.sort((a, b) => 0.5 - Math.random());
    
    for (var i = 0; i < candidateKeys.length; i++)
    {   
        const index   = shuffledCandidates[i];
        const name    = candidateKeys[index];
        const degrees = (candidates[name].tickets)/total*360;
        createSector(i, radius, degrees, totalDeg, colors[(i + (i == candidateKeys.length - 1 && candidateKeys.length%colors.length == 1))%colors.length], name)
        
        //Save degrees in candidates object
        candidates[name].start = totalDeg;
        candidates[name].end   = totalDeg + degrees;
        totalDeg += degrees;
    }
    wheelEl.innerHTML += "<div class='wheelcap'></div>";
}

function createSector(id, radius, angle, rotation, color, label)
{
    for (var j = 0; j < Math.floor(angle/90); j++)
    {
        wheelEl.innerHTML += "<div id = '"+id+"_"+j+"' class = 'sector'></div>";
        document.getElementById(id+"_"+j).style.transform += "rotate("+(rotation+90*j)+"deg)";
        document.getElementById(id+"_"+j).style.background = color;
    }
    
    wheelEl.innerHTML += "<div id = '"+id+"' class = 'sector'></div>";
    document.getElementById(String(id)).style.transform += "rotate("+(rotation + angle-(angle%90))+"deg)";
    document.getElementById(String(id)).style.transform += "skew("+(90 - (angle%90))+"deg)";
    document.getElementById(String(id)).style.background = color;

    placeText(id, radius, angle, rotation+angle/2, label);
}

function placeText(id, radius, angle, rotation, label)
{
    if (angle > 90) angle = 90;

    wheelEl.innerHTML += "<div id = '"+id+"_label' class = 'sectorLabel'>" + label + "</div>"
    document.getElementById(id+"_label").style.fontSize = "10px";
    document.getElementById(id+"_label").style.whiteSpace = "nowrap";
    var aspectRatio = document.getElementById(id+"_label").clientHeight/document.getElementById(id+"_label").clientWidth;
    var x = 0.95*radius*2*Math.tan(angle/2*Math.PI/180)/(aspectRatio + Math.tan(angle/2*Math.PI/180))/2;
    if (x > 0.95*radius*2) x = 0.95*radius*2;
    if (aspectRatio*x > 0.5*radius*2) x = 0.5*radius*2/aspectRatio;
    document.getElementById(id+"_label").style.fontSize = 10*x/document.getElementById(id+"_label").clientWidth + "px";
    document.getElementById(id+"_label").style.paddingRight = 0.95*radius*2 - x + "px";
    document.getElementById(id+"_label").style.marginLeft = -document.getElementById(id+"_label").clientWidth/2 + "px";
    document.getElementById(id+"_label").style.marginTop = -document.getElementById(id+"_label").clientHeight/2 + "px";
    document.getElementById(id+"_label").style.rotate = rotation + "deg";
    
    // max height: 0.5 radius
    // max width:  0.9 radius
}

