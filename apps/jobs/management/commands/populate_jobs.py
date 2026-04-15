from django.core.management.base import BaseCommand
from apps.companies.models import Company
from apps.jobs.models import Job, JobCategory


class Command(BaseCommand):
    help = 'Populate database with sample job data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create companies
        companies_data = [
            {'name': 'TechCorp', 'slug': 'techcorp', 'website': 'https://techcorp.com', 
             'description': 'Leading technology company'},
            {'name': 'DataSystems Inc', 'slug': 'datasystems', 'website': 'https://datasystems.com',
             'description': 'Data analytics and AI solutions'},
            {'name': 'WebDev Solutions', 'slug': 'webdev', 'website': 'https://webdev.com',
             'description': 'Full-stack web development agency'},
            {'name': 'CloudTech', 'slug': 'cloudtech', 'website': 'https://cloudtech.com',
             'description': 'Cloud infrastructure provider'},
        ]
        
        companies = []
        for data in companies_data:
            company, created = Company.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            companies.append(company)
            if created:
                self.stdout.write(f'Created company: {company.name}')
        
        # Create job categories
        categories_data = [
            {'name': 'Software Development', 'slug': 'software-development'},
            {'name': 'Data Science', 'slug': 'data-science'},
            {'name': 'Design', 'slug': 'design'},
        ]
        
        for data in categories_data:
            category, created = JobCategory.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create jobs
        jobs_data = [
            {
                'company': companies[0],
                'title': 'Senior Full Stack Developer',
                'description': 'We are looking for an experienced Full Stack Developer to join our team. You will work on cutting-edge web applications using React, Node.js, and PostgreSQL. Must have 5+ years of experience.',
                'location': 'New York, NY',
                'employment_type': 'FT',
                'salary_min': 120000,
                'salary_max': 160000,
            },
            {
                'company': companies[1],
                'title': 'Data Scientist',
                'description': 'Join our data science team to build machine learning models and analyze large datasets. Experience with Python, TensorFlow, and SQL required. PhD preferred.',
                'location': 'San Francisco, CA',
                'employment_type': 'FT',
                'salary_min': 130000,
                'salary_max': 180000,
            },
            {
                'company': companies[2],
                'title': 'Frontend Developer',
                'description': 'Looking for a talented Frontend Developer with expertise in React, TypeScript, and modern CSS. You will create beautiful, responsive user interfaces.',
                'location': 'Remote',
                'employment_type': 'FT',
                'salary_min': 90000,
                'salary_max': 130000,
            },
            {
                'company': companies[0],
                'title': 'DevOps Engineer',
                'description': 'Seeking a DevOps Engineer to manage our cloud infrastructure. Experience with AWS, Docker, Kubernetes, and CI/CD pipelines required.',
                'location': 'Austin, TX',
                'employment_type': 'FT',
                'salary_min': 110000,
                'salary_max': 150000,
            },
            {
                'company': companies[3],
                'title': 'Cloud Solutions Architect',
                'description': 'Design and implement scalable cloud solutions for enterprise clients. Must have deep knowledge of AWS/Azure and 7+ years experience.',
                'location': 'Seattle, WA',
                'employment_type': 'FT',
                'salary_min': 150000,
                'salary_max': 200000,
            },
            {
                'company': companies[2],
                'title': 'UI/UX Designer',
                'description': 'Create intuitive and beautiful user experiences. Proficiency in Figma, Adobe XD, and user research methodologies required.',
                'location': 'Los Angeles, CA',
                'employment_type': 'FT',
                'salary_min': 80000,
                'salary_max': 120000,
            },
            {
                'company': companies[1],
                'title': 'Backend Developer',
                'description': 'Build robust APIs and microservices using Python/Django or Node.js. Experience with databases and distributed systems preferred.',
                'location': 'Boston, MA',
                'employment_type': 'FT',
                'salary_min': 100000,
                'salary_max': 140000,
            },
            {
                'company': companies[3],
                'title': 'Junior Software Engineer',
                'description': 'Entry-level position for recent graduates. Learn from experienced engineers while contributing to real projects. CS degree required.',
                'location': 'Remote',
                'employment_type': 'FT',
                'salary_min': 70000,
                'salary_max': 90000,
            },
            {
                'company': companies[0],
                'title': 'Machine Learning Engineer',
                'description': 'Develop and deploy ML models for production systems. Strong background in Python, PyTorch, and cloud platforms required. 3+ years experience.',
                'location': 'San Francisco, CA',
                'employment_type': 'FT',
                'salary_min': 140000,
                'salary_max': 190000,
            },
            {
                'company': companies[2],
                'title': 'Mobile App Developer',
                'description': 'Build native iOS and Android applications. Experience with Swift, Kotlin, and React Native preferred. Join our growing mobile team.',
                'location': 'Chicago, IL',
                'employment_type': 'FT',
                'salary_min': 95000,
                'salary_max': 135000,
            },
            {
                'company': companies[1],
                'title': 'Database Administrator',
                'description': 'Manage and optimize our database infrastructure. Experience with PostgreSQL, MongoDB, and database performance tuning required.',
                'location': 'Denver, CO',
                'employment_type': 'FT',
                'salary_min': 105000,
                'salary_max': 145000,
            },
            {
                'company': companies[3],
                'title': 'Security Engineer',
                'description': 'Protect our systems and data from threats. Experience with cybersecurity, penetration testing, and security protocols required.',
                'location': 'Washington, DC',
                'employment_type': 'FT',
                'salary_min': 125000,
                'salary_max': 170000,
            },
            {
                'company': companies[0],
                'title': 'Product Manager',
                'description': 'Lead product strategy and development. Experience with agile methodologies and cross-functional team management required.',
                'location': 'New York, NY',
                'employment_type': 'FT',
                'salary_min': 115000,
                'salary_max': 155000,
            },
            {
                'company': companies[2],
                'title': 'QA Engineer',
                'description': 'Ensure quality of our software products. Experience with automated testing, Selenium, and test frameworks required.',
                'location': 'Remote',
                'employment_type': 'FT',
                'salary_min': 85000,
                'salary_max': 120000,
            },
            {
                'company': companies[1],
                'title': 'Solutions Architect',
                'description': 'Design technical solutions for enterprise clients. 8+ years experience in software architecture and system design required.',
                'location': 'Boston, MA',
                'employment_type': 'FT',
                'salary_min': 135000,
                'salary_max': 180000,
            },
            {
                'company': companies[3],
                'title': 'Technical Writer',
                'description': 'Create clear and comprehensive technical documentation. Experience with API documentation and developer guides required.',
                'location': 'Remote',
                'employment_type': 'FT',
                'salary_min': 75000,
                'salary_max': 105000,
            },
            {
                'company': companies[0],
                'title': 'Systems Administrator',
                'description': 'Manage and maintain our IT infrastructure. Experience with Linux, Windows servers, and network administration required.',
                'location': 'Austin, TX',
                'employment_type': 'FT',
                'salary_min': 90000,
                'salary_max': 125000,
            },
            {
                'company': companies[2],
                'title': 'Graphic Designer',
                'description': 'Design visual content for web and mobile applications. Proficiency in Adobe Creative Suite and design principles required.',
                'location': 'Los Angeles, CA',
                'employment_type': 'FT',
                'salary_min': 70000,
                'salary_max': 110000,
            },
            {
                'company': companies[1],
                'title': 'Analytics Engineer',
                'description': 'Build data pipelines and analytics infrastructure. Experience with dbt, SQL, and data warehousing required.',
                'location': 'San Francisco, CA',
                'employment_type': 'FT',
                'salary_min': 120000,
                'salary_max': 160000,
            },
            {
                'company': companies[3],
                'title': 'Infrastructure Engineer',
                'description': 'Design and maintain scalable infrastructure. Experience with Terraform, Kubernetes, and cloud platforms required.',
                'location': 'Seattle, WA',
                'employment_type': 'FT',
                'salary_min': 130000,
                'salary_max': 175000,
            },
        ]
        
        for data in jobs_data:
            job, created = Job.objects.get_or_create(
                company=data['company'],
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created job: {job.title} at {job.company.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {Job.objects.count()} jobs!'))
