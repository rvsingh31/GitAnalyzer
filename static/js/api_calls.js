$(document).on('click','.type_file',{},function(){
    path = $(this).attr('file_path');
    
    var scope = angular.element(document.getElementById("detailsblock")).scope();
    scope.$apply(function () {
            scope.get(path);
    });
    
    applyFilterToAllSheets(path);

});


function applyFilterToAllSheets(path){
    activesheets.forEach(worksheet =>  
        worksheet.applyFilterAsync(
            "File Path",
            path,
            tableau.FilterUpdateType.REPLACE
        )
    );  
}

function filterBySingleValue(path){
    activesheet.applyFilterAsync(
        "File Path",
        path,
        tableau.FilterUpdateType.REPLACE
    );
}

function AddValues(){
    activesheet.applyFilterAsync(
        "File Path",
        ["appveyor.yml",".travis.yml"],
         tableau.FilterUpdateType.ADD
    );
}

function reset_this(){
    activesheets.forEach(worksheet =>  
        worksheet.clearFilterAsync("File Path")
    );
    
}

function filterScore() {
    activesheet.applyRangeFilterAsync(
      "Score",
      {
        min: 0,
        max: 1000000
      },
      tableau.FilterUpdateType.REPLACE);
  }     