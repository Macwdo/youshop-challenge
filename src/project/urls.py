from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler403, handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]

handler403 = 'app.views.handler403'
handler404 = 'app.views.handler404'


