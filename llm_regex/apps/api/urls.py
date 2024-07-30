from rest_framework.routers import Route, DefaultRouter

from .views import UploadedFileViewSet

router = DefaultRouter()
router.register(r"file", UploadedFileViewSet)

urlpatterns = router.urls
