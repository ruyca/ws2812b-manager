console.log("JavaScript is loaded!");
const onButton = document.getElementById("on-button");

onButton.addEventListener("click", function(){
    console.log("ON BUTTON was clicked");
    fetch('/on', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => console.log(data));
});

const offButton = document.getElementById("off-button");
offButton.addEventListener("click", function(){
    console.log("OFF BUTTON was clicked");
    fetch('/off',{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
});