var cfControllers = angular.module('cfControllers', []);

cfControllers.controller('CompanyListCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('companies/another.json').success(function(data) {
            $scope.companies = data;
        });
    }
]);
