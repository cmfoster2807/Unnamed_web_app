from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def game_detail(request):
    selected_sort = request.GET.get("sort", "popular")
    valid_sorts = {"popular", "new", "trending", "controversial"}
    if selected_sort not in valid_sorts:
        selected_sort = "popular"

    game = {
        "title": "Sekiro: Shadows Die Twice",
        "year": "2019",
        "developer": "FromSoftware",
        "publisher": "Activision",
        "genres": ["Action Adventure", "Soulslike", "Single Player"],
        "rating": "4.8",
        "logs": "2.1k",
        "reviews": "642",
        "description": "A challenging action-adventure game focused on precision combat, exploration, and mastery.",
    }

    reviews = [
        {
            "user": "Alex",
            "initial": "A",
            "rating": "5",
            "text": "Brutal at first, but incredibly satisfying once the combat finally clicks. Every boss feels like a conversation you have to learn instead of a wall you have to break.",
            "likes": "248",
            "dislikes": "12",
            "reply_count": "23",
            "new_score": 2,
            "trend_score": 86,
            "controversy_score": 31,
            "replies": [
                {
                    "user": "Nina",
                    "initial": "N",
                    "text": "blah blah blah",
                },
                {
                    "user": "Owen",
                    "initial": "O",
                    "text": "blah blah blah",
                },
            ],
        },
        {
            "user": "Maya",
            "initial": "M",
            "rating": "4.5",
            "text": "One of the cleanest combat systems I have ever played.",
            "likes": "191",
            "dislikes": "9",
            "reply_count": "14",
            "new_score": 3,
            "trend_score": 94,
            "controversy_score": 24,
            "replies": [
                {
                    "user": "Jules",
                    "initial": "J",
                    "text": "blah blah blah",
                },
            ],
        },
        {
            "user": "Ryan",
            "rating": "2",
            "initial": "R",
            "text": "This game sucks it's too hard.",
            "likes": "42",
            "dislikes": "118",
            "reply_count": "37",
            "new_score": 1,
            "trend_score": 58,
            "controversy_score": 96,
            "replies": [
                {
                    "user": "Tessa",
                    "initial": "T",
                    "text": "blah blah blah",
                },
                {
                    "user": "Cam",
                    "initial": "C",
                    "text": "blah blah blah",
                },
            ],
        },
    ]

    sorters = {
        "popular": lambda review: int(review["likes"]) - int(review["dislikes"]),
        "new": lambda review: review["new_score"],
        "trending": lambda review: review["trend_score"],
        "controversial": lambda review: review["controversy_score"],
    }
    reviews = sorted(reviews, key=sorters[selected_sort], reverse=True)

    review_sort_options = [
        {"value": "popular", "label": "Popular", "selected": selected_sort == "popular"},
        {"value": "new", "label": "New", "selected": selected_sort == "new"},
        {"value": "trending", "label": "Trending", "selected": selected_sort == "trending"},
        {"value": "controversial", "label": "Controversial", "selected": selected_sort == "controversial"},
    ]

    popular_lists = [
        {
            "title": "Games That Demand Perfect Timing",
            "author": "Maya",
            "likes": "428",
            "game_count": "24",
            "covers": ["Sekiro", "Elden Ring", "Sifu", "Lies of P"],
        },
        {
            "title": "The Hardest Games I Actually Finished",
            "author": "Alex",
            "likes": "317",
            "game_count": "18",
            "covers": ["Sekiro", "Bloodborne", "Cuphead", "Celeste"],
        },
        {
            "title": "Essential Samurai Games",
            "author": "Jordan",
            "likes": "186",
            "game_count": "12",
            "covers": ["Sekiro", "Ghost", "Nioh 2", "Ishin"],
        },
        {
            "title": "Boss Fights I Still Think About",
            "author": "Nina",
            "likes": "154",
            "game_count": "31",
            "covers": ["Sekiro", "Hades", "Hollow Knight", "God of War"],
        },
    ]

    return render(request, "pages/game_detail.html", {
        "game": game,
        "reviews": reviews,
        "review_sort_options": review_sort_options,
        "popular_lists": popular_lists,
    })
