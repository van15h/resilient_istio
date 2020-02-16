window.onload = function () {
  var statsTime = document.getElementById("statsTime");
  var persons = document.getElementById("persons");
  var image = document.getElementById("frame");

  function updateStats() {
    var request = new Request('http://localhost:35060/analysis', {
      method: 'get',
      cache: 'no-store'
    });

    fetch(request).then(function (response) {
      return response.json();
    }).then(function (text) {
      console.log("length: ");
      console.log(text.persons.length);

      image.src = 'data:image/png;base64,' + text.image;

      var detectedPersons = "";
      statsTime.innerHTML = text.persons[0].timestamp;
      for (p of text.persons) {
        detectedPersons += "<b><p>gender: " + p.gender + "</b>" +
        " | age: " + p.age +
        " | event: " + p.event + "</p>";
      }
      persons.innerHTML = detectedPersons;
    });
  };

  setInterval(updateStats, 1000);
}