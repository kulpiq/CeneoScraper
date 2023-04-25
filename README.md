# CeneoScraper

## CSS colectors of the components of opinion in [Ceneo.pl]() service

|Components|Variable/Dictionary key|Data type|Selector|
| :- | :- | :- | :- |
|opinion|`opinion/single_opinion`|`Tag, dictionary`|`div.js_product-review`|
|opinion ID|`opinion_id|string|`["data-entry-id"]`|
|opinion’s author|`author`|`string`|`span.user-post__author-name`|
|author’s recommendation|`recommendation`|`bool`|`span.user-post__author-recomendation > em`|
|score expressed in number of stars|`score`|`float`|`span.user-post__score-count`|
|opinion’s content|`description`|`string`|`div.user-post__text`|
|list of product advantages|`pros`|`string`|`div.review-feature__col:has( > div.review-feature__title--positives) > div.review-feature__item`|
|list of product disadvantages|`cons`|`string`|`div.review-feature__col:has( > div.review-feature__title--negatives) > div.review-feature__item`|
|how many users think that opinion was helpful|`like`|`int`|`button.vote-yes["data-total-vote"]`,`button.vote-yes > span<`, `span[id^=votes-yes]`|
|how many users think that opinion was unhelpful|`dislike`|`int`|`button.vote-no["data-total-vote"`]`button.vote-no > span`,`span[id^=votes-no]`|
|publishing date|`publish_date`|`string`|`span.user-post__published > time:nth-child(1) ["datetime"]`|
|purchase date|`purchase_date`|`string`|`span.user-post__published > time:nth-child(2) ["datetime"]`|

## Python libraries used in project
1. Requests
2. BeautifulSoup
3. Json
4. Os
5. Translate
6. Numpy