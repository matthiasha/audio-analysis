function fileCtrl ($scope) {
    $scope.filename = '';

    $scope.uploadFile = function() {
        $scope.processDropzone();
    };
}

angular.module('fileApp').controller('fileCtrl', fileCtrl);
