from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.db.models import Q
from .igdb import search_games, search_developers, sync_game
from django.shortcuts import render, get_object_or_404, redirect



def search(request):
    """Search against IGDB (games, developers) or local users, based on selected type."""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'games')

    game_results = []
    developer_results = []
    user_results = []

    if query:
        if search_type == 'developers':
            developer_results = search_developers(query)
        elif search_type == 'users':
            user_results = User.objects.filter(
                Q(username__icontains=query) | Q(email__icontains=query)
            ).select_related('profile')[:20]
        else:  # default: games
            game_results = search_games(query)

    return render(request, 'games/search.html', {
        'game_results': game_results,
        'developer_results': developer_results,
        'user_results': user_results,
        'query': query,
        'search_type': search_type,
    })

def game_detail(request, igdb_id):
    """Serve from local DB if exists, otherwise sync from IGDB first."""
    try:
        game = Game.objects.get(igdb_id=igdb_id)
    except Game.DoesNotExist:
        game = sync_game(igdb_id)

    return render(request, 'games/game_detail.html', {'game': game})

def developer_detail(request, igdb_id):
    """Serve from local DB if exists, otherwise sync from IGDB first."""
    from .models import Developer
    from .igdb import sync_developer

    try:
        developer = Developer.objects.get(igdb_id=igdb_id)
    except Developer.DoesNotExist:
        developer = sync_developer(igdb_id)

    return render(request, 'games/developer_detail.html', {'developer': developer})\

def profile_detail(request, username):
    """Display a user's profile page."""
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile  # your OneToOneField from Profile -> User

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'is_following': (
            request.user.is_authenticated
            and request.user.profile.is_following(profile_user)
        ),
    }
    return render(request, 'games/profile_detail.html', context)

@login_required
@require_POST
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    profile = request.user.profile

    if profile.is_following(target):
        profile.unfollow(target)
    else:
        profile.follow(target)

    return redirect('profile_detail', username=username)