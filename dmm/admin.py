from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Specie)
admin.site.register(Tag)
admin.site.register(TonalType)
admin.site.register(Expert)
admin.site.register(ContentType)
admin.site.register(ResourceType)
admin.site.register(LanguageType)


admin.site.register(Result)
admin.site.register(Comment)
admin.site.register(CommentRound)
admin.site.register(CommentRoundTags)
