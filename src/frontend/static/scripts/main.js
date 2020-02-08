function toggle_on() {
  // console.log('started')
  // const Http = new XMLHttpRequest();
  // const url = 'http://localhost:35060/production?toggle=on';
  // console.log(url)
  // Http.open("POST", url);
  // Http.send();

  // Http.onreadystatechange = (e) => {
  //   console.log(Http.responseText)
  // }
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
  // console.log('stopped')
  // const Http = new XMLHttpRequest();
  // const url = 'http://localhost:35060/production?toggle=off';
  // console.log(url)
  // Http.open("POST", url);
  // Http.send();

  // Http.onreadystatechange = (e) => {
  //   console.log(Http.responseText)
  // }

  var request = new Request('http://localhost:35060/production?toggle=off', {
    method: 'post'
  });
  fetch(request).then(function (response) {
    return response.text();
  }).then(function (text) {
    console.log(text.substring(0, 30));
  });

};