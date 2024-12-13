from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LanguageViewSet,
    TechnologyViewSet,
    ProjectViewSet,
    ProjectHandler
)

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'technologies', TechnologyViewSet)
router.register(r'projects', ProjectViewSet)


urlpatterns = [
   path('api/', include(router.urls)),
   path('project/', ProjectHandler.as_view(), name='create_project_with_details'),

]
