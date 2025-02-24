"""
URL configuration for rice_database project.

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
from django.contrib import admin
from django.urls import path, include
from browse import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    
    path('chat/', include('chat.urls')),

    path('index', views.index, name='index_url'),
    path('tools', views.about, name='tools_url'),
    path('browse', views.services, name='Browse_url'),

    path('jbrowse', views.jbrowse, name='jbrowse_url'),
    path('blast', views.blast, name='blast_url'),
    path('blast_run', views.blast_run, name='blast_run_url'),
    path('table_lncRNA', views.table_lncRNA, name='table_lncRNA_url'),
    path('table_lncRNA_run', views.table_lncRNA_run, name='table_lncRNA_run_url'),
    path('download', views.download, name='download_url'),
    path('statistics1', views.statistics1, name='statistics1_url'),
    path('statistics2', views.statistics2, name='statistics2_url'),
    path('documentation', views.documentation, name='documentation_url'),
    path('submit', views.submit, name='submit_url'),
    path('contact', views.contact, name='contact_url'),
]





