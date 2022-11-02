/**
 *  Get the last part of the url (devided by /)
 */
 $("*[onlyready]").hide();
function getGenerationID() {
    var url = window.location.href;
    var generationID = url.substring(url.lastIndexOf('/') + 1);
    // the page may have a query string, so we need to remove it
    generationID = generationID.split('?')[0];

    return generationID;
}

id = getGenerationID();

$("#renderid").text(id);

const stages = {
    "Preparing...": {
        "start": 1,
        "end": 5
    },
    "Waiting for payment verification..." : {
        "start": 1,
        "end": 5
    },
    "In queue": {
        "start": 6,
        "end": 30
    },
    "Getting started...": {
        "start": 31,
        "end": 35
    },
    "Rendering...": {
        "start": 36,
        "end": 80,
        "progressSupport": true
    },
    "Converting to GIF...": {
        "start": 89,
        "end": 99
    },
    "Done!": {
        "start": 100,
        "end": 100
    }

}

function getValueFromRange(prosent, min, max) {
    return (prosent / 100) * (max - min) + min;
}

fetcher = setInterval(function() {
    r = new XMLHttpRequest();
    r.open("GET", "/job/"+id+"/fetch", true);
    r.onload = function() {
        if (r.status == 200) {
            var data = r.responseText;
            var json = JSON.parse(data);
            $("#status").text(json.display)
            if (json.done) {
                // show and reload the image
                // loop all with attribute "onlyready"
                $("*[onlyready]").show();
                $("#img").attr("src", "/static/img/exported/"+id+".gif");
                clearInterval(fetcher);
                $("#barholder").hide();
                $("#status").hide();
                $("#renderid").hide();
                
            }

            // update the progress bar
            var stage = stages[json.display];
            console.log(stage);
            var progress = stage.start
            var bar = $("#pb");
            bar.attr("aria-valuenow", progress);
            bar.css("width", progress+"%");
            if (stage.progressSupport) {
                var progress = getValueFromRange(json.render.progress, stage.start, stage.end);
                bar.attr("aria-valuenow", progress);
                bar.css("width", progress+"%");
            }

        }
    }
    r.send();
}, 1000);

// when clicking on the download button download the gif¨
$("#download").click(function() {
    var url = "/static/img/exported/"+id+".gif";
    // just open the url in a new tab won't download it because browsers just show the gif
    // so we need to download the file
    var a = document.createElement('a');
    a.href = url;
    a.download = id+".gif";
    a.click();
    
    
});