"""
Script to populate interview questions database
Run: python manage.py shell < populate_interview_questions.py
"""
from apps.interviews.models import InterviewQuestion

questions_data = [
    # Technical - Software Development
    {
        'question_text': 'Explain the difference between REST and GraphQL APIs.',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'medium',
        'sample_answer': 'REST uses multiple endpoints with standard HTTP methods, while GraphQL uses a single endpoint with flexible queries.'
    },
    {
        'question_text': 'What is the time complexity of binary search?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'easy',
        'sample_answer': 'O(log n) - binary search divides the search space in half with each iteration.'
    },
    {
        'question_text': 'Implement a function to reverse a linked list.',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'hard',
        'sample_answer': 'Use three pointers: previous, current, and next. Iterate through the list reversing the links.'
    },
    
    # Behavioral
    {
        'question_text': 'Tell me about a time when you had to work with a difficult team member.',
        'category': 'behavioral',
        'job_role': 'Software Developer',
        'difficulty': 'medium',
        'sample_answer': 'Use STAR method: Describe the Situation, Task, Action you took, and Result achieved.'
    },
    {
        'question_text': 'Describe a project where you had to learn a new technology quickly.',
        'category': 'behavioral',
        'job_role': 'Software Developer',
        'difficulty': 'easy',
        'sample_answer': 'Focus on your learning process, resources used, and how you applied the knowledge.'
    },
    
    # Data Science
    {
        'question_text': 'Explain the bias-variance tradeoff in machine learning.',
        'category': 'technical',
        'job_role': 'Data Scientist',
        'difficulty': 'medium',
        'sample_answer': 'Bias is error from overly simple models, variance is error from overly complex models. Need to balance both.'
    },
    {
        'question_text': 'What is the difference between supervised and unsupervised learning?',
        'category': 'technical',
        'job_role': 'Data Scientist',
        'difficulty': 'easy',
        'sample_answer': 'Supervised learning uses labeled data, unsupervised learning finds patterns in unlabeled data.'
    },
    
    # General
    {
        'question_text': 'Why do you want to work for our company?',
        'category': 'general',
        'job_role': 'General',
        'difficulty': 'easy',
        'sample_answer': 'Research the company and align your career goals with their mission and values.'
    },
    {
        'question_text': 'Where do you see yourself in 5 years?',
        'category': 'general',
        'job_role': 'General',
        'difficulty': 'easy',
        'sample_answer': 'Show ambition while staying realistic and aligned with the role.'
    },
    {
        'question_text': 'What are your salary expectations?',
        'category': 'general',
        'job_role': 'General',
        'difficulty': 'medium',
        'sample_answer': 'Research market rates and provide a range based on your experience and the role.'
    },

    # Python Developer
    {
        'question_text': 'What are the key differences between a list, tuple, set, and dictionary in Python?',
        'category': 'technical',
        'job_role': 'Python Developer',
        'difficulty': 'easy',
        'sample_answer': 'Lists and tuples are ordered collections, lists are mutable while tuples are immutable. Sets are unordered collections of unique items. Dictionaries store key-value pairs and are mutable and unordered (insertion-ordered from Python 3.7+).'
    },
    {
        'question_text': 'Explain how list comprehensions work in Python and when you would use them.',
        'category': 'technical',
        'job_role': 'Python Developer',
        'difficulty': 'easy',
        'sample_answer': 'List comprehensions provide a concise way to create lists from iterables using the syntax: [expression for item in iterable if condition]. They are useful for simple transformations and filtering in a single readable line.'
    },
    {
        'question_text': 'How does Python\'s garbage collection and reference counting work?',
        'category': 'technical',
        'job_role': 'Python Developer',
        'difficulty': 'medium',
        'sample_answer': 'Python primarily uses reference counting: each object tracks how many references point to it. When the count drops to zero, the memory is freed. Additionally, a cyclic garbage collector periodically finds and cleans up reference cycles that reference counting alone cannot handle.'
    },
    {
        'question_text': 'Describe how you would structure a Python project for a REST API using Django or FastAPI.',
        'category': 'technical',
        'job_role': 'Python Developer',
        'difficulty': 'medium',
        'sample_answer': 'I would separate concerns into modules: settings/config, models/schemas, serializers, views/routers, services, and tests. For Django I would create apps per bounded context and define URL routing and DRF viewsets. For FastAPI I would use routers, Pydantic models, and dependency injection for services and database sessions.'
    },
    {
        'question_text': 'Tell me about a challenging Python bug you fixed in production. How did you debug it?',
        'category': 'behavioral',
        'job_role': 'Python Developer',
        'difficulty': 'medium',
        'sample_answer': 'Use the STAR method: explain the production issue, how you reproduced it locally, tools you used (logs, breakpoints, profiling), options you evaluated, and the final fix and lessons learned (e.g., adding tests, monitoring, or feature flags).'
    },

    # Full Stack Developer
    {
        'question_text': 'Walk me through how a browser request flows through a full‑stack web application you built.',
        'category': 'technical',
        'job_role': 'Full Stack Developer',
        'difficulty': 'medium',
        'sample_answer': 'Start from DNS lookup and HTTP request → frontend router/component → API call → backend routing/controller → business logic/service layer → database/cache → response serialization → frontend rendering and state update. Mention security (auth, CSRF), caching, and logging along the path.'
    },
    {
        'question_text': 'How do you design a secure authentication and authorization system for a full‑stack app?',
        'category': 'technical',
        'job_role': 'Full Stack Developer',
        'difficulty': 'hard',
        'sample_answer': 'Use secure password storage (bcrypt/argon2), protect transport with HTTPS, use JWT or session cookies with HttpOnly and SameSite flags, implement role/permission checks on the backend, validate input, and protect against CSRF/XSS. Also add rate limiting and account lockout for brute‑force protection.'
    },
    {
        'question_text': 'Give an example of a time you improved performance of a slow page end‑to‑end.',
        'category': 'behavioral',
        'job_role': 'Full Stack Developer',
        'difficulty': 'medium',
        'sample_answer': 'Describe how you measured baseline performance, identified bottlenecks (e.g., N+1 queries, large payloads, unoptimized React components), implemented optimizations (caching, DB indexes, lazy loading, code‑splitting), and validated improvements with metrics and monitoring.'
    },
]

print("Creating interview questions...")
for q_data in questions_data:
    question, created = InterviewQuestion.objects.get_or_create(
        question_text=q_data['question_text'],
        defaults=q_data
    )
    if created:
        print(f"✓ Created: {q_data['question_text'][:50]}...")
    else:
        print(f"- Already exists: {q_data['question_text'][:50]}...")

print(f"\nTotal questions in database: {InterviewQuestion.objects.count()}")
