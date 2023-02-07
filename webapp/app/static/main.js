
function bind_temp_buttons(){
    var buttons = document.querySelectorAll("button.temp");
    buttons.forEach((b) => {
        b.onclick = function(e){
            let dir = e.target.closest("button").value;
	    send_request("settemp/"+dir,()=>{
		get_settemp();
	    });
        }
    });
}

function bind_mode_buttons(){
    var buttons = document.querySelectorAll("button.mode");
    buttons.forEach((b) => {
        b.onclick = function(e){
	    // Get the selected mode    
            let mode = e.target.closest("button").value;
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
		if ( b.value == mode ) {
                    b.classList.add("active");
		}
	    });
        }
    };
    request.open("GET", "mode");
    request.send();

}

function get_temp(){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Conver the database to JSON and render

            document.querySelector("#currtemp").innerHTML = request.responseText;

        }
    };
    request.open("GET", "temp");
    request.send();
}

function get_settemp(){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Conver the database to JSON and render
	    temps = JSON.parse(request.responseText);

            document.querySelector("#lowtemp").innerHTML = temps[0];
            document.querySelector("#hightemp").innerHTML = temps[1];

        }
    };
    request.open("GET", "settemp");
    request.send();
}


function send_request(url,callback = null){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Conver the database to JSON and render
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
get_settemp();

get_temp();
