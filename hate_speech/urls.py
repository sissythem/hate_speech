from os.path import join, realpath, dirname, abspath
from os import pardir
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from hate_speech import settings
from hate_speech_detection.views import *

schema_view = get_swagger_view(title='Hate-Speech-Detection')

router = routers.DefaultRouter()
# router.register(r'runs', RunView, basename="runs")
# router.register(r'experiments', ExperimentView, basename="experiments")
# router.register(r'experiment-groups', ExperimentGroupView, basename="experiment-groups")
# router.register(r'uploads,', UploadView, basename="uploads")

dir_path = dirname(realpath(__file__))
parent = abspath(join(dir_path, pardir))
yaml_file = join(parent, "static", "schema.yml")

urlpatterns = [
                  url('docs/', TemplateView.as_view(template_name="index.html")),
                  url(r'^admin/', admin.site.urls),
                  url(r'^', include(router.urls))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Hate-Speech-Detection Admin'
admin.site.site_title = "Hate-Speech-Detection"
