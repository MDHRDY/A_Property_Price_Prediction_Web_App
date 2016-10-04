function initMap() {
	
	var broadway = {
		info: '<strong>Property 1</strong><br>\
					5224 N Broadway St<br> New York, NY 60640<br>\
					Sale Year: 2014, Price $678k<br>',
		lat: 40.8380377095,
		long: -73.9027923602
	};

	var belmont = {
		info: '<strong>Property2</strong><br>\
					5224 N Broadway St<br> New York, NY 60640<br>\
					Sale Year: 2014, Price $678k<br>',
		lat: 40.8383885679,
		long: -73.9022425262
	};

	var sheridan = {
		info: '<strong>Property3</strong><br>\r\
					5224 N Broadway St<br> New York, NY 60640<br>\r\
					Sale Year: 2014, Price $678k<br>',
		lat: 40.8380120729,
		long: -73.9016901473
	};

	var property4 = {
		info: '<strong>Property4</strong><br>\r\
					5224 N Broadway St<br> New York, NY 60640<br>\
					Sale Year: 2014, Price $678k<br>',
		lat: 40.838455749,
		long: -73.9005619362
	};

	var property5 = {
		info: '<strong>Property 5</strong><br>\r\
					5224 N Broadway St<br> New York, NY 60640<br>\
					Sale Year: 2014, Price $678k<br>',
		lat: 40.8385023841,
		long: -73.9005329548
	};


	var locations = [
      [broadway.info, broadway.lat, broadway.long, 0],
      [belmont.info, belmont.lat, belmont.long, 1],
      [sheridan.info, sheridan.lat, sheridan.long, 2],
      [property4.info, property4.lat, property4.long, 3],
      [property5.info, property5.lat, property5.long, 4],

    ];

	var map = new google.maps.Map(document.getElementById('mapMultLoc'), {
		zoom: 16,
		center: new google.maps.LatLng(40.8380377095, -73.9027923602),
		mapTypeId: google.maps.MapTypeId.ROADMAP
	});

	var infowindow = new google.maps.InfoWindow({});

	var marker, i;

	for (i = 0; i < locations.length; i++) {
		marker = new google.maps.Marker({
			position: new google.maps.LatLng(locations[i][1], locations[i][2]),
			map: map
		});

		google.maps.event.addListener(marker, 'click', (function (marker, i) {
			return function () {
				infowindow.setContent(locations[i][0]);
				infowindow.open(map, marker);
			}
		})(marker, i));
	}
}