function updateArrowText() {
    //Convert rotation to text and display
    for (const name in candidates) {
        // Works until we have rotated more than 1000 times.
        const angle = (360*1000 - rotation)%(360)
        const text = document.getElementById("arrowtext")
        const maxWidth = 400

        if (angle >= candidates[name].start && angle < candidates[name].end) {

            text.innerHTML = name
            text.style.fontSize = 10+"px"
            const width = text.clientWidth
            let fontSize = Math.min(10*maxWidth/width,70)
            text.style.fontSize = fontSize+"px"
            break
        }
    }
}