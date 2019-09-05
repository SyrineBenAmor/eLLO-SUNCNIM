
	function onConnectionLost(){
	console.log("connection lost");
	document.getElementById("status").innerHTML = "Connection Lost";
	document.getElementById("messages").innerHTML ="Connection Lost";
	connected_flag=0;
	}

	function onFailure(message) {
		console.log("Failed");
		document.getElementById("messages").innerHTML = "Connection Failed- Retrying";
        setTimeout(MQTTconnect, reconnectTimeout);
        }

		function onMessageArrived(r_message){
		out_msg="Message received "+r_message.payloadString+"<br>";
		out_msg=out_msg+"Message received Topic "+r_message.destinationName;
		//console.log("Message received ",r_message.payloadString);
		console.log(out_msg);
		document.getElementById("messages").innerHTML =out_msg;
		}

	function onConnected(recon,url){
	console.log(" in onConnected " +reconn);
	}

	function onConnect() {
	  // Once a connection has been made, make a subscription and send a message.
	document.getElementById("messages").innerHTML ="Connected to "+host +"on port "+port;
	connected_flag=1
	document.getElementById("status").innerHTML = "Connected";
	console.log("on Connect "+connected_flag);
	//mqtt.subscribe("sensor1");
	//message = new Paho.MQTT.Message("Hello World");
	//message.destinationName = "sensor1";
	//mqtt.send(message);
	  }

    function MQTTconnect() {
	document.getElementById("messages").innerHTML ="";
	var s = "192.168.0.130";
	var p = "9001";
	if (p!="")
	{
	console.log("ports");
		port=parseInt(p);
		console.log("port" +port);
		}
	if (s!="")
	{
		//host=s;
		console.log("host");
		}


	console.log("connecting to "+ host +" "+ port);
	mqtt = new Paho.MQTT.Client(host,port,"clientjsaaa");
	//document.write("connecting to "+ host);
	var options = {
        timeout: 3,
		onSuccess: onConnect,
		onFailure: onFailure,
      
     };
	
        mqtt.onConnectionLost = onConnectionLost;
        mqtt.onMessageArrived = onMessageArrived;
		mqtt.onConnected = onConnected;

	mqtt.connect(options);
	return false;
	}

	function sub_topics(){
		document.getElementById("messages").innerHTML ="";
		if (connected_flag==0){
		out_msg="<b>Not Connected so can't subscribe</b>"
		console.log(out_msg);
		document.getElementById("messages").innerHTML = out_msg;
		return false;
		}
	var stopic= document.forms["subs"]["Stopic"].value;
	console.log("Subscribing to topic ="+stopic);
	mqtt.subscribe(stopic);
	return false;
	}

	function send_message(){
		document.getElementById("messages").innerHTML ="";
		if (connected_flag==0){
		out_msg="<b>Not Connected so can't send</b>"
		console.log(out_msg);
		document.getElementById("messages").innerHTML = out_msg;
		return false;
		}
		var msg = document.forms["smessage"]["message"].value;
		console.log(msg);

		var topic = document.forms["smessage"]["Ptopic"].value;
		message = new Paho.MQTT.Message(msg);
		if (topic=="")
			message.destinationName = "test-topic"
		else
			message.destinationName = topic;
		mqtt.send(message);
		return false;
	}

	function sub_topics_CPU(){
		document.getElementById("messages").innerHTML ="";
		if (connected_flag==0){
		out_msg="<b>Not Connected so can't subscribe</b>"
		console.log(out_msg);
		document.getElementById("messages").innerHTML = out_msg;
		return false;
		}
	var stopic= CPU;
	console.log("Subscribing to topic ="+stopic);
	mqtt.subscribe(stopic);
	return false;
}
