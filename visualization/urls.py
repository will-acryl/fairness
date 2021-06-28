from django.conf.urls import url

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r"^data", views.data, name="data"),
    url(r"^check", views.check, name="check"),
    url(r"^before_chart_data", views.before_chart_data, name="before_chart_data"),
    url(r"^after_chart_data", views.after_chart_data, name="after_chart_data"),
    url(r"^mitigate", views.mitigate, name="mitigate"),
    url(r"^compare", views.compare, name="compare"),
    url(r"^uploadCSV", views.uploadCSV, name="uploadCSV"),
    url(r"^uploadUrlCSV", views.uploadUrlCSV, name="uploadUrlCSV"),
    url(
        r"^select_attribute_option",
        views.select_attribute_option,
        name="select_attribute_option",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
