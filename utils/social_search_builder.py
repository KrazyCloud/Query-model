# TODO Pintrest, Instagram be added

# =====================================================
# BASE URLS (single source of truth per platform)
# =====================================================

TWITTER_BASE = "https://x.com/search?q="
YOUTUBE_BASE = "https://www.youtube.com/results?search_query="
REDDIT_BASE = "https://www.reddit.com/search/?q="
QUORA_BASE = "https://www.quora.com/search?q="
PINTEREST_PINS_BASE = "https://www.pinterest.com/search/pins/?q="
PINTEREST_BOARDS_BASE = "https://www.pinterest.com/search/boards/?q="
PINTEREST_USERS_BASE = "https://www.pinterest.com/search/users/?q="
INSTAGRAM_HASHTAG_BASE = "https://www.instagram.com/explore/tags/"
GOOGLE_SITE_BASE = "https://www.google.com/search?q="


def generate_social_search_links():

    return {

        # =================================================
        # 🐦 TWITTER / X
        # =================================================

        "twitter": {

            "exact_phrase": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\"",

                "keywords": []
            },

            "hashtag_phrase": {
                "filters":
                    TWITTER_BASE + "(\"{keyword}\" OR #{keyword})",

                "keywords": []
            },

            "latest": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\"&f=live",

                "keywords": []
            },

            "verified_accounts": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\" filter:verified",

                "keywords": []
            },

            "viral_posts": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\" min_faves:1000",

                "keywords": []
            },

            "videos_only": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\" filter:videos",

                "keywords": []
            },

            "images_only": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\" filter:images",

                "keywords": []
            },

            "links_only": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\" filter:links",

                "keywords": []
            },

            "hindi_only": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\" lang:hi",

                "keywords": []
            },

            "english_only": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\" lang:en",

                "keywords": []
            },

            "exclude_memes": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\" -meme",

                "keywords": []
            },

            "exclude_replies": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\" -filter:replies",

                "keywords": []
            },

            "replies_only": {
                "filters":
                    TWITTER_BASE + "\"{keyword}\" filter:replies",

                "keywords": []
            },
        },

        # =================================================
        # 📺 YOUTUBE
        # =================================================

        "youtube": {

            "basic": {
                "filters":
                    YOUTUBE_BASE + "{keyword}",

                "keywords": []
            },

            "news": {
                "filters":
                    YOUTUBE_BASE + "{keyword} news",

                "keywords": []
            },

            "debate": {
                "filters":
                    YOUTUBE_BASE + "{keyword} debate",

                "keywords": []
            },

            "analysis": {
                "filters":
                    YOUTUBE_BASE + "{keyword} analysis",

                "keywords": []
            },

            "shorts": {
                "filters":
                    YOUTUBE_BASE + "{keyword} shorts",

                "keywords": []
            },

            "live": {
                "filters":
                    YOUTUBE_BASE + "{keyword} live",

                "keywords": []
            }
        },

        # =================================================
        # 👽 REDDIT
        # =================================================

        "reddit": {

            "exact_phrase": {
                "filters":
                    REDDIT_BASE + "\"{keyword}\"",

                "keywords": []
            },

            "top_posts": {
                "filters":
                    REDDIT_BASE + "\"{keyword}\"&sort=top",

                "keywords": []
            },

            "new_posts": {
                "filters":
                    REDDIT_BASE + "\"{keyword}\"&sort=new",

                "keywords": []
            },

            "india_discussions": {
                "filters":
                    REDDIT_BASE + "\"{keyword}\" subreddit:india",

                "keywords": []
            }
        },

        # =================================================
        # ❓ QUORA
        # =================================================

        "quora": {

            "exact_phrase": {
                "filters":
                    QUORA_BASE + "\"{keyword}\"",

                "keywords": []
            },

            "politics": {
                "filters":
                    QUORA_BASE + "{keyword} politics",

                "keywords": []
            },

            "public_opinion": {
                "filters":
                    QUORA_BASE + "{keyword} public opinion",

                "keywords": []
            }
        },

        # =================================================
        # 📌 PINTEREST
        # =================================================
        # Pinterest search has NO boolean support (no OR, no
        # exact-phrase quoting, no exclude). It's pure semantic
        # ranking on whatever text follows ?q=. {keyword} is
        # substituted as-is (URL-encoded at call time).

        "pinterest": {

            "pins": {
                "filters":
                    PINTEREST_PINS_BASE + "{keyword}",

                "keywords": []
            },

            "boards": {
                "filters":
                    PINTEREST_BOARDS_BASE + "{keyword}",

                "keywords": []
            },

            "users": {
                "filters":
                    PINTEREST_USERS_BASE + "{keyword}",

                "keywords": []
            },

            "idea_pins": {
                "filters":
                    PINTEREST_PINS_BASE + "{keyword} ideas",

                "keywords": []
            },

            "diy": {
                "filters":
                    PINTEREST_PINS_BASE + "{keyword} diy",

                "keywords": []
            }
        },

        # =================================================
        # 📷 INSTAGRAM
        # =================================================
        # Instagram has NO public keyword-search page (the real
        # search endpoint requires an authenticated session).
        # The only unauthenticated, crawlable surface is a
        # hashtag page, which means {keyword} MUST be a single
        # word with no spaces/punctuation for these to resolve
        # (e.g. "COCKROACHJANTAPARTY", not "Cockroach Janta
        # Party"). For multi-word phrases, use the google_site
        # fallback instead, same pattern as the Reddit/Quora
        # fallback in your doc.

        "instagram": {

            "hashtag": {
                "filters":
                    INSTAGRAM_HASHTAG_BASE + "{keyword}/",

                "keywords": []
            },

            "google_site_fallback": {
                "filters":
                    GOOGLE_SITE_BASE + "site:instagram.com+\"{keyword}\"",

                "keywords": []
            }
        }
    }