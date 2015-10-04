var app = angular.module('app', [])

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
});


function TweetService($http) {
    var TweetService = {};

    function tweets(term) {
        return $http.get(tweet_url + term);
    };
    
    TweetService.getTweets = tweets;
    return TweetService;

};


function WikiPageService($http) {
    var WikiPageService = {};

    function getTitles(term) {
        return $http.get(title_url + term);
    };

    function getPage(title) {
        return $http.get(page_url + title)
    }

    WikiPageService.getTitles = getTitles;
    WikiPageService.getPage = getPage
    return WikiPageService
}

function TweetController($location, TweetService) {
    var vm = this;
    vm.loaded = false;
    vm.error = false;
    vm.tweets = [];

    this.getTweets = function() {
        var term = $location.hash();
        console.log('finding tweets');
        return TweetService.getTweets(term)
            .success(function(data, status, headers, config) {
                console.log('loaded tweets');
                vm.loaded = true;
                vm.tweets = data.tweets
            })
            .error(function(data, status, headers, config) {
                vm.loaded = true;
                vm.error = true;
                vm.msg = data.msg;
            });
    };
};

function WikiController($location, WikiPageService) {
    var vm = this;
    vm.loaded = false;
    vm.error = false;
    vm.titles = []

    this.getTitles = function() {
        var term = $location.hash();
        return WikiPageService.getTitles(term)
            .success(function(data, status, headers, config) {
                vm.titles = data.titles;
                vm.loaded = true;
            })
            .error(function(data, status, headers, config) {
                vm.loaded = true;
                vm.error = true;
                vm.msg = data.msg;
            });
    };


};

app.factory('TweetService', TweetService);
app.factory('WikiPageService', WikiPageService);
app.controller('TweetController', TweetController);
app.controller('WikiController', WikiController);
