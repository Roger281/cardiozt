from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^home$', views.list_models, name='home'),
    url(r'^home/historial$', views.hc, name='historialc'),
    url(r'^home/resultados/(?P<pk>\d+)/$', views.resultados, name='resultados'),
    url(r'^cerrar/$', logout, {'next_page': '/'}, name="user-logout"),
    url(r'^clear/$', views.clear_data, name='cleat-data'),
    url(r'^perfil/$', views.perfil_lipidico, name='perfil'),
    url(r'^update_file/$', views.update_file, name='update-file'),
    url(r'^home/models/$', views.list_models, name='list-models'),
    url(r'^home/model/(?P<id_model>\d+)/$', views.train_model, name='model'),
    url(r'^home/create_model/(?P<id_data>\d+)/$', views.create_model, name='create-model'),
    url(r'^home/data/$', views.list_data, name='list-data'),
    url(r'^home/prediction/(?P<id_model>\d+)/$', views.prediction, name='prediction'),
    url(r'^sendemail/$', views.send_email, name='send-email'),

]
