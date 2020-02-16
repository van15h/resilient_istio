function toggle_on() {
  var request = new Request('http://localhost:35060/production?toggle=on', {
    method: 'post'
  });
  fetch(request).then(function (response) {
    return response.text();
  }).then(function (text) {
    console.log(text.substring(0, 30));
  });

};

function toggle_off() {
  var request = new Request('http://localhost:35060/production?toggle=off', {
    method: 'post'
  });
  fetch(request).then(function (response) {
    return response.text();
  }).then(function (text) {
    console.log(text.substring(0, 30));
  });

};

function get_analysis() {
  var xmlhttp = new XMLHttpRequest();
  var url = 'http://localhost:35060/analysis';

  xmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var myArr = JSON.parse(this.responseText);
      myFunction(myArr);
    }
  };

  xmlhttp.open("GET", url, true);
  xmlhttp.send();
}