
function bind_temp_buttons(){
    var buttons = document.querySelectorAll("button.temp");
    buttons.forEach((b) => {
        b.onclick = function(e){
	    alert("Temp Adjust!");
            // Remove the on-click for now so that we cant add more buttons
            // var value = e.target.closest("button").innerText;
            // var count = document.querySelector("input.episodeCount").value;
            // send_request("play/"+value+"/"+get_device_name());
        }
    });
}

function bind_mode_buttons(){
    var buttons = document.querySelectorAll("button.mode");
    buttons.forEach((b) => {
        b.onclick = function(e){
	    // Get the selected mode    
            let mode = e.target.closest("button").getAttribute("mode");
	    // Send it back to the server and update the active state of the
	    // buttons
	    send_request("mode/"+mode,() => {
	    	get_mode();
	    });
        }
    });
}

function get_mode(){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Conver the database to JSON and render
	    mode = request.responseText;
            var buttons = document.querySelectorAll("button.mode");
            buttons.forEach((b) => {
	    	// Clear the existing active class 
                b.classList.remove("active");
		// And mark only the matching button as active
		if ( b.getAttribute("mode") == mode ) {
                    b.classList.add("active");
		}
	    });
        }
    };
    request.open("GET", "/mode");
    request.send();

}


function send_request(url,callback = null){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Conver the database to JSON and render
            ;
	    if (callback != null){
		callback();
	    }
        }
    };
    request.open("GET", url);
    request.send();
    
}


bind_temp_buttons();
bind_mode_buttons();
get_mode();
