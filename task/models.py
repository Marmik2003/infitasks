from django.db import models

class TaskItem(models.Model):
    item = models.CharField(max_length=150, blank=False, null=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.item