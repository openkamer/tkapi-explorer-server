
from django.urls import path
from django.conf.urls import url
from api import views


urlpatterns = [
    path('v1/entity/types/', view=views.get_entity_types),
    path('v1/entities/', view=views.get_entities_by_url),
    path('v1/entity/links/', view=views.get_entity_links),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
