from django.db import models 
from django.contrib.auth.models import User


# Base model for the game database
class Game(models.Model):
    title = models.CharField(max_length=200)
    igdb_id = models.IntegerField(unique=True, null=True, blank=True)
    cover_image_url = models.URLField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    platform = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank = True)
    genre = models.CharField(max_length = 100, blank = True)
    
    def __str__(self):
        return self.title

# Creates the review data structure
RATING_CHOICES = [(x / 2, str(x / 2)) for x in range(0,21)]
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Attaches a one to many relationship with user - will delete all reviews if user is deleted
    game = models.ForeignKey(Game, on_delete=models.CASCADE) # Attaches a one to many relationship with game - will delete all reviews if game is deleted
    rating = models.DecimalField( # Gives the players a choice between scores 0-10 including .5 stars
        max_digits = 3,
        decimal_places = 1,
        choices = RATING_CHOICES,
    )
    review_text = models.TextField(blank = True) # Text body for review
    date_played = models.DateField(null = True, blank = True) # Allows user to set time played manually
    created_at = models.DateTimeField(auto_now_add = True) # Auto-populates with date/time review is published

    def __str__(self): # What the model will print by default when called
        return f"{self.user.username} - {self.game.title} ({self.rating})"
    

# Allows users to customize profiles beyond django defaults
class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete = models.CASCADE)  # user profile attached to users - will delete profile if user is deleted
    bio = models.TextField(blank = True) # Text box for bio
    avatar = models.ImageField(upload_to = 'avatars/', blank = True, null = True) # Profile picture file upload
    favorite_game = models.ForeignKey( # Game of all time field
        Game, null = True, blank = True,
        on_delete = models.SET_NULL,
        related_name = '+'
    ) 

# Separate model for selecting favorite games to be displayed on profile page
class TopGames(models.Model): 
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'favorites')
    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    position = models.PositiveSmallIntegerField() # 1-4

    class Meta:
        unique_together = ('profile', 'position')
        ordering = ['position']
        verbose_name = 'Top Games'
        verbose_name_plural = 'Top Games'

# Model for creating and managing lists 
class GameList(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='lists') # Many to one relationship to user
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.profile.user.username}"


# Creates a model with the information specifically for an entry to a game list
class GameListEntry(models.Model):
    # Many to one relationship with the list and the game
    game_list = models.ForeignKey(GameList, on_delete=models.CASCADE, related_name='entries')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    position = models.PositiveIntegerField()
    note = models.CharField(max_length=300, blank=True)

    class Meta: # Allows for display settings and metadata specifications
        unique_together = ('game_list', 'position')
        ordering = ['position']

    def __str__(self):
        return f"{self.position}. {self.game.title}"