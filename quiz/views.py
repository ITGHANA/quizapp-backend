from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Quiz, Question, Choice, UserQuizAttempt, UserRanking, QuizCategory
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, UserQuizAttemptSerializer, UserRankingSerializer, UserSerializer, QuizCategorySerializer
from accounts.models import CustomUser

class QuizCategoryViewSet(viewsets.ModelViewSet):
    queryset = QuizCategory.objects.all()
    serializer_class = QuizCategorySerializer



class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def submit_attempt(self, request, pk=None):
        quiz = self.get_object()
        user = request.user
        score = request.data.get('score')
        time_taken = request.data.get('time_taken')

        if not all([score, time_taken]):
            return Response({"error": "Both score and time_taken are required."}, status=status.HTTP_400_BAD_REQUEST)

        attempt, created = UserQuizAttempt.objects.update_or_create(
            user=user,
            quiz=quiz,
            defaults={'score': score, 'time_taken': time_taken}
        )

        # Update user ranking
        ranking, _ = UserRanking.objects.get_or_create(user=user)
        ranking.total_score += int(score)
        ranking.quizzes_taken += 1
        ranking.average_score = ranking.total_score / ranking.quizzes_taken
        ranking.save()

        return Response(UserQuizAttemptSerializer(attempt).data)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserQuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = UserQuizAttempt.objects.all()
    serializer_class = UserQuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class UserRankingViewSet(viewsets.ModelViewSet):
    queryset = UserRanking.objects.all().order_by('-average_score')
    serializer_class = UserRankingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]