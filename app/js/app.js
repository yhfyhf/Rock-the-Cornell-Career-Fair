var cfApp = angular.module('cfApp', [
    'ngRoute',
    'cfControllers'
]);

cfApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/companies', {
                templateUrl: 'partials/company-list.html',
                controller: 'CompanyListCtrl'
            }).
            otherwise({
                redirectTo: '/companies'
            });
    }
]);
