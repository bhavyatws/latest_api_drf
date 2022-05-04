"""employer_employee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from employer_employee.settings.common import *
from rest_framework_simplejwt import views as jwt_views
from account.views import MyTokenObtainPairView#Customized TokenObtainer
# from employer_employee.settings.production import DEBUG404



urlpatterns = [
    path('admin/', admin.site.urls),
    #django debug toolbar
    path('__debug__/', include('debug_toolbar.urls')),
    #silk (like debug toolbar this tool )
    # path('silk/', include('silk.urls', namespace='silk')),
    # path( "api-auth/", include("rest_framework.urls")),
    #Simple JWT Route
    path("api-auth/", include("rest_framework.urls")),  
    path("api-token/",MyTokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
    #User API
    path('account/',include('account.urls')),
    path('job/',include('job.urls')),
    path('job-assigned/',include('job_assigned.urls')),
    path('notes/',include('notes.urls')),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



