from django.contrib import admin

# Register your models here.
import pluto.models as pluto

admin.site.register(pluto.Article)
admin.site.register(pluto.User)
admin.site.register(pluto.Mate)

admin.site.register(pluto.Level)
admin.site.register(pluto.Record)