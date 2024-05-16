"""
URL configuration for kks_reestr_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('/ajax/get-objects', views.get_objects, name='get-objects'),
    path('/ajax/get-sector-2', views.GetSector2View.as_view(), name='get-sector-2'),
    path('/ajax/get-sector-3', views.GetSector3View.as_view(), name='get-sector-3'),
    path('/ajax/get-sector-4', views.GetSector4View.as_view(), name='get-sector-4'),
    path('/ajax/get-type-doc', views.GetTypeDocView.as_view(), name='get-type-doc'),
    path('/ajax/get-sector-5', views.GetSector5View.as_view(), name='get-sector-5'),
    path('/ajax/get-sector-6', views.GetSector6View.as_view(), name='get-sector-6'),
    path('/ajax/get-sector-6-1', views.GetSector61View.as_view(), name='get-sector-6-1'),
    path('/ajax/get-sector-7', views.GetSector7View.as_view(), name='get-sector-7'),
    path('/ajax/get-sector-8', views.GetSector8View.as_view(), name='get-sector-8'),
    path('/ajax/get-sector-9', views.GetSector9View.as_view(), name='get-sector-9'),
    # path('admin/', admin.site.urls),
]
