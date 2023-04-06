from django.urls import path, re_path
from django.conf.urls import include

from mangos.views import mangosClasificacionView

urlpatterns = [
    re_path(r'resultado$', mangosClasificacionView.as_view()),
]