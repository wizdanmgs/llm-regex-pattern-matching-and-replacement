from rest_framework.routers import Route, DefaultRouter

from .views import UploadedFileViewSet, NlpQueryViewSet

router = DefaultRouter()
router.register(r"file", UploadedFileViewSet)
router.register(r"nlp", NlpQueryViewSet)

urlpatterns = router.urls
