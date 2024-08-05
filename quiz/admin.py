from django.contrib import admin
from .models import Quiz, Question, Choice, UserQuizAttempt, UserRanking
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'quiz')
    list_filter = ('quiz',)
    search_fields = ['text', 'quiz__title']

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'time_limit', 'created_at')
    list_filter = ('created_at',)
    search_fields = ['title', 'description']

class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'time_taken', 'completed_at')
    list_filter = ('completed_at', 'quiz')
    search_fields = ['user__username', 'quiz__title']

class UserRankingAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_score', 'quizzes_taken', 'average_score')
    list_filter = ('average_score',)
    search_fields = ['user__username']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserQuizAttempt, UserQuizAttemptAdmin)
admin.site.register(UserRanking, UserRankingAdmin)