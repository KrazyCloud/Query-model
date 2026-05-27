from urllib.parse import quote_plus
from datetime import datetime


def generate_social_search_links(
    topic: str,
    keywords: list = None
):

    encoded = quote_plus(topic)
    hashtag = topic.replace(" ", "").upper()
    current_year = datetime.now().year

    return {

        # =================================================
        # 🐦 TWITTER / X
        # =================================================

        "twitter": {

            "exact_phrase": {
                "url":
                    f'https://x.com/search?q="{encoded}"',

                "keywords": []
            },

            "hashtag_phrase": {
                "url":
                    f'https://x.com/search?q=("{encoded}" OR #{hashtag})',

                "keywords": []
            },

            "latest": {
                "url":
                    f'https://x.com/search?q="{encoded}"&f=live',

                "keywords": []
            },

            "verified_accounts": {
                "url":
                    f'https://x.com/search?q="{encoded}" filter:verified',

                "keywords": []
            },

            "viral_posts": {
                "url":
                    f'https://x.com/search?q="{encoded}" min_faves:1000',

                "keywords": []
            },

            "videos_only": {
                "url":
                    f'https://x.com/search?q="{encoded}" filter:videos',

                "keywords": []
            },

            "images_only": {
                "url":
                    f'https://x.com/search?q="{encoded}" filter:images',

                "keywords": []
            },

            "links_only": {
                "url":
                    f'https://x.com/search?q="{encoded}" filter:links',

                "keywords": []
            },

            "hindi_only": {
                "url":
                    f'https://x.com/search?q="{encoded}" lang:hi',

                "keywords": []
            },

            "english_only": {
                "url":
                    f'https://x.com/search?q="{encoded}" lang:en',

                "keywords": []
            },

            "exclude_memes": {
                "url":
                    f'https://x.com/search?q="{encoded}" -meme',

                "keywords": []
            },

            "exclude_replies": {
                "url":
                    f'https://x.com/search?q="{encoded}" -filter:replies',

                "keywords": []
            },

            "replies_only": {
                "url":
                    f'https://x.com/search?q="{encoded}" filter:replies',

                "keywords": []
            },

            "positive_sentiment": {
                "url":
                    f'https://x.com/search?q="{encoded}" :) ',

                "keywords": []
            },

            "negative_sentiment": {
                "url":
                    f'https://x.com/search?q="{encoded}" :( ',

                "keywords": []
            },

            "recent_trend": {
                "url":
                    f'https://x.com/search?q=("{encoded}" OR #{hashtag}) '
                    f'lang:en min_faves:50 since:{current_year}-01-01',

                "keywords": []
            }
        },

        # =================================================
        # 📺 YOUTUBE
        # =================================================

        "youtube": {

            "basic": {
                "url":
                    f'https://www.youtube.com/results?search_query={encoded}',

                "keywords": []
            },

            "exact_phrase": {
                "url":
                    f'https://www.youtube.com/results?search_query="{encoded}"',

                "keywords": []
            },

            "hashtag": {
                "url":
                    f'https://www.youtube.com/results?search_query=%23{hashtag}',

                "keywords": []
            },

            "news": {
                "url":
                    f'https://www.youtube.com/results?search_query={encoded}+news',

                "keywords": []
            },

            "debate": {
                "url":
                    f'https://www.youtube.com/results?search_query={encoded}+debate',

                "keywords": []
            },

            "analysis": {
                "url":
                    f'https://www.youtube.com/results?search_query={encoded}+analysis',

                "keywords": []
            },

            "interview": {
                "url":
                    f'https://www.youtube.com/results?search_query={encoded}+interview',

                "keywords": []
            },

            "podcast": {
                "url":
                    f'https://www.youtube.com/results?search_query={encoded}+podcast',

                "keywords": []
            },

            "shorts": {
                "url":
                    f'https://www.youtube.com/results?search_query={encoded}+shorts',

                "keywords": []
            },

            "live": {
                "url":
                    f'https://www.youtube.com/results?search_query={encoded}+live',

                "keywords": []
            }
        },

        # =================================================
        # 👽 REDDIT
        # =================================================

        "reddit": {

            "exact_phrase": {
                "url":
                    f'https://www.reddit.com/search/?q="{encoded}"',

                "keywords": []
            },

            "new_posts": {
                "url":
                    f'https://www.reddit.com/search/?q="{encoded}"&sort=new',

                "keywords": []
            },

            "top_posts": {
                "url":
                    f'https://www.reddit.com/search/?q="{encoded}"&sort=top',

                "keywords": []
            },

            "comments": {
                "url":
                    f'https://www.reddit.com/search/?q="{encoded}"&type=comment',

                "keywords": []
            },

            "india_discussions": {
                "url":
                    f'https://www.reddit.com/search/?q="{encoded}"+subreddit:india',

                "keywords": []
            },

            "political_discussions": {
                "url":
                    f'https://www.reddit.com/search/?q="{encoded}"+subreddit:politics',

                "keywords": []
            },

            "india_politics": {
                "url":
                    f'https://www.reddit.com/r/india/search/?q="{encoded}"&restrict_sr=1',

                "keywords": []
            },

            "exclude_memes": {
                "url":
                    f'https://www.reddit.com/search/?q="{encoded}"+-meme',

                "keywords": []
            },

            "author_search": {
                "url":
                    f'https://www.reddit.com/search/?q="{encoded}"+author:USERNAME',

                "keywords": []
            },

            "google_strategy": {
                "url":
                    f'https://www.google.com/search?q=site:reddit.com+"{encoded}"',

                "keywords": []
            }
        },

        # =================================================
        # ❓ QUORA
        # =================================================

        "quora": {

            "exact_phrase": {
                "url":
                    f'https://www.quora.com/search?q="{encoded}"',

                "keywords": []
            },

            "politics": {
                "url":
                    f'https://www.quora.com/search?q={encoded}+politics',

                "keywords": []
            },

            "public_opinion": {
                "url":
                    f'https://www.quora.com/search?q={encoded}+public+opinion',

                "keywords": []
            },

            "india_context": {
                "url":
                    f'https://www.quora.com/search?q={encoded}+India',

                "keywords": []
            },

            "questions": {
                "url":
                    f'https://www.quora.com/search?q={encoded}+questions',

                "keywords": []
            },

            "controversy": {
                "url":
                    f'https://www.quora.com/search?q={encoded}+controversy',

                "keywords": []
            },

            "reviews": {
                "url":
                    f'https://www.quora.com/search?q={encoded}+reviews',

                "keywords": []
            },

            "google_strategy": {
                "url":
                    f'https://www.google.com/search?q=site:quora.com+"{encoded}"',

                "keywords": []
            }
        },

        # =================================================
        # 📰 GOOGLE NEWS
        # =================================================

        "google_news": {

            "news": {
                "url":
                    f'https://news.google.com/search?q={encoded}',

                "keywords": []
            },

            "latest": {
                "url":
                    f'https://www.google.com/search?q={encoded}&tbm=nws',

                "keywords": []
            },

            "recent_24h": {
                "url":
                    f'https://www.google.com/search?q={encoded}&tbm=nws&tbs=qdr:d',

                "keywords": []
            },

            "recent_week": {
                "url":
                    f'https://www.google.com/search?q={encoded}&tbm=nws&tbs=qdr:w',

                "keywords": []
            }
        }
    }