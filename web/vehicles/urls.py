from rest_framework import routers

from vehicles.views import CarsViewSet

router = routers.SimpleRouter()
router.register('cars', CarsViewSet, basename='cars')
urlpatterns = router.urls
