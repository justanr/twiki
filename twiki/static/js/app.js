var app = angular.module('app', [])

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
});


function TweetService($http) {
    var TweetService = {};

    function tweets(term) {
        return $http.get('/tweets/' + term);
    };
    
    function provideLinkURL(tweet) {
        tweet.url = 'https://twitter.com/' + tweet.user + '/status/' + tweet.id;
        return tweet;
    };


    TweetService.getTweets = tweets;
    TweetService.provideLinkURL = provideLinkURL;
    return TweetService;

};


function WikiPageService($http) {
    var WikiPageService = {};

    function pages(term) {
        return $http.get('/pages/' + term);
    };

    WikiPageService.getPages = pages;
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
                vm.tweets = data.tweets.map(TweetService.provideLinkURL)
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
    vm.pages = []

    this.getPages = function() {
        var term = $location.hash();
        return WikiPageService.getPages(term)
            .success(function(data, status, headers, config) {
                vm.pages = data.pages;
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
