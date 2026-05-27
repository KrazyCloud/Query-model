def generate_social_search_links():

    return {

        # =================================================
        # 🐦 TWITTER / X
        # =================================================

        "twitter": {

            "exact_phrase": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\"",

                "keywords": []
            },

            "hashtag_phrase": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "({query})",

                "keywords": []
            },

            "latest": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\"",

                "extra":
                    "&f=live",

                "keywords": []
            },

            "verified_accounts": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" filter:verified",

                "keywords": []
            },

            "viral_posts": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" min_faves:1000",

                "keywords": []
            },

            "videos_only": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" filter:videos",

                "keywords": []
            },

            "images_only": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" filter:images",

                "keywords": []
            },

            "links_only": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" filter:links",

                "keywords": []
            },

            "hindi_only": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" lang:hi",

                "keywords": []
            },

            "english_only": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" lang:en",

                "keywords": []
            },

            "exclude_memes": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" -meme",

                "keywords": []
            },

            "exclude_replies": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" -filter:replies",

                "keywords": []
            },

            "replies_only": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" filter:replies",

                "keywords": []
            },

            "positive_sentiment": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" :)",

                "keywords": []
            },

            "negative_sentiment": {
                "base_url":
                    "https://x.com/search?q=",

                "template":
                    "\"{query}\" :(",

                "keywords": []
            }
        },

        # =================================================
        # 📺 YOUTUBE
        # =================================================

        "youtube": {

            "basic": {
                "base_url":
                    "https://www.youtube.com/results?search_query=",

                "template":
                    "{query}",

                "keywords": []
            },

            "news": {
                "base_url":
                    "https://www.youtube.com/results?search_query=",

                "template":
                    "{query} news",

                "keywords": []
            },

            "debate": {
                "base_url":
                    "https://www.youtube.com/results?search_query=",

                "template":
                    "{query} debate",

                "keywords": []
            },

            "analysis": {
                "base_url":
                    "https://www.youtube.com/results?search_query=",

                "template":
                    "{query} analysis",

                "keywords": []
            },

            "shorts": {
                "base_url":
                    "https://www.youtube.com/results?search_query=",

                "template":
                    "{query} shorts",

                "keywords": []
            },

            "live": {
                "base_url":
                    "https://www.youtube.com/results?search_query=",

                "template":
                    "{query} live",

                "keywords": []
            }
        },

        # =================================================
        # 👽 REDDIT
        # =================================================

        "reddit": {

            "exact_phrase": {
                "base_url":
                    "https://www.reddit.com/search/?q=",

                "template":
                    "\"{query}\"",

                "keywords": []
            },

            "top_posts": {
                "base_url":
                    "https://www.reddit.com/search/?q=",

                "template":
                    "\"{query}\"",

                "extra":
                    "&sort=top",

                "keywords": []
            },

            "new_posts": {
                "base_url":
                    "https://www.reddit.com/search/?q=",

                "template":
                    "\"{query}\"",

                "extra":
                    "&sort=new",

                "keywords": []
            },

            "india_discussions": {
                "base_url":
                    "https://www.reddit.com/search/?q=",

                "template":
                    "\"{query}\" subreddit:india",

                "keywords": []
            }
        },

        # =================================================
        # ❓ QUORA
        # =================================================

        "quora": {

            "exact_phrase": {
                "base_url":
                    "https://www.quora.com/search?q=",

                "template":
                    "\"{query}\"",

                "keywords": []
            },

            "politics": {
                "base_url":
                    "https://www.quora.com/search?q=",

                "template":
                    "{query} politics",

                "keywords": []
            },

            "public_opinion": {
                "base_url":
                    "https://www.quora.com/search?q=",

                "template":
                    "{query} public opinion",

                "keywords": []
            }
        }
    }