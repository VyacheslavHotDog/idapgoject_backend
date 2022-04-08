from rest_framework.routers import DefaultRouter
from app.views import PhotosViewSet

router = DefaultRouter()
router.register('images', PhotosViewSet, basename='image')
