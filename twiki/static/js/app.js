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


function TweetController($location, TweetService) {
    vm = this;
    vm.loaded = false;
    vm.error = false;
    vm.tweets = [];

    this.getTweets = function() {
        var term = $location.hash();
        console.log('term is ' + term);
        return TweetService.getTweets(term)
            .success(function(data, status, headers, config) {
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

function WikiController() {
    this.getPages = function() {};
};

app.factory('TweetService', TweetService);
app.controller('TweetController', TweetController);
app.controller('WikiController', WikiController);
