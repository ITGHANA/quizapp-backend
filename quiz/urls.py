from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, ChoiceViewSet, UserQuizAttemptViewSet, UserRankingViewSet, UserViewSet

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'attempts', UserQuizAttemptViewSet)
router.register(r'rankings', UserRankingViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]