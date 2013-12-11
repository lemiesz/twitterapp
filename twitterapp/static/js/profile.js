twit.controller('profileControl',function($scope,$http){
	$scope.listOfTweets = []
	$scope.isCollapsed = false;
	$scope.myAverage = 0;
	$scope.dbAverage = 0;
	var getChartData = function(){
		var avg = 0;
		for(var i = 0; i<$scope.listOfTweets.length; i++){
			avg = avg + parseInt($scope.listOfTweets[i].sentimentValue);
		}
		$scope.myAverage = avg/$scope.listOfTweets.length
	}


	var getDbAverage = function(){
		$http({method: 'GET', url:'/get/avgSen'}).
			success(function(data,status,headers,config){
				$scope.dbAverage = data[0];
			}).
			error(function(data,status,headers,config){
				console.log(data[0] || 'ERROR OCCURED GETTING AVERAGE VALUE')
			})
	}

	$scope.getTweets = function(){
		$http({method: 'GET',url:'/get/userTweets'}).
			success(function(data,status,headers,config){
				for(var i = 0; i<data.length;i++){
					$scope.listOfTweets.push(JSON.parse(data[i]))
				}
				getChartData();
				console.log($scope.listOfTweets)
			}).
			error(function(data,status,headers,config){
				console.log(data || 'ERROR OCCURED GETTING USER')
			})	
	}

	$scope.collapse = function(){
		if($scope.isCollapsed == true){
			$scope.isCollapsed == false;
		}
		else if ($scope.isCollapsed == false){
			$scope.isCollapsed = true;
		}
	}
	$scope.getTweets();
	getDbAverage();


});