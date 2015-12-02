function Hello($scope, $http) {
		$http.get('http://127.0.0.1:8000/users').
				success(function(data) {
						$scope.users = data;
				});
		$http.get('http://127.0.0.1:8000/current').
				success(function(data) {
						$scope.current = data;
				});

		var data = { password: '123456', email: 'harchenko.grape@gmail.com' };
		$http.get('http://127.0.0.1:8000/token/?format=json', data).success(function(response, status, headers, config){
						$('.api-response').html("API Response: OK<br/>Content: " + JSON.stringify(data));
				}).error(function(err, status, headers, config){
						$('.api-response').html("API Response: " + status + response);
				});
}