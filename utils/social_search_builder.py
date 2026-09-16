
# TODO Pinterest, Instagram be added

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


# =====================================================
# FILTER CONFIGURATION HELPER
# =====================================================

def create_filter(url):
    return {
        "filters": url,
        "keywords": [],
        "active_filter": False
    }


# =====================================================
# SOCIAL SEARCH LINKS
# =====================================================

def generate_social_search_links():

    return {

        # =================================================
        # TWITTER / X
        # =================================================

        "twitter": {

            "exact_phrase": create_filter(
                TWITTER_BASE + '"{keyword}"'
            ),

            "hashtag_phrase": create_filter(
                TWITTER_BASE + '("{keyword}" OR #{keyword})'
            ),

            "latest": create_filter(
                TWITTER_BASE + '"{keyword}"&f=live'
            ),

            "verified_accounts": create_filter(
                TWITTER_BASE + '"{keyword}" filter:verified'
            ),

            "viral_posts": create_filter(
                TWITTER_BASE + '"{keyword}" min_faves:1000'
            ),

            "videos_only": create_filter(
                TWITTER_BASE + '"{keyword}" filter:videos'
            ),

            "images_only": create_filter(
                TWITTER_BASE + '"{keyword}" filter:images'
            ),

            "links_only": create_filter(
                TWITTER_BASE + '"{keyword}" filter:links'
            ),

            "hindi_only": create_filter(
                TWITTER_BASE + '"{keyword}" lang:hi'
            ),

            "english_only": create_filter(
                TWITTER_BASE + '"{keyword}" lang:en'
            ),

            "exclude_memes": create_filter(
                TWITTER_BASE + '"{keyword}" -meme'
            ),

            "exclude_replies": create_filter(
                TWITTER_BASE + '"{keyword}" -filter:replies'
            ),

            "replies_only": create_filter(
                TWITTER_BASE + '"{keyword}" filter:replies'
            ),
        },

        # =================================================
        # YOUTUBE
        # =================================================

        "youtube": {

            "basic": create_filter(
                YOUTUBE_BASE + "{keyword}"
            ),

            "news": create_filter(
                YOUTUBE_BASE + "{keyword} news"
            ),

            "debate": create_filter(
                YOUTUBE_BASE + "{keyword} debate"
            ),

            "analysis": create_filter(
                YOUTUBE_BASE + "{keyword} analysis"
            ),

            "shorts": create_filter(
                YOUTUBE_BASE + "{keyword} shorts"
            ),

            "live": create_filter(
                YOUTUBE_BASE + "{keyword} live"
            ),
        },

        # =================================================
        # REDDIT
        # =================================================

        "reddit": {

            "exact_phrase": create_filter(
                REDDIT_BASE + '"{keyword}"'
            ),

            "top_posts": create_filter(
                REDDIT_BASE + '"{keyword}"&sort=top'
            ),

            "new_posts": create_filter(
                REDDIT_BASE + '"{keyword}"&sort=new'
            ),

            "india_discussions": create_filter(
                REDDIT_BASE + '"{keyword}" subreddit:india'
            ),
        },

        # =================================================
        # QUORA
        # =================================================

        "quora": {

            "exact_phrase": create_filter(
                QUORA_BASE + '"{keyword}"'
            ),

            "politics": create_filter(
                QUORA_BASE + "{keyword} politics"
            ),

            "public_opinion": create_filter(
                QUORA_BASE + "{keyword} public opinion"
            ),
        },

        # =================================================
        # PINTEREST
        # =================================================

        "pinterest": {

            "pins": create_filter(
                PINTEREST_PINS_BASE + "{keyword}"
            ),

            "boards": create_filter(
                PINTEREST_BOARDS_BASE + "{keyword}"
            ),

            "users": create_filter(
                PINTEREST_USERS_BASE + "{keyword}"
            ),

            "idea_pins": create_filter(
                PINTEREST_PINS_BASE + "{keyword} ideas"
            ),

            "diy": create_filter(
                PINTEREST_PINS_BASE + "{keyword} diy"
            ),
        },

        # =================================================
        # INSTAGRAM
        # =================================================

        "instagram": {

            "hashtag": create_filter(
                INSTAGRAM_HASHTAG_BASE + "{keyword}/"
            ),

            "google_site_fallback": create_filter(
                GOOGLE_SITE_BASE + 'site:instagram.com+"{keyword}"'
            ),
        },
    }