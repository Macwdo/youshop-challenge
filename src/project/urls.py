from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler403, handler404

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include('app.urls')),
]

handler403 = 'app.views.handler403'
handler404 = 'app.views.handler404'


