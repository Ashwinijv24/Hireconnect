"""
Populate MCQ Interview Questions
Run: python manage.py shell < populate_mcq_questions.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
django.setup()

from apps.interviews.models import InterviewQuestion

# Clear existing questions
InterviewQuestion.objects.all().delete()

# Software Developer MCQ Questions
software_dev_questions = [
    {
        'question_text': 'What is the time complexity of binary search algorithm?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'easy',
        'option_a': 'O(n)',
        'option_b': 'O(log n)',
        'option_c': 'O(n²)',
        'option_d': 'O(1)',
        'correct_answer': 'B',
        'explanation': 'Binary search divides the search space in half with each iteration, resulting in O(log n) time complexity.'
    },
    {
        'question_text': 'Which of the following is NOT a principle of Object-Oriented Programming?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'easy',
        'option_a': 'Encapsulation',
        'option_b': 'Inheritance',
        'option_c': 'Compilation',
        'option_d': 'Polymorphism',
        'correct_answer': 'C',
        'explanation': 'Compilation is a process, not an OOP principle. The four main OOP principles are Encapsulation, Inheritance, Polymorphism, and Abstraction.'
    },
    {
        'question_text': 'What does REST stand for in web services?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'easy',
        'option_a': 'Remote Execution Service Technology',
        'option_b': 'Representational State Transfer',
        'option_c': 'Rapid Enterprise Service Tool',
        'option_d': 'Resource Execution State Transfer',
        'correct_answer': 'B',
        'explanation': 'REST stands for Representational State Transfer, an architectural style for distributed systems.'
    },
    {
        'question_text': 'Which data structure uses LIFO (Last In First Out) principle?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'easy',
        'option_a': 'Queue',
        'option_b': 'Array',
        'option_c': 'Stack',
        'option_d': 'Linked List',
        'correct_answer': 'C',
        'explanation': 'Stack follows LIFO principle where the last element added is the first one to be removed.'
    },
    {
        'question_text': 'What is the purpose of a foreign key in a database?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'medium',
        'option_a': 'To encrypt data',
        'option_b': 'To establish relationships between tables',
        'option_c': 'To speed up queries',
        'option_d': 'To validate data types',
        'correct_answer': 'B',
        'explanation': 'A foreign key is used to establish and enforce a link between data in two tables, creating relationships.'
    },
    {
        'question_text': 'Which HTTP method is idempotent?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'medium',
        'option_a': 'POST',
        'option_b': 'PUT',
        'option_c': 'PATCH',
        'option_d': 'All of the above',
        'correct_answer': 'B',
        'explanation': 'PUT is idempotent, meaning multiple identical requests have the same effect as a single request.'
    },
    {
        'question_text': 'What is the main advantage of using microservices architecture?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'medium',
        'option_a': 'Faster development speed',
        'option_b': 'Independent deployment and scaling',
        'option_c': 'Lower infrastructure costs',
        'option_d': 'Simpler codebase',
        'correct_answer': 'B',
        'explanation': 'Microservices allow independent deployment and scaling of different services, improving flexibility and resilience.'
    },
    {
        'question_text': 'Which design pattern ensures a class has only one instance?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'medium',
        'option_a': 'Factory Pattern',
        'option_b': 'Observer Pattern',
        'option_c': 'Singleton Pattern',
        'option_d': 'Strategy Pattern',
        'correct_answer': 'C',
        'explanation': 'Singleton pattern restricts instantiation of a class to a single instance and provides global access to it.'
    },
    {
        'question_text': 'What is the space complexity of merge sort algorithm?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'hard',
        'option_a': 'O(1)',
        'option_b': 'O(log n)',
        'option_c': 'O(n)',
        'option_d': 'O(n log n)',
        'correct_answer': 'C',
        'explanation': 'Merge sort requires O(n) additional space for the temporary arrays used during merging.'
    },
    {
        'question_text': 'In distributed systems, what does CAP theorem state?',
        'category': 'technical',
        'job_role': 'Software Developer',
        'difficulty': 'hard',
        'option_a': 'You can achieve Consistency, Availability, and Partition tolerance simultaneously',
        'option_b': 'You can only achieve two out of three: Consistency, Availability, Partition tolerance',
        'option_c': 'Consistency is more important than Availability',
        'option_d': 'Partition tolerance is optional',
        'correct_answer': 'B',
        'explanation': 'CAP theorem states that a distributed system can only guarantee two out of three properties: Consistency, Availability, and Partition tolerance.'
    },
]

# Data Scientist MCQ Questions
data_scientist_questions = [
    {
        'question_text': 'What is the primary purpose of cross-validation in machine learning?',
        'category': 'technical',
        'job_role': 'Data Scientist',
        'difficulty': 'easy',
        'option_a': 'To increase model accuracy',
        'option_b': 'To assess model performance and prevent overfitting',
        'option_c': 'To reduce training time',
        'option_d': 'To clean the data',
        'correct_answer': 'B',
        'explanation': 'Cross-validation helps assess how well a model generalizes to unseen data and prevents overfitting.'
    },
    {
        'question_text': 'Which metric is best for imbalanced classification problems?',
        'category': 'technical',
        'job_role': 'Data Scientist',
        'difficulty': 'medium',
        'option_a': 'Accuracy',
        'option_b': 'F1-Score',
        'option_c': 'Mean Squared Error',
        'option_d': 'R-squared',
        'correct_answer': 'B',
        'explanation': 'F1-Score balances precision and recall, making it suitable for imbalanced datasets where accuracy can be misleading.'
    },
    {
        'question_text': 'What does PCA (Principal Component Analysis) do?',
        'category': 'technical',
        'job_role': 'Data Scientist',
        'difficulty': 'medium',
        'option_a': 'Increases the number of features',
        'option_b': 'Reduces dimensionality while preserving variance',
        'option_c': 'Removes outliers',
        'option_d': 'Normalizes the data',
        'correct_answer': 'B',
        'explanation': 'PCA is a dimensionality reduction technique that transforms data to a lower-dimensional space while retaining most of the variance.'
    },
    {
        'question_text': 'Which algorithm is best for finding clusters in data?',
        'category': 'technical',
        'job_role': 'Data Scientist',
        'difficulty': 'easy',
        'option_a': 'Linear Regression',
        'option_b': 'K-Means',
        'option_c': 'Decision Tree',
        'option_d': 'Naive Bayes',
        'correct_answer': 'B',
        'explanation': 'K-Means is a popular clustering algorithm that groups similar data points together.'
    },
    {
        'question_text': 'What is the curse of dimensionality?',
        'category': 'technical',
        'job_role': 'Data Scientist',
        'difficulty': 'hard',
        'option_a': 'Too many features make models perform poorly',
        'option_b': 'Data becomes sparse in high-dimensional space',
        'option_c': 'Distance metrics become less meaningful',
        'option_d': 'All of the above',
        'correct_answer': 'D',
        'explanation': 'The curse of dimensionality refers to various phenomena that arise when analyzing data in high-dimensional spaces, including sparsity and distance metric issues.'
    },
]

# Product Manager MCQ Questions
product_manager_questions = [
    {
        'question_text': 'What is the primary goal of a Product Manager?',
        'category': 'general',
        'job_role': 'Product Manager',
        'difficulty': 'easy',
        'option_a': 'Write code for the product',
        'option_b': 'Maximize product value and user satisfaction',
        'option_c': 'Manage the development team',
        'option_d': 'Design the user interface',
        'correct_answer': 'B',
        'explanation': 'A Product Manager focuses on maximizing product value and ensuring user satisfaction through strategic decisions.'
    },
    {
        'question_text': 'What does MVP stand for in product development?',
        'category': 'general',
        'job_role': 'Product Manager',
        'difficulty': 'easy',
        'option_a': 'Most Valuable Player',
        'option_b': 'Minimum Viable Product',
        'option_c': 'Maximum Value Proposition',
        'option_d': 'Minimum Value Package',
        'correct_answer': 'B',
        'explanation': 'MVP (Minimum Viable Product) is a version with just enough features to satisfy early customers and provide feedback.'
    },
    {
        'question_text': 'Which framework is commonly used for prioritizing features?',
        'category': 'general',
        'job_role': 'Product Manager',
        'difficulty': 'medium',
        'option_a': 'RICE',
        'option_b': 'SWOT',
        'option_c': 'PESTEL',
        'option_d': 'Porter\'s Five Forces',
        'correct_answer': 'A',
        'explanation': 'RICE (Reach, Impact, Confidence, Effort) is a popular framework for prioritizing product features and initiatives.'
    },
    {
        'question_text': 'What is a user story in Agile development?',
        'category': 'general',
        'job_role': 'Product Manager',
        'difficulty': 'easy',
        'option_a': 'A biography of the user',
        'option_b': 'A description of a feature from user perspective',
        'option_c': 'A technical specification',
        'option_d': 'A bug report',
        'correct_answer': 'B',
        'explanation': 'A user story describes a feature from the end user\'s perspective, typically in the format: "As a [user], I want [goal] so that [benefit]".'
    },
    {
        'question_text': 'What is product-market fit?',
        'category': 'general',
        'job_role': 'Product Manager',
        'difficulty': 'medium',
        'option_a': 'When the product is bug-free',
        'option_b': 'When the product satisfies strong market demand',
        'option_c': 'When the product is profitable',
        'option_d': 'When the product has all planned features',
        'correct_answer': 'B',
        'explanation': 'Product-market fit occurs when a product satisfies strong market demand and customers are willing to pay for it.'
    },
]

# UI/UX Designer MCQ Questions
uiux_designer_questions = [
    {
        'question_text': 'What does UX stand for?',
        'category': 'general',
        'job_role': 'UI/UX Designer',
        'difficulty': 'easy',
        'option_a': 'User Experience',
        'option_b': 'Universal Extension',
        'option_c': 'User Execution',
        'option_d': 'Unified Experience',
        'correct_answer': 'A',
        'explanation': 'UX stands for User Experience, which encompasses all aspects of user interaction with a product.'
    },
    {
        'question_text': 'Which principle states that users spend most time on other sites?',
        'category': 'general',
        'job_role': 'UI/UX Designer',
        'difficulty': 'medium',
        'option_a': 'Hick\'s Law',
        'option_b': 'Jakob\'s Law',
        'option_c': 'Fitts\'s Law',
        'option_d': 'Miller\'s Law',
        'correct_answer': 'B',
        'explanation': 'Jakob\'s Law states that users prefer your site to work the same way as other sites they already know.'
    },
    {
        'question_text': 'What is the purpose of a wireframe?',
        'category': 'general',
        'job_role': 'UI/UX Designer',
        'difficulty': 'easy',
        'option_a': 'To show final colors and images',
        'option_b': 'To outline structure and layout',
        'option_c': 'To write code',
        'option_d': 'To test performance',
        'correct_answer': 'B',
        'explanation': 'A wireframe is a low-fidelity representation that outlines the structure and layout of a page or screen.'
    },
    {
        'question_text': 'What is the recommended minimum touch target size for mobile?',
        'category': 'technical',
        'job_role': 'UI/UX Designer',
        'difficulty': 'medium',
        'option_a': '24x24 pixels',
        'option_b': '32x32 pixels',
        'option_c': '44x44 pixels',
        'option_d': '64x64 pixels',
        'correct_answer': 'C',
        'explanation': 'Apple\'s Human Interface Guidelines recommend a minimum touch target size of 44x44 points for comfortable interaction.'
    },
    {
        'question_text': 'What is A/B testing used for?',
        'category': 'general',
        'job_role': 'UI/UX Designer',
        'difficulty': 'easy',
        'option_a': 'Testing two different versions to see which performs better',
        'option_b': 'Testing alphabetical order',
        'option_c': 'Testing accessibility',
        'option_d': 'Testing browser compatibility',
        'correct_answer': 'A',
        'explanation': 'A/B testing compares two versions of a design to determine which one performs better based on user behavior.'
    },
]

# Combine all questions
all_questions = (
    software_dev_questions + 
    data_scientist_questions + 
    product_manager_questions + 
    uiux_designer_questions
)

# Create questions
created_count = 0
for q_data in all_questions:
    q_data['question_type'] = 'mcq'
    InterviewQuestion.objects.create(**q_data)
    created_count += 1

print(f"✅ Successfully created {created_count} MCQ interview questions!")
print(f"   - Software Developer: {len(software_dev_questions)}")
print(f"   - Data Scientist: {len(data_scientist_questions)}")
print(f"   - Product Manager: {len(product_manager_questions)}")
print(f"   - UI/UX Designer: {len(uiux_designer_questions)}")
