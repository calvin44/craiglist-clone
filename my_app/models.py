from django.db import models

# Create your models here.


class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    # rename the model in django-admin interface
    class Meta:
        verbose_name_plural = 'Searches'

    def __str__(self):
        return '{}'.format(self.search)
