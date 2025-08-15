from django import forms

class PgnUploadForm(forms.Form):
    pgn_file = forms.FileField(label="Upload PGN file")
