# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('ManagerBoard.views',
    #(r"^upload", "upload"),
    #(r"", "upload"),
    url(r'^upload', 'upload', name='upload'),
    url(r'^login', 'login', name='login'),
    url(r'^document', 'document', name='document'),
)

print "adasdasd"
