function init() {
  websocket = new WebSocket("ws://127.0.0.1:8888/ws");
  websocket.onopen = function(e) { onOpen(e) };
  websocket.onclose = function(e) { onClose(e) };
  websocket.onmessage = function(e) { onMessage(e) };
  websocket.onerror = function(e) { onError(e) };
  btn = document.getElementById("button");
  btn.onclick = onBtnClick;
}

function onOpen(e) {
  console.log(e.type);
	  
}

function onMessage(e) {
  console.log('rcvd: ' + e.data);
}

function onClose(e) {
	console.log("Bye");
}

function onBtnClick(e) {
	console.log("btn");
  	id = document.getElementById("id");
  	type = document.getElementById("type");
  	msg = document.getElementById("msg");

  	var msg = {
	  type: type.value,
	  text: msg.value,
	  id:   id.value,
	  date: Date.now()
    }; 
    console.log(msg);
    websocket.send(JSON.stringify(msg));
}

window.addEventListener("load", init, false);