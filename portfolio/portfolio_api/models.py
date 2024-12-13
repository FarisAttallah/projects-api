from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, null=True, blank=True)
    gitHubLink = models.URLField(null=True, blank=True)

    languages = models.ManyToManyField(Language, related_name="projects")
    technologies = models.ManyToManyField(Technology, related_name="projects")
    details = models.JSONField(default=list, blank=True)  # Store details as a list of strings

    def __str__(self):
        return self.title



