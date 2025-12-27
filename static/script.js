// Check if music should be playing
const music = document.getElementById("bg-music");

if (sessionStorage.getItem("musicPlaying") === "true") {
    music.play().catch(error => {
        console.log("Autoplay prevented by browser until interaction.");
    });
}