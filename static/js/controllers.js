'use strict';

var create_url = "/create/";
var list_url = "/list/";
var reset_url = "/reset/";

angular.module('myApp', [])
    .config(['$interpolateProvider', function ($interpolateProvider) {
      $interpolateProvider.startSymbol('{$');
      $interpolateProvider.endSymbol('$}');
    }])
    .config(function ($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    })
    .controller('MapController', ['$scope', '$http', function ($scope, $http) {
      console.log("MapController");
      var geocoder;
      var infowindow;
      var map;
      var layer;

      $scope.initialize = function () {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 12,
          center: $scope.start_pos
        });

        layer = new google.maps.FusionTablesLayer({
          query: {
            select: '*',
            from: '1oAIu-g2fXBKVYown0m5m8BYf2Ubgt9CJraqmXU0r',
          }
        });
        layer.setMap(map);

        geocoder = new google.maps.Geocoder;
        infowindow = new google.maps.InfoWindow;

        $scope.place_list();

        google.maps.event.addListener(map, 'click', function (event) {
          var loc = {lat: event.latLng.lat(), lng: event.latLng.lng()};
          $scope.geocodeLatLng(geocoder, loc, map, infowindow);
        });
      };
      google.maps.event.addDomListener(window, 'load', $scope.initialize);

      $scope.geocodeLatLng = function (geocoder, location, map, infowindow) {
        var latlng = {lat: parseFloat(location.lat), lng: parseFloat(location.lng)};
        geocoder.geocode({'location': latlng}, function (results, status) {
          if (status === google.maps.GeocoderStatus.OK) {
            var address = null;
            map.setZoom(12);
            if (latlng) {
              map.setCenter(latlng);
            }
            var marker = new google.maps.Marker({
              position: latlng,
              map: map
            });
            if (results[0]) {
              angular.forEach(results, function (data, index) {
                var lat = data.geometry.location.lat();
                var lng = data.geometry.location.lng();
                if (!address && parseFloat(location.lat.toFixed(3)) == parseFloat(lat.toFixed(3))) {
                  address = data;
                }
                else if (!address && parseFloat(location.lng.toFixed(3)) == parseFloat(lng.toFixed(3))) {
                  address = data;
                }
              });
              if (address) {
                infowindow.setContent(address.formatted_address);
                infowindow.open(map, marker);

                var place_data = {
                  "address": address.formatted_address,
                  "latitude": location.lat,
                  "longitude": location.lng
                };
                $scope.create_place(place_data);

              } else {
                infowindow.setContent("No adress found");
                infowindow.open(map, marker);
              }
            } else {
              infowindow.setContent("No results found");
              infowindow.open(map, marker);
            }
          } else {
            infowindow.setContent(status);
            infowindow.open(map, marker);
          }
        });
      };


      $scope.places = [];
      $scope.start_pos = {lat: 41.100119, lng: 29.045054}; // Turkey :)

      $scope.place_list = function () {
        $http.get(list_url).success(function (data) {
          console.log("Success");
          $scope.places = data.object_list;
          angular.forEach($scope.places, function (data, index) {
            var lat = data.latitude;
            var lng = data.longitude;
            var address = data.address;

            var marker = new google.maps.Marker({
              position: {lat: parseFloat(lat), lng: parseFloat(lng)},
              map: map
            });
            if (infowindow) {
              infowindow.setContent(address);
              infowindow.open(map, marker);
            }
            $scope.start_pos = {lat: parseFloat(lat), lng: parseFloat(lng)};
          });

        }).error(function (data, status, headers, config) {
          console.log('Error');
        });
      };

      $scope.get_place = function (place) {
        var marker = new google.maps.Marker({
          position: {lat: parseFloat(place.latitude), lng: parseFloat(place.longitude)},
          map: map
        });
        infowindow.setContent(place.address);
        infowindow.open(map, marker);
      };
      $scope.reset = function () {
        $http.get(reset_url).success(function (data) {
          console.log("Success");
          if (data.result) {
            $scope.initialize();
            $scope.places = data.object_list;
          } else {
            window.alert("There was an error. Please try again.")
            console.log(data.error);
          }

        }).error(function (data, status, headers, config) {
          window.alert("There was an error. Please try again.")
          console.log('Error');
        });
      };
      $scope.create_place = function (place_data) {
        place_data = JSON.stringify(place_data)
        console.log(place_data);
        $http.post(create_url, place_data).success(function (data) {
          console.log("Success");
          console.log(data);
          if (data.result) {
            $scope.places.push(data.object);
          } else {
            console.log(data.error);
          }
        }).error(function (data, status, headers, config) {
          console.log('Error');
        });
      };
    }]);
