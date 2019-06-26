from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from mysite.core import views as core_views

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^uploads/query/$', core_views.query_upload, name='query_upload'),
    url(r'^uploads/database/$', core_views.database_upload, name='database_upload'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^uploaded/$', core_views.uploaded_query, name='uploaded'),
    url(r'^uploaded/(?P<filename>.+)/$', core_views.download, name='download'),
    url(r'^result/$', core_views.user_result, name='result'),
    url(r'^result/(?P<filename>.+)/$', core_views.download_result, name='download_result'),
    #url(r'^$', core_views.button),
    #url(r'^run_query_search', core_views.run_query_search, name='run_query_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
