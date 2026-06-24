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
        
    });


});