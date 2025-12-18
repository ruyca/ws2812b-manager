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

const colorInput = document.querySelector("#color");
const sendBtn = document.querySelector("#send");

sendBtn.addEventListener("click", () =>{
    console.log(colorInput.value);
    fetch("/color", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            color: colorInput.value
        })
    });
});

const colorPreset1 = "#01c7fc";
const preset1Btn = document.getElementById("preset-1");

preset1Btn.addEventListener("click", () => {
    console.log(colorPreset1);
    fetch("/color", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            color: colorPreset1
        })
    });
});

const colorPreset2 = "#ff4b0f";
const preset2Btn = document.getElementById("preset-2");

preset2Btn.addEventListener("click", () => {
    console.log(colorPreset2);
    fetch("/color", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            color: colorPreset2
        })
    });
});

const colorPreset3 = "#ff0000";
const preset3Btn = document.getElementById("preset-3");

preset3Btn.addEventListener("click", () => {
    console.log(colorPreset3);
    fetch("/color", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            color: colorPreset3
        })
    });
});

const colorPreset4 = "#f72b98";
const preset4Btn = document.getElementById("preset-4");

preset4Btn.addEventListener("click", () => {
    console.log(colorPreset4);
    fetch("/color", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            color: colorPreset4
        })
    });
});