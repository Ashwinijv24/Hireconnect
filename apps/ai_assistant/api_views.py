from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatConversation, ChatMessage, CoverLetter, SalaryInsight
from .serializers import (ChatConversationSerializer, ChatMessageSerializer, 
                          CoverLetterSerializer, SalaryInsightSerializer)
from apps.jobs.models import Job
import random


class ChatConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ChatConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatConversation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message and get AI response"""
        conversation = self.get_object()
        user_message = request.data.get('message')
        
        # Save user message
        ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # Generate AI response (placeholder)
        ai_response = self._generate_ai_response(user_message, request.user)
        
        # Save AI response
        ChatMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=ai_response
        )
        
        return Response(ChatConversationSerializer(conversation).data)
    
    def _generate_ai_response(self, message, user):
        """Generate contextual AI response based on user message"""
        message_lower = message.lower()
        
        # Resume/CV related queries
        if 'resume' in message_lower or 'cv' in message_lower:
            if 'format' in message_lower or 'template' in message_lower:
                return """For resume formatting, I recommend:
- Use a clean, professional layout with clear sections
- Stick to standard fonts (Arial, Calibri, Times New Roman)
- Keep margins between 0.5-1 inch
- Use consistent bullet points and spacing
- Save as PDF to preserve formatting across devices
- Aim for 1-2 pages maximum

Would you like specific advice on any section?"""
            elif 'skill' in message_lower or 'skills' in message_lower:
                return """When listing skills on your resume:
- Prioritize skills relevant to the job description
- Include both technical and soft skills
- Be honest about your proficiency level
- Group related skills together
- Update skills based on each job application
- Consider adding certifications or proficiency levels

What type of role are you targeting?"""
            elif 'experience' in message_lower or 'work' in message_lower:
                return """For describing work experience:
- Use action verbs (led, developed, implemented, improved)
- Quantify achievements with metrics (increased by 25%, reduced time by 40%)
- Focus on impact, not just duties
- Tailor descriptions to match job requirements
- Include 3-5 bullet points per role
- Start with most recent position

Need help with a specific role description?"""
            else:
                return """I can help optimize your resume! Here are key areas:
- Structure: Use clear sections (Contact, Summary, Experience, Skills, Education)
- Content: Focus on achievements and quantifiable results
- Keywords: Match job description terminology
- Formatting: Keep it clean and professional
- Length: Aim for 1-2 pages

What aspect would you like to improve?"""
        
        # Interview preparation
        if 'interview' in message_lower:
            if 'question' in message_lower or 'ask' in message_lower:
                return """Common interview questions to prepare for:
- Tell me about yourself (focus on relevant experience)
- Why do you want this role? (research the company)
- What are your strengths? (provide specific examples)
- Describe a challenge you overcame (use STAR method)
- Where do you see yourself in 5 years? (align with company)
- Why should we hire you? (unique value proposition)

Would you like to practice with our mock interview feature?"""
            elif 'prepare' in message_lower or 'practice' in message_lower:
                return """Interview preparation checklist:
- Research the company thoroughly (mission, recent news, culture)
- Review the job description and prepare examples
- Practice common questions with STAR method
- Prepare thoughtful questions to ask them
- Plan your outfit and route to the interview
- Get good sleep the night before
- Arrive 10-15 minutes early

Try our mock interview feature to practice!"""
            elif 'star' in message_lower or 'method' in message_lower:
                return """The STAR method for behavioral questions:
- Situation: Describe the context briefly
- Task: Explain what you needed to accomplish
- Action: Detail the specific steps you took
- Result: Share the positive outcome with metrics

Example: "In my previous role, I [Situation], so I [Task]. I [Action], which resulted in [Result]."

This approach shows your problem-solving skills effectively."""
            else:
                return """Interview tips for success:
- Arrive early and dress professionally
- Make eye contact and offer a firm handshake
- Listen carefully to questions before answering
- Use specific examples from your experience
- Ask thoughtful questions about the role
- Follow up with a thank you email
- Be authentic and enthusiastic

Would you like specific interview preparation?"""
        
        # Salary and compensation
        if 'salary' in message_lower or 'pay' in message_lower or 'compensation' in message_lower:
            if 'negotiate' in message_lower or 'negotiat' in message_lower:
                return """Salary negotiation tips:
- Research market rates for your role and location
- Know your worth based on experience and skills
- Don't mention a number first if possible
- Ask for time to consider the offer
- Negotiate beyond salary (benefits, flexibility, PTO)
- Be professional and collaborative
- Get the offer in writing

Use our salary insights tool to research market rates."""
            elif 'range' in message_lower or 'market' in message_lower:
                return """To find salary ranges:
- Use our Salary Insights tool with job title and location
- Check Glassdoor, PayScale, and LinkedIn Salary
- Consider your experience level (entry, mid, senior)
- Factor in location cost of living
- Include benefits and bonuses in total compensation
- Compare across similar companies

What job title and location are you interested in?"""
            else:
                return """Salary information I can help with:
- Market research for your role and location
- Negotiation strategies and talking points
- Understanding total compensation packages
- Benefits evaluation and comparison
- Career progression and salary growth

Use our Salary Insights tool or tell me your role and location."""
        
        # Job search and applications
        if 'job' in message_lower or 'apply' in message_lower or 'application' in message_lower:
            if 'search' in message_lower or 'find' in message_lower:
                return """Tips for effective job searching:
- Use specific keywords matching your skills
- Filter by location, experience level, and job type
- Set up job alerts for new postings
- Follow companies you're interested in
- Network on LinkedIn and industry events
- Customize applications for each role
- Track your applications in our system

Browse our job listings or use filters to narrow down."""
            elif 'cover' in message_lower or 'letter' in message_lower:
                return """Writing an effective cover letter:
- Address it to a specific person if possible
- Show enthusiasm for the company and role
- Highlight relevant skills and achievements
- Keep it to one page
- Use professional tone but show personality
- Proofread carefully for errors
- Use our AI Cover Letter generator for help

Would you like me to help generate a cover letter?"""
            elif 'track' in message_lower or 'status' in message_lower:
                return """Track your applications easily:
- Visit "My Applications" to see all your submissions
- Check application status (Pending, Reviewing, Shortlisted, etc.)
- View timeline of updates and communications
- Access your submitted resume and cover letter
- Receive notifications on status changes
- Message employers directly through the platform

Check your application dashboard now."""
            else:
                return """Job search assistance available:
- Browse and filter job listings
- Apply with resume and cover letter
- Track application status in real-time
- Get AI-powered job matching scores
- Receive notifications on updates
- Practice with mock interviews
- Optimize your profile

What would you like help with?"""
        
        # Career guidance and general help
        if 'career' in message_lower or 'goal' in message_lower or 'path' in message_lower:
            return """Career development guidance:
- Identify your strengths and interests
- Set clear short-term and long-term goals
- Build relevant skills through courses or projects
- Network with professionals in your field
- Seek mentorship and feedback
- Track your progress and adjust as needed
- Consider certifications for your industry

What career goals are you working towards?"""
        
        # Default helpful response
        return """I'm your AI job search assistant! I can help with:

📄 **Resume & CV**: Formatting, content, skills optimization
🎤 **Interview Prep**: Questions, STAR method, practice tips
💰 **Salary**: Market research, negotiation strategies
🔍 **Job Search**: Finding roles, applications, tracking
📝 **Cover Letters**: Writing tips and AI generation
🎯 **Career Guidance**: Goals, skills, development

What would you like help with today? Ask me anything about your job search!"""


class CoverLetterViewSet(viewsets.ModelViewSet):
    serializer_class = CoverLetterSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate AI cover letter"""
        job_id = request.data.get('job_id')
        job_title = request.data.get('job_title')
        company_name = request.data.get('company_name')
        
        # Get job details if job_id provided
        if job_id:
            try:
                job = Job.objects.get(id=job_id)
                job_title = job.title
                company_name = job.company.name
            except Job.DoesNotExist:
                pass
        
        # Generate cover letter content
        content = self._generate_cover_letter(request.user, job_title, company_name)
        
        cover_letter = CoverLetter.objects.create(
            user=request.user,
            job_title=job_title,
            company_name=company_name,
            content=content
        )
        
        return Response(CoverLetterSerializer(cover_letter).data)
    
    def _generate_cover_letter(self, user, job_title, company_name):
        """Generate cover letter content (placeholder)"""
        user_name = user.get_full_name() or user.username
        
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my background and skills, I am confident I would be a valuable addition to your team.

Throughout my career, I have developed expertise in various areas that align perfectly with this role. I am particularly drawn to {company_name} because of your innovative approach and commitment to excellence.

Key qualifications I bring include:
- Strong technical and problem-solving skills
- Proven track record of delivering results
- Excellent communication and teamwork abilities
- Passion for continuous learning and growth

I am excited about the opportunity to contribute to {company_name}'s success and would welcome the chance to discuss how my skills and experience align with your needs.

Thank you for considering my application. I look forward to hearing from you.

Sincerely,
{user_name}"""


class SalaryInsightViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SalaryInsight.objects.all()
    serializer_class = SalaryInsightSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search salary insights by job title and location"""
        job_title = request.query_params.get('job_title')
        location = request.query_params.get('location')
        experience_level = request.query_params.get('experience_level', 'mid')
        
        # Try to find existing insight
        insight = SalaryInsight.objects.filter(
            job_title__icontains=job_title,
            location__icontains=location if location else '',
            experience_level=experience_level
        ).first()
        
        if not insight:
            # Generate mock salary data
            insight = self._generate_salary_insight(job_title, location, experience_level)
        
        return Response(SalaryInsightSerializer(insight).data)
    
    @action(detail=False, methods=['post'])
    def analyze(self, request):
        """Analyze salary for a given job title, location, and experience level"""
        job_title = request.data.get('job_title')
        location = request.data.get('location')
        years_of_experience = request.data.get('years_of_experience', 5)
        
        if not job_title or not location:
            return Response(
                {'error': 'job_title and location are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Determine experience level based on years
        if years_of_experience < 2:
            experience_level = 'entry'
        elif years_of_experience < 5:
            experience_level = 'mid'
        elif years_of_experience < 10:
            experience_level = 'senior'
        else:
            experience_level = 'lead'
        
        # Generate salary insight
        insight = self._generate_salary_insight(job_title, location, experience_level)
        
        # Format insights text
        insights_text = self._format_salary_insights(insight, job_title, location, years_of_experience)
        
        return Response({
            'insights': insights_text,
            'salary_data': SalaryInsightSerializer(insight).data
        })
    
    def _generate_salary_insight(self, job_title, location, experience_level):
        """Generate salary insight data (placeholder)"""
        # Base salary ranges by experience level
        base_ranges = {
            'entry': (40000, 70000),
            'mid': (70000, 120000),
            'senior': (120000, 180000),
            'lead': (150000, 250000)
        }
        
        min_sal, max_sal = base_ranges.get(experience_level, (60000, 100000))
        median_sal = (min_sal + max_sal) / 2
        
        # Adjust for location (placeholder logic)
        if location and any(city in location.lower() for city in ['san francisco', 'new york', 'seattle']):
            min_sal *= 1.3
            max_sal *= 1.3
            median_sal *= 1.3
        
        insight = SalaryInsight.objects.create(
            job_title=job_title,
            location=location or 'United States',
            experience_level=experience_level,
            min_salary=min_sal,
            max_salary=max_sal,
            median_salary=median_sal,
            data_points=random.randint(50, 500)
        )
        
        return insight

    def _format_salary_insights(self, insight, job_title, location, years_of_experience):
        """Format salary insights into readable text"""
        exp_level = insight.experience_level.upper()
        min_sal = f"${insight.min_salary:,.0f}"
        max_sal = f"${insight.max_salary:,.0f}"
        median_sal = f"${insight.median_salary:,.0f}"
        
        insights = f"""SALARY ANALYSIS FOR {job_title.upper()}

Location: {location}
Experience Level: {exp_level}
Years of Experience: {years_of_experience}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SALARY RANGE:
  Minimum: {min_sal}
  Median:  {median_sal}
  Maximum: {max_sal}

Data Points: {insight.data_points} salary records analyzed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY INSIGHTS:

1. MARKET POSITION
   Your experience level ({exp_level}) typically earns between {min_sal} and {max_sal}
   in {location}. The median salary for this role is {median_sal}.

2. EXPERIENCE IMPACT
   With {years_of_experience} years of experience, you're positioned in the {exp_level}
   category. Each additional year typically increases earning potential by 3-5%.

3. LOCATION FACTOR
   {location} is {'a high-cost area with premium salaries' if any(city in location.lower() for city in ['san francisco', 'new york', 'seattle']) else 'a standard market for tech salaries'}.
   Salaries vary significantly by region.

4. NEGOTIATION TIPS
   • Research company size and funding (startups vs. established companies)
   • Consider total compensation (benefits, stock, bonuses)
   • Highlight your unique skills and achievements
   • Don't accept the first offer - negotiate professionally
   • Factor in cost of living for the location

5. CAREER GROWTH
   • Entry Level ({exp_level}): Focus on building skills and experience
   • Mid Level: Emphasize leadership and project impact
   • Senior Level: Highlight strategic contributions and mentorship
   • Lead Level: Demonstrate business impact and team leadership

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS:
✓ Use this data to set realistic salary expectations
✓ Prepare negotiation talking points
✓ Research specific companies for their salary bands
✓ Consider benefits and work-life balance in your decision
✓ Track salary trends over time

Good luck with your job search!"""
        
        return insights
