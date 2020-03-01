window.onload = function () {
  var statsTime = document.getElementById("statsTime");
  var statsPersons = document.getElementById("statsPersons");

  function updateStats() {
    destination = "http://" + url.HOST + ":" + url.PORT + "/analysis";
    console.log(destination);
    var request = new Request(destination, {
      method: "get",
      cache: "no-store"
    });

    fetch(request).then(function (response) {
      return response.json();
    }).then(function (text) {
      console.log("length: ");
      console.log(text.persons.length);

      var detectedPersons = "";
      statsTime.innerHTML = text.persons[0].timestamp;
      for (p of text.persons) {
        detectedPersons += "<b><p>gender: " + p.gender + "</b>" +
          " | age: " + p.age +
          " | event: " + p.event + "</p>";
      }
      statsPersons.innerHTML = detectedPersons;
    });
  };
  setInterval(updateStats, 1000);


  var alertsPersons = document.getElementById("alertsPersons");
  var alertsData = document.getElementById("alertsData");

  function updateAlerts() {
    destination = "http://" + url.HOST + ":" + url.PORT + "/alert";
    console.log(destination);
    var request = new Request(destination, {
      method: "get",
      cache: "no-store"
    });

    fetch(request).then(function (response) {
      return response.json();
    }).then(function (text) {
      console.log("length: ");
      console.log(text.persons.length);

      var data = "<p> timestamp: " + text.timestamp + "</p>" +
        "<p> section: " + text.section + "</p>" +
        "<p> event: " + text.event + "</p>";
      alertsData.innerHTML = data;

      var detectedPersons = "";
      for (p of text.persons) {
        detectedPersons += "<p>name: <b>" + p.name + "</b></p>";
      }
      alertsPersons.innerHTML = detectedPersons;
    });
  };

  setInterval(updateAlerts, 1000);
}