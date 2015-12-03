function Hello($scope, $http) {
		$http.get('http://127.0.0.1:8000/api/users').
				success(function(data) {
						$scope.users = data;
				});
		$http.get('http://127.0.0.1:8000/api/current').
				success(function(data) {
						$scope.current = data;
				});

		//var data = { password: '123456', email: 'harchenko.grape@gmail.com' };
		//$http.get('http://127.0.0.1:8000/api/token/?format=json', data).success(function(response, status, headers, config){
		//				$('.api-response').html("API Response: OK<br/>Content: " + JSON.stringify(data));
		//		}).error(function(err, status, headers, config){
		//				$('.api-response').html("API Response: " + status + response);
		//		});
}