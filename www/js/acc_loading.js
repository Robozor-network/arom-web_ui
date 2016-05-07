var AROM_nodes = null;

function myFunction(data){
    $.ajax({
        url: "/bootstrap/"+data,
        //dataType: 'html',
        success: function(result){
            alert("Skript byl načten a spuštěn!");
            $("acc_content").html(result);
        },
        error: function(result){
            alert("Skript Není - "+result);
        }
    });
}


function loadModal(data){
	$('.modal-body').load('/bootstrap/'+data,function(result){
	    $('.modal-body').modal({show:true});
	});
}

function loadDevices(devices){
	for (var i = devices.length - 1; i >= 0; i--) {
		console.log(devices[i])
		$("#device_sidebar").append("<li class='nav-item'><a href='/bootstrap'>"+devices[i]+"</a></li>");
	}

}


function setCookie(name, value){
    document.cookie = name+"="+value+""+"; path=/";
}

function getCookie(name){
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}



/*    ROS
=======================================*/
	var ros = new ROSLIB.Ros({
	    url : 'ws://'+window.location.hostname+':9090'
	    //url : 'ws://telescopeC.local:9090'
	}); 

	ros.on('connection', function() {
		console.log("Connected to websocket server.");
	    //var fbDiv = document.getElementById('feedback');
	    //fbDiv.innerHTML += "<p>Connected to websocket server.</p>";
	});

	ros.on('error', function(error) {
		console.log("Error connecting to websocket server.");
	    //var fbDiv = document.getElementById('feedback');
	    //fbDiv.innerHTML += "<p>Error connecting to websocket server.</p>";
	});

	ros.on('close', function() {
		console.log("Connection to websocket server closed.");
	    //var fbDiv = document.getElementById('feedback');
	    //fbDiv.innerHTML += "<p>Connection to websocket server closed.</p>";
	});


	var MountControl = new ROSLIB.Topic({
	    ros : ros,
	    name : '/arom/mount',
	    messageType : 'arom/DriverControlm'    // tohle se zjisti v ''rostopic info ''
	});

	var MountMessage = new ROSLIB.Message({   //rosmsg show arom/DriverControlm
	    name : "",
	    type : "",
	    data : "",
	    validate : "",
	    check : ""
	});
	var nodes = []

	ros.getParams(function(params) {
	    //console.log(params);
	});

	ros.getNodes(function(params) {
	    var i = 0;
	    var len = params.length;
	    for (; i < len; i++) { 
	        if (params[i].indexOf("AROM") > -1){
	            nodes.push(params[i]);
	        }
	    }
	    console.log(nodes);
	    loadDevices(nodes);
	    window.AROM_nodes = nodes
	});
	console.log(nodes);  

/*    ROS message alert
=======================================*/


var listener = new ROSLIB.Topic({
    ros : ros,
    name : '/rosout',
    messageType : 'rosgraph_msgs/Log'
});

listener.subscribe(function(msg) {
    //console.log(msg);
    if (msg.level == 8 && getCookie("setting_alert_error") == 'true'){
        Lobibox.notify('error', {
            size: 'mini',
            title: msg.name,
            msg: msg.msg,
            icon: false
        });
    }
    if (msg.level == 4 && getCookie("setting_alert_warn") == 'true'){
        Lobibox.notify('warning', {
            size: 'mini',
            title: msg.name,
            msg: msg.msg,
            icon: false
        });
    }
    if (msg.level == 1 && getCookie("setting_alert_debug") == 'true'){
        Lobibox.notify('success', {
            size: 'mini',
            title: msg.name,
            msg: msg.msg,
            icon: false
        });
    }
    if (msg.level == 2 && getCookie("setting_alert_info") == 'true'){
        Lobibox.notify('info', {
            //delayToRemove: 100,
            size: 'mini',
            title: msg.name,
            msg: msg.msg,
            icon: false
        });
    }
});


/*    /ROS message alert
=======================================*/





$("#menu-toggle").click(function(e) {
    e.preventDefault();
$("#wrapper").toggleClass("toggled");



});



$(document).ready(function(){
	console.log("loaded");
	console.log(window.AROM_nodes);
	console.log("loaded");
	console.log(AROM_nodes);
	//for (var i = window.AROM_nodes.length - 1; i >= 0; i--) {
	//	console.log(window.AROM_nodes[i])
	//}



}) 
