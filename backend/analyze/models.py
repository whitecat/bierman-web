from django.db import models

class Component(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    file = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    lineno = models.IntegerField()
    docstring = models.TextField(blank=True, null=True)
    parameters = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.type}: {self.name} ({self.file}:{self.lineno})"

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "Components"

class Question(models.Model):
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=32)
    component = models.CharField(max_length=255)
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.difficulty.capitalize()} Q: {self.question[:40]}..."

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
