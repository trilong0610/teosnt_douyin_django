"""douyin URL Configuration

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
from django.conf import settings
from django.contrib import admin
from douyin import views
from django.conf.urls.static import static
from django.urls import path, include

app_name = 'douyin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home.as_view(), name='upload'),
    path('no_edit/', views.downVideoNoEdit.as_view(), name='no_edit'),
    path('get_code/<str:code>', views.get_code.as_view(), name='get_code'),
    path('create_code/', views.create_code.as_view(), name='create_code'),
    path('check_code/<str:code>', views.check_code.as_view(), name='check_code')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
