from django.db import models
from search.configurations import N


class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return f'"id": {self.id}, "title": "{self.title}", “content”: “{self.content}”'

