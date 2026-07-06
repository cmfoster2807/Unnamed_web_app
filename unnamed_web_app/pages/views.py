from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def game_detail(request):
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

    recent_reviews = [
        {
            "user": "Alex",
            "rating": "5",
            "text": "Brutal at first, but incredibly satisfying once the combat finally clicks.",
        },
        {
            "user": "Maya",
            "rating": "4.5",
            "text": "One of the cleanest combat systems I have ever played.",
        },
        {
            "user": "Ryan",
            "rating": "2",
            "text": "This game sucks it's too hard.",
        },
    ]

    return render(request, "pages/game_detail.html", {
        "game": game,
        "recent_reviews": recent_reviews,
    })