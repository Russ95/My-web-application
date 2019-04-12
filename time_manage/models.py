from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Event(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)  #the user posting this twitter
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    #category = models.TextField()

    @property
    def get_html_url(self):
        url = reverse('time_manage:event_edit', args=(self.id,))
        # url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
