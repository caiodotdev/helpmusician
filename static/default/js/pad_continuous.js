padStarted = undefined;

function controlPad(id) {
    var playerAudio = padSamples.player(id);
    if (padStarted) {
        if (padStarted.name === id) {
            padStarted.stop();
            $('#' + padStarted.name).removeClass('pad-active');
            padStarted = undefined;
        } else {
            padStarted.stop();
            $('#' + padStarted.name).removeClass('pad-active');
            padStarted = playerAudio;
            padStarted.name = id;
            padStarted.start(0);
            $('#' + id).addClass('pad-active');
        }
    } else {
        padStarted = playerAudio;
        padStarted.name = id;
        padStarted.start(0);
        $('#' + id).addClass('pad-active');
    }

}


document.body.onkeydown = function (e) {
    if (e.keyCode == 81) {
        padOn(pad1);
    }
    if (e.keyCode == 87) {
        padOn(pad2);
    }
    if (e.keyCode == 69) {
        padOn(pad3);
    }
    if (e.keyCode == 65) {
        padOn(pad4);
    }
    if (e.keyCode == 83) {
        padOn(pad5);
    }
    if (e.keyCode == 68) {
        padOn(pad6);
    }
    if (e.keyCode == 90) {
        padOn(pad7);
    }
    if (e.keyCode == 88) {
        padOn(pad8);
    }
    if (e.keyCode == 67) {
        padOn(pad9);
    }
    if (e.keyCode == 70) {
        padOn(pad10);
    }
    if (e.keyCode == 71) {
        padOn(pad11);
    }
    if (e.keyCode == 86) {
        padOn(pad12);
    }
}

document.body.onkeyup = function (e) {
    if (e.keyCode == 81) {
        padOff(pad1);
    }
    if (e.keyCode == 87) {
        padOff(pad2);
    }
    if (e.keyCode == 69) {
        padOff(pad3);
    }
    if (e.keyCode == 65) {
        padOff(pad4);
    }
    if (e.keyCode == 83) {
        padOff(pad5);
    }
    if (e.keyCode == 68) {
        padOff(pad6);
    }
    if (e.keyCode == 90) {
        padOff(pad7);
    }
    if (e.keyCode == 88) {
        padOff(pad8);
    }
    if (e.keyCode == 67) {
        padOff(pad9);
    }
    if (e.keyCode == 70) {
        padOff(pad10);
    }
    if (e.keyCode == 71) {
        padOff(pad11);
    }
    if (e.keyCode == 86) {
        padOff(pad12);
    }
}
