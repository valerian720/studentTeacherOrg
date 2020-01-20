from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect

app_name='schedule'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', lambda request: redirect('login/', permanent=False)),

    path('redir/',views.index,name='index'),
    path('teacher/',views.teacherSc,name='teacherSc'),
    path('student/',views.studentSc,name='studentSc'),
    path('api/',views.api,name='api'),
    # url(r'^login/$', LoginView.as_view(), name='login'),
]