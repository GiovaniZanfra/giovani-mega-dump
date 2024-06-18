from django import forms
from .models import Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'track_score', 'album_cover', 'number_of_tracks', 'horrible_ratio', 'bad_ratio', 'ok_ratio', 'like_ratio', 'love_ratio', 'favs_ratio', 'gut_feeling', 'calculated_score', 'unified_score']
