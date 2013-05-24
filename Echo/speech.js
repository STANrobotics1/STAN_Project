var recognition;


function handleSpeech(event) {
  alert("Hello");
}

function initSpeechRecognition() {
  recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  //recognition.interimResults = true;
  recognition.lang = 'en';
  recognition.onresult = function (event) {
    console.log("Handling result");
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        //insertAtCaret(textAreaID, event.results[i][0].transcript);
        document.getElementById("output").innerHTML += event.results[i][0].transcript;
      }
    }
  };
}

function startSpeechRecognition() {
  recognition.start();
  console.log("Starting");
}

function stopSpeechRecognition() {
  recognition.stop();
  console.log("Stopping");
}

function handleResult(event) {
  console.log("Handling result");
  for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        document.getElementById("output").innerHTML += event.results[i][0].transcript;
        //insertAtCaret("output", event.results[i][0].transcript);
      }
  }
  console.log("Stopping");
  recognition.stop();
}