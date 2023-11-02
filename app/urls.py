from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    # path('to_docor', views.doctor, name='doctor'),
    # path('to_translator', views.trans, name='trans'),
    # path('rule', views.rule, name='rule'),
    # path('error', views.error, name='error'),
]
