var app = angular.module('app', ['ngMessages'])



app.config(function($interpolateProvider) {
    // change up angular's templating syntax to avoid
    // collisions with Jinja2
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
});


// tweet_url, page_url and title_url are defined in the base template
// by Flask's url_for

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

function MainController(TweetService, WikiPageService) {
    var vm = this;

    vm.activated = false;

    vm.annyang = annyang

    function init() {
        vm.twitter = {
            loaded: false,
            error: false,
            tweets: []
        };

        vm.wiki = {
            loaded: false,
            error: false,
            pages: []
        };

    };

    this.submit = function(term) {
        init();
        vm.activated = true;
        getTweets(term);
        getPages(term);
    };

    function getTweets(term) {
        return TweetService.getTweets(term)
            .success(function(data, status, headers, config) {
                vm.twitter.loaded = true;
                vm.twitter.tweets = data.tweets
            })
            .error(function(data, status, headers, config) {
                vm.twitter.error = true;
                vm.twitter.msg = data.msg;
            });
    };

    function getPages(term) {
        return WikiPageService.getTitles(term)
            .success(function(data, status, headers, config) {
                vm.wiki.pages = data.titles;
                vm.wiki.loaded = true;

                for (i=0; i < vm.wiki.pages.length; ++i) {
                    getPage(vm.wiki.pages[i]);
                };
            })
            .error(function(data, status, headers, config) {
                vm.wiki.error = true;
                vm.wiki.msg = data.msg;
            });
    };

    function getPage(page) {
        return WikiPageService.getPage(page.title)
            .success(function(data, status, headers, config) {
                page.summary = data.page.summary
            })
            .error(function(data, status, headers, config) {
                page.summary = data.msg
            });
    }

    vm.annyang.debug();
    vm.annyang.addCommands({"search *val": this.submit});
    vm.annyang.start();
};

app.factory('TweetService', TweetService);
app.factory('WikiPageService', WikiPageService);
app.controller('MainController', MainController);
