from django.contrib import admin

# Register your models here.
from .models import *

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

class AnswerStore(admin.ModelAdmin):
    model = UserChoices

admin.site.register(Question, QuestionAdmin)
admin.site.register(UserChoices, AnswerStore)