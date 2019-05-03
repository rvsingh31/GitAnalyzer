var main=angular.module('main',[]);


main.controller('analyzeRepo',function($http,$scope){
    $scope.url = "";
    
    $scope.analyze = function(){	
                $http({
                        url:'/analyze',
                        method:'POST',
                        data:{'url':$scope.url}
                    }).success(function(resp){
                        if (resp == "analyzed"){
                            $("#after_div").hide();
                            $("#before_div").show();
                            window.location.href = "\main"
                       }
                       else{
                            $.notify({
                                message: "Some Error Occured. Please try again later!"
                            },{
                                type: 'danger',
                                timer: 4000,
                                placement: {
                                    from: 'bottom',
                                    align: 'right'
                                }
                            });
                       }
                    })
                    .error(function() {	
                            $("#repoModal").modal("hide");
                            $("#after_div").hide();
                            $("#before_div").show();
                            $('#newrepo_form').trigger("reset");
                            
                        $.notify({
                            message: "Some Error Occured. Please try again later!"
                        },{
                            type: 'danger',
                            timer: 4000,
                            placement: {
                                from: 'bottom',
                                align: 'right'
                            }
                        }); 
                    })
    }


});




main.controller('ListCtrl', function($http,$scope) {
        $scope.items = ''
        $scope.getAll = function(){

            $http({
                url:'/getAllRepos',
                method:'GET',
            }).success(function(resp){
                $scope.items = JSON.parse(JSON.stringify(resp))
            })
            .error(function() {	
                console.log("error")
            })
        }
        $scope.getAll();
  });
  
  // jQuery
  $('.dropdown-menu').find('input').click(function(e) {
    e.stopPropagation();
  });