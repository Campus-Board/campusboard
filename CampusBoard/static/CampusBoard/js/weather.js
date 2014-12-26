$(function(){

	//var weather = $('#weather');
	var location = "campinas";
	var locationName = "Campinas";
	
	$.getJSON('http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.placefinder%20where%20text%3D%22'+ location +'%22)%20limit%201%20&format=json&diagnostics=true&callback=', function(data){
		//$('#weathertext').show();
		$('#placetitle').html( locationName );
		$('#weatherimage').attr('src','static/CampusBoard/images/weather/'+data.query.results.channel.item.condition.code+'.png');
		$('#temperature').html( convert( $("#derece").val(), data.query.results.channel.item.condition.temp ));
		$('#condition').html(data.query.results.channel.item.condition.text);
	});

	//makeCorsRequest();
  //createCORSRequest();

	(function update_weather(){
		$.getJSON('http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.placefinder%20where%20text%3D%22'+ location +'%22)%20limit%201%20&format=json&diagnostics=true&callback=', function(data){
			$('#weathertext').show();
			$('#placetitle').html( locationName );
			$('#weatherimage').attr('src','static/CampusBoard/images/weather/'+data.query.results.channel.item.condition.code+'.png');
			$('#temperature').html( convert( $("#derece").val(), data.query.results.channel.item.condition.temp ));
			$('#condition').html(data.query.results.channel.item.condition.text);
		});
		// Schedule this function to be run again in 1 sec
		setTimeout(update_weather, 5000);
	})();
});
/* Hava Durumu Widget */
function convert(derece, deger){
	var ilkhesap = 0;
	if (derece=="F")
	{
		Sonuc = deger +' &deg;F';
	}else{
		ilkhesap = (parseInt(deger) -32) * 5 / 9;
		Sonuc = Math.round(ilkhesap) +' &deg;C';
	}
	return Sonuc;
}

function createCORSRequest() {
  var url = "http://weather.yahooapis.com/forecastrss?w=455828&u=c"
  if(XMLHttpRequest) {
    var request = new XMLHttpRequest();
    if("withCredentials" in request) {
      // Firefox 3.5 and Safari 4
      request.open('GET', url, true);
      console.log(request);
      request.onreadystatechange = function(){console.log('entro');};
      request.send();
    } else if (XDomainRequest) {
      // IE8
      var xdr = new XDomainRequest();
      xdr.open("get", url);
      xdr.send();

      // handle XDR responses -- not shown here :-)
    }

  // This version of XHR does not support CORS  
  // Handle accordingly
  }
  /*var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {

    // Check if the XMLHttpRequest object has a "withCredentials" property.
    // "withCredentials" only exists on XMLHTTPRequest2 objects.
    xhr.open(method, url, true);

  } else if (typeof XDomainRequest != "undefined") {

    // Otherwise, check if XDomainRequest.
    // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
    xhr = new XDomainRequest();
    xhr.open(method, url);

  } else {

    // Otherwise, CORS is not supported by the browser.
    xhr = null;

  }*/
  //return xhr;
}
// Make the actual CORS request.
function makeCorsRequest() {
  // All HTML5 Rocks properties support CORS.
  var url = 'http://weather.yahooapis.com/forecastrss?w=455828&u=c';

  var xhr = createCORSRequest('GET', url);
  if (!xhr) {
    alert('CORS not supported');
    return;
  }

  // Response handlers.
  xhr.onload = function() {
    var text = xhr.responseText;
    var title = text.match('<title>(.*)?</title>')[1];
    alert('Response from CORS request to ' + url + ': ' + title);
  };

  xhr.onerror = function(e) {
  	//console.log(e);
    console.log('Woops, there was an error making the request.');
  };

  //xhr.withCredentials = true;
  //xhr.setRequestHeader('Origin', 'http://weather.yahooapis.com/');
  //xhr.setRequestHeader("Access-Control-Allow-Origin", "http://weather.yahooapis.com/");
  xhr.setRequestHeader("Accept", "application/xml");
  xhr.setRequestHeader("Content-Type", "application/xml");
  console.log(xhr);

  xhr.send();
}