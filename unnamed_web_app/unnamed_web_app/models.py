from django.db import models 
from django.contrib.auth.models import User

RATING_CHOICES = [(x / 2, str(x / 2)) for x in range(0,21)]
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits = 3,
        decimal_places = 1,
        choices = RATING_CHOICES,
    )
    review_text = models.TextField(blank = True)
    date_played = models.DateField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.rating})"
    

    