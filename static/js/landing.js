const wrapper = document.getElementsByClassName("wrapper")[0];
const bg = document.getElementById("bg");
const window_size = {w: window.innerWidth, h: window.innerHeight};
const username = document.getElementById("username");
const pin = document.getElementById("gamepin");

wrapper.addEventListener("mouseenter", function() {
    bg.style.transform = "scale(1.02)";
})

wrapper.addEventListener("mouseleave", function() {
    bg.style.transform = "scale(1)";
})