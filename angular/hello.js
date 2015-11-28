function Hello($scope, $http) {
    $http.get('http://127.0.0.1:8000/users').
        success(function(data) {
            $scope.users = data;
        });
    $http.get('http://127.0.0.1:8000/current').
        success(function(data) {
            $scope.current = data;
        });
}