# TODO Pintrest, Instagram be added

def generate_social_search_links():

    return {

        # =================================================
        # 🐦 TWITTER / X
        # =================================================

        "twitter": {

            "exact_phrase": {
                "filters":
                    "\"{keyword}\"",

                "keywords": []
            },

            "hashtag_phrase": {
                "filters":
                    "({keyword})",

                "keywords": []
            },

            "latest": {
                "filters":
                    "\"{keyword}\"",

                "extra":
                    "&f=live",

                "keywords": []
            },

            "verified_accounts": {
                "filters":
                    "\"{keyword}\" filter:verified",

                "keywords": []
            },

            "viral_posts": {
                "filters":
                    "\"{keyword}\" min_faves:1000",

                "keywords": []
            },

            "videos_only": {
                "filters":
                    "\"{keyword}\" filter:videos",

                "keywords": []
            },

            "images_only": {
                "filters":
                    "\"{keyword}\" filter:images",

                "keywords": []
            },

            "links_only": {
                "filters":
                    "\"{keyword}\" filter:links",

                "keywords": []
            },

            "hindi_only": {
                "filters":
                    "\"{keyword}\" lang:hi",

                "keywords": []
            },

            "english_only": {
                "filters":
                    "\"{keyword}\" lang:en",

                "keywords": []
            },

            "exclude_memes": {
                "filters":
                    "\"{keyword}\" -meme",

                "keywords": []
            },

            "exclude_replies": {
                "filters":
                    "\"{keyword}\" -filter:replies",

                "keywords": []
            },

            "replies_only": {
                "filters":
                    "\"{keyword}\" filter:replies",

                "keywords": []
            },
        },

        # =================================================
        # 📺 YOUTUBE
        # =================================================

        "youtube": {

            "basic": {
                "filters":
                    "{keyword}",

                "keywords": []
            },

            "news": {
                "filters":
                    "{keyword} news",

                "keywords": []
            },

            "debate": {
                "filters":
                    "{keyword} debate",

                "keywords": []
            },

            "analysis": {
                "filters":
                    "{keyword} analysis",

                "keywords": []
            },

            "shorts": {
                "filters":
                    "{keyword} shorts",

                "keywords": []
            },

            "live": {
                "filters":
                    "{keyword} live",

                "keywords": []
            }
        },

        # =================================================
        # 👽 REDDIT
        # =================================================

        "reddit": {

            "exact_phrase": {
                "filters":
                    "\"{keyword}\"",

                "keywords": []
            },

            "top_posts": {
                "filters":
                    "\"{keyword}\"",

                "extra":
                    "&sort=top",

                "keywords": []
            },

            "new_posts": {
                "filters":
                    "\"{keyword}\"",

                "extra":
                    "&sort=new",

                "keywords": []
            },

            "india_discussions": {
                "filters":
                    "\"{keyword}\" subreddit:india",

                "keywords": []
            }
        },

        # =================================================
        # ❓ QUORA
        # =================================================

        "quora": {

            "exact_phrase": {
                "filters":
                    "\"{keyword}\"",

                "keywords": []
            },

            "politics": {
                "filters":
                    "{keyword} politics",

                "keywords": []
            },

            "public_opinion": {
                "filters":
                    "{keyword} public opinion",

                "keywords": []
            }
        }
    }