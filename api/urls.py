
from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^v1/entities/$', view=views.get_entities),
    url(r'^v1/entity/$', view=views.get_entity),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
