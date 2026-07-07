$(document).ready(function () {

    $('.text').textillate({
        loop: true,
        in: {
            effect: 'bounceIn'
        },
        out: {
            effect: 'bounceOut'
        }
    });

    //siri config
    var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 180,
    style: "ios9",
    amplitude: "1",
    speed: "0.30",
    autostart: true,

    });

    $('.siri-message').textillate({
        loop: true,
        in: {
            effect: 'rotateIn',
            sequence: true
        },
        out: {
            effect: 'rotateOut',
            reverse: true
        }
    });

    // mic click event
    $("#MicBtn").click(function (e) { 

        eel.playAssisstantSound()
        $("#Oval").attr("hidden", true);
        $("#Siriwave").attr("hidden", false);
        eel.allCommand()()
        
    });

    function PlayAssistant(message) {
        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#Siriwave").attr("hidden", false);
            eel.allCommand(message);
            $("#chatbox").val("")
            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden",true);
        }
    }

    function ShowHideBtn(message) {
        if (message.length == 0) {
            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden", true);
        }
        else {
            $("#MicBtn").attr("hidden", true);
            $("#SendBtn").attr("hidden", false);
        }
    }

    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideBtn(message)

    });

    $("#SendBtn").click(function () {

        let message = $("#chatbox").val()
        PlayAssistant(message)

    });

    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) { `13 is enter key in js`
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    })


});



eel.expose(showSiriWave);
function showSiriWave() {
    eel.playAssisstantSound();
    $("#Oval").attr("hidden", true);
    $("#Siriwave").attr("hidden", false);
    eel.allCommand()();
}

function doc_keyUp(e) {
    if (e.key === 'u' && e.altKey) {
        showSiriWave();   // Alt+U still works manually
    }
}

document.addEventListener('keyup', doc_keyUp, false);


