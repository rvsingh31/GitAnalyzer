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
                            $("#repoModal").modal("hide");
                            $("#after_div").hide();
                            $("#before_div").show();
                            $('#newrepo_form').trigger("reset");
                            swal("Complete", "Your repository has been analysed!", "success")
                            .then((value) => {
                                document.location.reload(true);
                              });
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



main.controller('getFileDetails',function($http,$scope){
    $scope.details={
        name:'',
        path:'',
        type:'',
        size:'',
        loc:'',
        lastmodified:''
    };
    
    $scope.get=function(filepath){	
                $http({
                        url:'/getDetails',
                        method:'POST',
                        data:{'filepath':filepath}
                    }).success(function(resp){
                            $scope.details.name = resp.FileName;
                            $scope.details.path = resp.FilePath;
                            $scope.details.type = resp.FileType;
                            $scope.details.size = resp.FileSizeBytes;
                            $scope.details.loc = resp.LinesOfCode;
                            $scope.details.lastmodified = resp.LastModified;
                    })
                    .error(function() {	
                        console.log("failure")
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