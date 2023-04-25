import json
import os
import requests
import numpy as np
from bs4 import BeautifulSoup
from translate import Translator

def get_element(dom_tree, selector=None, attribute=None, return_list = None):
    try:
        if return_list:
            return ", ".join([tag.text.strip() for tag in dom_tree.select("div.review-feature__col:has( > div.review-feature__title--positives) > div.review-feature__item")])
        if attribute:
            if selector:
                return dom_tree.select_one(selector)[attribute].strip()
            return dom_tree[attribute]
        return dom_tree.select_one(selector).text.strip()
    
    except (AttributeError, TypeError):
        return None
def clean_text(text):
     
    return " ".join(text.replace(r"\s", " ").split())
selectors = {
                    "opinion_id": [None, "data-entry-id"],
                    "author": ["span.user-post__author-name"],
                    "recommendation": ["span.user-post__author-recommendation > em"],
                    "score": ["span.user-post__score-count"],
                    "description": ["div.user-post__text"],
                    "pros": ["div.review-feature__col:has( > div.review-feature__title--positives) > div.review-feature__item",None, True],
                    "cons": ["div.review-feature__col:has( > div.review-feature__title--negatives) > div.review-feature__item"],
                    "like": ["button.vote-yes > span"],
                    "dislike": ["button.vote-yes > span"],
                    "publish_date": ["span.user-post__published > time:nth-child(1)", "datetime"],
                    "purchase_date": ["span.user-post__published > time:nth-child(2)", "datetime"]
                }
from_lang = 'pl'
to_lang = "eng"
translator = Translator(from_lang, to_lang)
#product_code = input("Please enter the product code: ")
product_code = "129910940"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
all_opinions = []

while url:
    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        print(url)
        page_dom = BeautifulSoup(response.text, 'html.parser')
        print(get_element(page_dom))
        opinions = page_dom.select("div.js_product-review")
        
        if len(opinions) > 0:

            for opinion in opinions:

                # opinion_id = opinion["data-entry-id"]
                # author = get_element(opinion, "span.user-post__author-name")
                # recommendation = get_element(opinion, "span.user-post__author-recommendation > em")
                # score = get_element(opinion, "span.user-post__score-count")
                # description = get_element(opinion, "div.user-post__text")
                # pros = get_element(opinion, "div.review-feature__col:has( > div.review-feature__title--positives) > div.review-feature__item",None, True)
                # pros = [p.text.strip() for p in pros]
                # cons = opinion.select("div.review-feature__col:has( > div.review-feature__title--negatives) > div.review-feature__item")
                # cons = [c.text.strip() for c in cons]
                # like = get_element(opinion, "button.vote-yes > span")
                # dislike = get_element(opinion, "button.vote-yes > span")
                # publish_date = get_element(opinion, "span.user-post__published > time:nth-child(1)", "datetime")
                # purchase_date = get_element(opinion, "span.user-post__published > time:nth-child(2)", "datetime")

                single_opinion = {}
                for key,value in selectors.items():
                    single_opinion[key] = get_element(opinion, *value)

                single_opinion["recommendation"] == True if single_opinion["recommendation"] == "Polecam" else False if single_opinion["recommendation"] == "Nie polecam" else None
                single_opinion["score"] = np.divide(*[float(score.replace(",",".")) for score in single_opinion["score"].split("/")])
                single_opinion["like"] = int(single_opinion["like"])
                single_opinion["dislike"] = int(single_opinion["dislike"])
                single_opinion["description"] = clean_text(single_opinion["description"])
                single_opinion["description-en"] = translator.translate(single_opinion["description"][:500])
                single_opinion["pros-en"] = translator.translate(single_opinion["pros"])
                single_opinion["cons-en"] = translator.translate(single_opinion["cons"])


                all_opinions.append(single_opinion)
            
            try:
                page = get_element(page_dom,"a.pagination__next", "href")
                url = f"https://www.ceneo.pl/{page}"
            except TypeError:
                url = None
            print(url)
        else:
            print(f"There are no opinions about produsct {product_code} code")
    else:
        print("The product does not exist")
    
    if len(all_opinions) > 0:
        if not os.path.exists("./opinions"):
            os.mkdir("./opinions")
        with open(f"./opinions/{product_code}.json", "w", encoding = "UTF-8") as jf:
            json.dumb(all_opinions, jf, indent = 4, ensure_ascii = False)
    
            