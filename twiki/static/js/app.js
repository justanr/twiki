var app = angular.module('app', [])



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


function TermService($location) {
    var TermService = {};

    TermService.term = $location.hash().split('+').join(' ');
    return TermService;
}

function ResultNameController(TermService) {
    vm = this;
    vm.term = TermService.term;
}

function TweetController(TermService, TweetService) {
    var vm = this;
    vm.loaded = false;
    vm.error = false;
    vm.tweets = [];

    function getTweets() {
        console.log('finding tweets');
        return TweetService.getTweets(TermService.term)
            .success(function(data, status, headers, config) {
                console.log('loaded tweets');
                vm.loaded = true;
                vm.tweets = data.tweets
            })
            .error(function(data, status, headers, config) {
                vm.error = true;
                vm.msg = data.msg;
            });
    };

    getTweets();
};

function WikiController(TermService, WikiPageService) {
    var vm = this;
    vm.loaded = false;
    vm.error = false;
    vm.pages = []

    function getTitles() {
        return WikiPageService.getTitles(TermService.term)
            .success(function(data, status, headers, config) {
                vm.pages = data.titles;
                vm.loaded = true;

                for (i=0; i < vm.pages.length; ++i) {
                    getPage(vm.pages[i]);
                };
            })
            .error(function(data, status, headers, config) {
                vm.error = true;
                vm.msg = data.msg;
            });
    };

    function getPage(page) {
        console.log("Loading summary for " + page.title);
        return WikiPageService.getPage(page.title)
            .success(function(data, status, headers, config) {
                page.summary = data.page.summary
            })
            .error(function(data, status, headers, config) {
                page.summary = data.msg
            });
    }

    getTitles();
};

app.factory('TweetService', TweetService);
app.factory('WikiPageService', WikiPageService);
app.factory('TermService', TermService);
app.controller('TweetController', TweetController);
app.controller('WikiController', WikiController);
app.controller('ResultNameController', ResultNameController);
