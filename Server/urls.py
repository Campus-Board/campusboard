from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
#)

urlpatterns = patterns('CampusBoard.views',
    (r"^manager/", include("ManagerBoard.urls")),
    (r"^personal", "personal"),
    (r"^general", "general"),
    (r"^forum", "forum"),
    (r"", "main"),
)# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
