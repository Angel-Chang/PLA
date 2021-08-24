# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Hide the header 
admin.site.site_header = " "
admin.site.site_title = "Pet Life Admin"
admin.site.site_url = None 
admin.site.index_title = " "
# Register your models here.
admin.site.register(member)
admin.site.register(LoginInfo)
admin.site.register(pet)
admin.site.register(doctor)
admin.site.register(docAppoint)
admin.site.register(userAppoint)
admin.site.register(advisory)
admin.site.register(docComment)
admin.site.register(docBH)
admin.site.register(clinic)
admin.site.register(clinicBH)
admin.site.register(store)
admin.site.register(storeBH)
admin.site.register(Account)
admin.site.register(BKLoginInfo)
admin.site.register(dynaPost)
admin.site.register(MemberLikePost)
admin.site.register(SocialAccount)
