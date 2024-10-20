from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from mailings.views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("mailings/", include("mailings.urls", namespace="mailings")),
    path("users/", include("users.urls", namespace="users")),
    path("blogs/", include("blogs.urls", namespace="blogs")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
