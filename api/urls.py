
from django.urls import path
from api import views


urlpatterns = [
    path('v1/entity/types/', view=views.get_entity_types),
    path('v1/entities/<str:type>/', view=views.get_entities_by_type),
    path('v1/entities/', view=views.get_entities_by_url),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
