from venv import logger
from rest_framework import viewsets
from .models import Language, Technology, Project
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from django.http import JsonResponse

from .serializers import (
    LanguageSerializer,
    TechnologySerializer,
    ProjectSerializer
)

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ProjectHandler(View):
    def post(self, request):
        logger.info("Request received")

        try:
            data = json.loads(request.body)

            # Retrieve or create Languages
            language_objects = []
            for language_data in data.get('languages', []):
                # Assuming Language model has fields 'id', 'name', and 'icon'
                language, created = Language.objects.get_or_create(
                    name=language_data['name']
                )
                # You may want to store the icon if required
                language.icon = language_data.get('icon', '')
                language.save()
                language_objects.append(language)

            # Retrieve or create Technologies
            technology_objects = []
            for technology_data in data.get('technologies', []):
                # Assuming Technology model has fields 'id', 'name', 'description', and 'icon'
                technology, created = Technology.objects.get_or_create(
                    name=technology_data['name']
                )
                # You may want to store the description and icon if required
                technology.description = technology_data.get('description', '')
                technology.icon = technology_data.get('icon', '')
                technology.save()
                technology_objects.append(technology)

            # Create the Project
            project = Project.objects.create(
                title=data['title'],
                description=data['description'],
                location=data.get('location'),
                gitHubLink=data.get('gitHubLink'),
            )

            # Store project details
            # Assuming Project model has a 'details' field (TextField, ArrayField, or similar)
            project.details = data.get('details', [])
            project.save()

            # Associate Languages and Technologies
            project.languages.set(language_objects)
            project.technologies.set(technology_objects)

            return JsonResponse({"message": "Project created successfully!", "project_id": project.id}, status=201)

        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
