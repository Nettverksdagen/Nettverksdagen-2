function adaptMask(radius)
{
    var mask = document.getElementById("mask");
    mask.style.height = radius*200/50 + "px";
    mask.style.left = 730-150-(radius-50)*3 + "px";
}