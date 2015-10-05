# [Twiki](https://justanr.pythonanywhere.com)

A unified Twitter-Wikipedia search client.

## About

Twiki uses Flask on the backend to wrap up [Tweepy](https://github.com/tweepy/tweepy) and [Wikipedia](https://github.com/goldsmith/Wikipedia) to provide a more stripped down, managable API to an Angular frontend.


## The Future
 
### The Javascript side

Coming from zero Angular, I'm sure it's non-idiomatic, however it was surprisingly quick to pick once the idea of directives settled in. I've been told to not use `ng-init` but can't seem to find a clear explaination of why -- the closest I've found is from the documentation that it's only proper use is aliasing with `ng-repeat`. 

Considering that, data retrival is done immediately in the controller by simply calling the function immediately, which feels odd after hearing that working constructors are a no-no for years. However, this simple change makes the HTML feel much more about templating and less about invoking business logic.

I can see why Angular is so popular and widely used. It allows the Javascript to provide all the logic while the HTML remains structural and present, compared to ReactJS where logic and display means can easily become muddled and the HTML is hidden inside render methods.

The entire site could be made into a single page app, but Angular's hash based routing system doesn't quite fit in my headspace right now. In fact, the entire app could be built completely within Angular/Javascript without any backend, though I'd probably use the same stripped down API approach.

The UI testing was done manually; however, looking into Javascript testing with something like Jasmine looks promising.

### UI Improvements

Following up on SPA, a search bar on the results page would be nice, perhaps implemented with a delay to avoid bombarding the backend with requests as a new term is typed in. Suggesting previous search terms -- backed by Redis, for example -- beyond what the browser wants to provide is another potential feature.

Beyond a SPA-style, the CSS could be greatly improved. Currently it's just a basic Bootstrap page complete with a nav bar culled from the bootstrap documentation.

Further styling of the Twitter results using their oEmbed API or a Twitter Javascript library would be an improvement. I'd probably tackle this through the Angular app, rather than through the Python side.

A fallback to non-Javascript enabled clients would be nice.

### The Python Side

I'm not completely satstified with the current backend implementation. The Tweepy and Wikipedia wrappers make adding data for the API a little stiff. For example, including geolocation would require adding either a separate method to each or adding parameters to the existing `search` methods. In the twitter case, adding a parameter would be the preferable method as `tweepy.API.search` accepts a geocode parameter, but the Wikipedia wrapper uses a separate function for geographic searches.

Using an application factory may seem an odd choice for such a simple app, however, it allows putting the application into a known state without messing with creation too much. This also prevents nasty things like leaving a debug-enabled application on a live server by accident.

### Performance improvements

The app feels quick right now, especially compared to it's initial implementation that rounded all the tweets and Wikipedia pages in Flask all at once and load times were around ten to fifteen seconds do to hitting wikipedia 11 times sequentially. 

The Wikipedia summary load times don't feel snappy, and is likely because of the middle man API. Caching these results would help here, but only after the first request for that page. However, since the title search and page summary requests are separate endpoints, these could be cached separately, allowing a page that appears from multiple search terms to be retrieved much faster.

## Running locally

To run locally, provide Twitter application key and secret in the `auth_keys.sample.py` file and rename it to `auth_keys.py`. I found this was simpler than using an environment postactivate hook and then a string of either `app.config.from_envvar` or filtering `os.environ` to locate the correct environment variables. This also provides a measure of future proofing if other API keys needed to be provided.

## Tests

To run the included tests, use `python setup.py test` which will invoke Tox and run the tests on Python 2.7 and 3.4. This make take a few minutes the first time around since it does need to install dependencies. Additionally, arguments can be passed directly to tox using the `--tox-args="..."` option. The tests are run with py.test and line coverage is measured by coverage and pytest-cov.
