from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import MockInterview, VideoInterview, InterviewQuestion
from .serializers import MockInterviewSerializer, VideoInterviewSerializer, InterviewQuestionSerializer
import random


class MockInterviewViewSet(viewsets.ModelViewSet):
    serializer_class = MockInterviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MockInterview.objects.filter(candidate=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)
    
    @action(detail=False, methods=['post'])
    def start_interview(self, request):
        """Start a new mock interview session with MCQ questions"""
        job_category = request.data.get('job_category')
        difficulty = request.data.get('difficulty', 'medium')
        
        # Get 15 random MCQ questions from the bank
        questions = list(InterviewQuestion.objects.filter(
            job_role__icontains=job_category,
            difficulty=difficulty,
            question_type='mcq'
        ))
        
        # If not enough questions for this category, get from all categories
        if len(questions) < 15:
            questions = list(InterviewQuestion.objects.filter(
                difficulty=difficulty,
                question_type='mcq'
            ))
        
        # Randomly select 15 questions
        selected_questions = random.sample(questions, min(15, len(questions)))
        
        question_list = [
            {
                'id': q.id,
                'text': q.question_text,
                'category': q.category,
                'options': {
                    'A': q.option_a,
                    'B': q.option_b,
                    'C': q.option_c,
                    'D': q.option_d
                }
            }
            for q in selected_questions
        ]
        
        interview = MockInterview.objects.create(
            candidate=request.user,
            job_category=job_category,
            difficulty=difficulty,
            questions=question_list
        )
        
        return Response(MockInterviewSerializer(interview).data)
    
    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        """Submit MCQ answer for a question"""
        interview = self.get_object()
        question_id = request.data.get('question_id')
        selected_option = request.data.get('answer')  # A, B, C, or D
        
        # Get the question to check correct answer
        try:
            question = InterviewQuestion.objects.get(id=question_id)
            is_correct = (selected_option == question.correct_answer)
        except InterviewQuestion.DoesNotExist:
            is_correct = False
        
        answers = interview.answers or []
        answers.append({
            'question_id': question_id,
            'answer': selected_option,
            'is_correct': is_correct
        })
        interview.answers = answers
        interview.save()
        
        return Response({'status': 'answer_saved', 'is_correct': is_correct})
    
    @action(detail=True, methods=['post'])
    def complete_interview(self, request, pk=None):
        """Complete interview and calculate score"""
        interview = self.get_object()
        
        # Calculate score based on correct answers
        total_questions = len(interview.questions)
        correct_answers = sum(1 for ans in interview.answers if ans.get('is_correct', False))
        score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
        
        # Generate feedback
        feedback = self._generate_mcq_feedback(interview, correct_answers, total_questions)
        
        interview.completed = True
        interview.ai_feedback = feedback
        interview.score = score
        interview.save()
        
        return Response(MockInterviewSerializer(interview).data)
    
    def _generate_mcq_feedback(self, interview, correct_answers, total_questions):
        """Generate feedback for MCQ interview"""
        percentage = (correct_answers / total_questions) * 100
        
        if percentage >= 80:
            performance = "Excellent"
            comment = "You demonstrated strong knowledge in this area!"
        elif percentage >= 60:
            performance = "Good"
            comment = "You have a solid understanding with room for improvement."
        elif percentage >= 40:
            performance = "Fair"
            comment = "You have basic knowledge but need more practice."
        else:
            performance = "Needs Improvement"
            comment = "Consider reviewing the fundamentals in this area."
        
        return f"""
Performance: {performance}

Score: {correct_answers}/{total_questions} correct answers ({percentage:.1f}%)

{comment}

Recommendations:
- Review the questions you got wrong
- Study the explanations for correct answers
- Practice more questions in this category
- Focus on areas where you struggled
- Take another practice test to track improvement
        """


class VideoInterviewViewSet(viewsets.ModelViewSet):
    serializer_class = VideoInterviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_employer:
            # Employers see interviews for their job applications
            return VideoInterview.objects.filter(
                application__job__posted_by=self.request.user
            )
        else:
            # Candidates see their own interviews
            return VideoInterview.objects.filter(
                application__candidate__user=self.request.user
            )

    def perform_create(self, serializer):
        # Only employers can create/schedule interviews, and only for their jobs
        user = self.request.user
        if not user.is_employer and not user.is_superuser:
            raise PermissionDenied('Only employers can schedule video interviews')

        app = serializer.validated_data.get('application')
        if not user.is_superuser and app.job.posted_by_id != user.id:
            raise PermissionDenied('Not allowed')

        serializer.save()
    
    @action(detail=True, methods=['post'])
    def generate_meeting_link(self, request, pk=None):
        """Generate video meeting link (placeholder)"""
        interview = self.get_object()
        # In production, integrate with Zoom/Google Meet API
        meeting_link = f"https://meet.example.com/{interview.id}"
        interview.meeting_link = meeting_link
        interview.save()
        
        return Response({'meeting_link': meeting_link})


class InterviewQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InterviewQuestion.objects.all()
    serializer_class = InterviewQuestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        job_role = self.request.query_params.get('job_role')
        difficulty = self.request.query_params.get('difficulty')
        
        if job_role:
            queryset = queryset.filter(job_role__icontains=job_role)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset
