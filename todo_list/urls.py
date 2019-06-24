from django.conf.urls import url
from .views import ItemView, ItemDetailView, ListView, ListDetailView

urlpatterns = [
    url(r'^lists/$', ListView.as_view(), name='list_view'),
    url(r'^lists/(?P<pk>[0-9]+)/$', ListDetailView.as_view(), name='list_detail_view'), 
    url(r'^lists/(?P<list_id>[0-9]+)/items/$', ItemView.as_view(), name='item_view'), 
    url(r'^lists/(?P<list_id>[0-9]+)/items/(?P<pk>[0-9]+)/$', ItemDetailView.as_view(), name='item_detail_view'), 
]
