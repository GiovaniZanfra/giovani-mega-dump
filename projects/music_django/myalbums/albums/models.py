from django.db import models

class Album(models.Model):
    name = models.CharField(max_length=255)  # Assuming each album has a name
    track_score = models.FloatField()
    album_cover = models.URLField(max_length=1024)
    number_of_tracks = models.IntegerField()
    horrible_ratio = models.FloatField()
    bad_ratio = models.FloatField()
    ok_ratio = models.FloatField()
    like_ratio = models.FloatField()
    love_ratio = models.FloatField()
    favs_ratio = models.FloatField()
    gut_feeling = models.FloatField()
    calculated_score = models.FloatField()
    unified_score = models.FloatField()

    def __str__(self):
        return self.name

class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    name = models.CharField(max_length=255)
    score = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.album.name}"
