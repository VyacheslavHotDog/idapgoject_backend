from django.db import models
from config.settings import UPLOAD_TO


class Photo(models.Model):
    name = models.CharField(max_length=300, null=True)
    url = models.CharField(max_length=1000, null=True)
    picture = models.FileField(upload_to=UPLOAD_TO)
    width = models.IntegerField()
    height = models.IntegerField()
    parent_picture = models.IntegerField(null=True)

    def to_json(self):

        res = {"id": self.id,
               "name": self.name,
               "url": self.url,
               "picture": "http://localhost:8000/m/" + str(self.picture),
               "width": self.width,
               "height": self.height,
               "parent_picture": self.parent_picture,
               }
        return res



