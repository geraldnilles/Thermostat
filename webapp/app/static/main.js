
function bind_temp_buttons(){
    var buttons = document.querySelectorAll("button.temp");
	for (var i = 0; i < buttons.length; i++){
        var b = buttons[i];
        b.onclick = function(e){
	    alert("Temp!");
            // Remove the on-click for now so that we cant add more buttons
            // var value = e.target.closest("button").innerText;
            // var count = document.querySelector("input.episodeCount").value;
            // send_request("play/"+value+"/"+get_device_name());
        }
    }
}

function bind_mode_buttons(){
    var buttons = document.querySelectorAll("button.mode");
	for (var i = 0; i < buttons.length; i++){
        var b = buttons[i];
        b.onclick = function(e){
	    alert("Mode!");
            // Remove the on-click for now so that we cant add more buttons
            // var value = e.target.closest("button").innerText;
            // var count = document.querySelector("input.episodeCount").value;
            // send_request("play/"+value+"/"+get_device_name());
        }
    }
}


function send_request(url){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Conver the database to JSON and render
            ;
        }
    };
    request.open("GET", url);
    request.send();
    
}


bind_temp_buttons();
bind_mode_buttons();

