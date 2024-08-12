from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class QuizCategory(models.Model):
    SCIENCE = 'Science'
    TECHNOLOGY = 'Technology'
    GENERAL_KNOWLEDGE = 'General Knowledge'

    CATEGORY_CHOICES = [
        (SCIENCE, 'Science'),
        (TECHNOLOGY, 'Technology'),
        (GENERAL_KNOWLEDGE, 'General Knowledge'),
    ]

    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=GENERAL_KNOWLEDGE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "categories"
    

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    time_limit = models.IntegerField(default=15, help_text="Time limit in seconds")
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Quizzes"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserQuizAttempt(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    time_taken = models.IntegerField(help_text="Time taken in seconds")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'quiz']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

class UserRanking(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    quizzes_taken = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - Rank: {self.average_score:.2f}"



@receiver(post_save, sender='accounts.CustomUser')
def create_user_ranking(sender, instance, created, **kwargs):
    if created:
        UserRanking.objects.create(user=instance)