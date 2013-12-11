var login = angular.module("login",[]);

login.controller('LoginControl', function($scope,$http){ 

	$scope.email="";
	$scope.firstname="";
	$scope.lastname="";
	$scope.password="";


	$scope.submit = function(){
		var postData = {email: $scope.email, firstname: $scope.firstname, lastname: $scope.lastname, password: $scope.password}
		console.log(postData)
		$http.post('/post/user',postData);
	}
});