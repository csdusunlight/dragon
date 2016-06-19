from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'wafuli_admin.views.index', name='admin_index'),
    url(r'^indexpage/$', 'wafuli_admin.views.get_admin_index_page', name='get_admin_index_page'),
    url(r'^admin_return', 'wafuli_admin.views.admin_return', name='admin_return'),
    url(r'^returnpage/$', 'wafuli_admin.views.get_admin_return_page', name='get_admin_return_page'),
    url(r'^admin_user/$', 'wafuli_admin.views.admin_user', name='admin_user'),
    url(r'^userpage/$', 'wafuli_admin.views.get_admin_user_page', name='get_admin_user_page'),
    url(r'^admin_withdraw/$', 'wafuli_admin.views.admin_withdraw', name='admin_withdraw'),
    url(r'^withpage/$', 'wafuli_admin.views.get_admin_with_page', name='get_admin_with_page'),
    url(r'^admin_score$', 'wafuli_admin.views.admin_score', name='admin_score'),
    url(r'^scorepage/$', 'wafuli_admin.views.get_admin_score_page', name='get_admin_score_page'),
    url(r'^admin_recommend_return', 'wafuli_admin.activity.admin_recommend_return', name='admin_recommend_return'),
    url(r'^return_recommend_page/$', 'wafuli_admin.activity.get_admin_recommend_return_page', name='get_admin_recommend_return_page'),
]