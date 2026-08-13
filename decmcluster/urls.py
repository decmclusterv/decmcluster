"""
URL configuration for decmcluster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/account/", include("account.urls")),
        path("api/", include("contact.urls")),
        path("api/", include("useful_link.urls")),
        path("api/", include("assessment.urls")),
        path("api/dashboard/", include("dashboard.urls")),
        path("api/", include("report.urls")),
        path("api/", include("response_tracking.urls")),
        path("api/", include("contact_list.urls")),
        path("api/", include("sop.urls")),
        path("api/", include("training.urls")),
        path("api/", include("map.urls")),
        path("api/", include("meeting_minute.urls")),
        path("api/", include("kobo.urls")),
        path("api/", include("evacuation_centre.urls")),
        path("api/", include("displacement.urls")),
        path("api/", include("fivew.urls")),
        path("api/", include("village_assessment.urls")),
        path("api/", include("latest_update.urls")),
        path("api/", include("emergency_alert.urls")),
        path("api/", include("announcement.urls")),
        path("api/", include("archive.urls")),
        path("api/", include("displacement_data.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
