from django.db import models

class PGNFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='pgn_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name