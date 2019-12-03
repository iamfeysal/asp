import uuid

from django.db import models
from team.models import Team


# Create your models here.
class RequestGame(models.Model):
    requesting_team_id = models.ForeignKey(Team, related_name="requestgames", on_delete=models.CASCADE)
    target_team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order_id)
