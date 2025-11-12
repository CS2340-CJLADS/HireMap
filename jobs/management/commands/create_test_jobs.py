from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Recruiter
from jobs.models import JobPosting
from decimal import Decimal


class Command(BaseCommand):
    help = 'Delete all existing jobs and create test job postings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-existing',
            action='store_true',
            help='Keep existing jobs and only add new test jobs',
        )

    def handle(self, *args, **options):
        keep_existing = options['keep_existing']
        
        if not keep_existing:
            # Delete all existing jobs
            count = JobPosting.objects.all().count()
            JobPosting.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {count} existing job postings'))
        
        # Get or create test recruiters
        recruiters_data = [
            {
                'username': 'techcorp@example.com',
                'email': 'techcorp@example.com',
                'company': 'TechCorp',
                'first_name': 'John',
                'last_name': 'Smith',
            },
            {
                'username': 'innovate@example.com',
                'email': 'innovate@example.com',
                'company': 'Innovate Labs',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
            },
            {
                'username': 'startup@example.com',
                'email': 'startup@example.com',
                'company': 'StartupXYZ',
                'first_name': 'Mike',
                'last_name': 'Davis',
            },
            {
                'username': 'bigtech@example.com',
                'email': 'bigtech@example.com',
                'company': 'BigTech Inc',
                'first_name': 'Emily',
                'last_name': 'Chen',
            },
        ]
        
        recruiters = []
        for rec_data in recruiters_data:
            user, created = User.objects.get_or_create(
                username=rec_data['username'],
                defaults={
                    'email': rec_data['email'],
                    'first_name': rec_data['first_name'],
                    'last_name': rec_data['last_name'],
                }
            )
            recruiter, created = Recruiter.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': rec_data['first_name'],
                    'last_name': rec_data['last_name'],
                    'company_name': rec_data['company'],
                    'city': 'San Francisco',
                    'state': 'CA',
                    'country': 'USA',
                }
            )
            recruiters.append(recruiter)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created recruiter: {rec_data["company"]}'))
        
        # Test job postings data
        test_jobs = [
            # Remote jobs
            {
                'title': 'Senior Software Engineer',
                'description': 'We are looking for an experienced software engineer to join our remote team. You will work on building scalable web applications using modern technologies.',
                'skills_required': 'Python, Django, React, PostgreSQL, AWS',
                'street_address': '1600 Amphitheatre Parkway',
                'post_code': '94043',
                'city': 'Mountain View',
                'state': 'CA',
                'country': 'USA',
                'salary_min': Decimal('120000.00'),
                'salary_max': Decimal('180000.00'),
                'remote': True,
                'visa_sponsorship': True,
                'recruiter': recruiters[0],
            },
            {
                'title': 'Full Stack Developer',
                'description': 'Join our team as a full stack developer. Work on exciting projects with cutting-edge technologies in a fully remote environment.',
                'skills_required': 'JavaScript, Node.js, React, MongoDB, Docker',
                'street_address': '1 Hacker Way',
                'post_code': '94025',
                'city': 'Menlo Park',
                'state': 'CA',
                'country': 'USA',
                'salary_min': Decimal('100000.00'),
                'salary_max': Decimal('150000.00'),
                'remote': True,
                'visa_sponsorship': False,
                'recruiter': recruiters[1],
            },
            {
                'title': 'DevOps Engineer',
                'description': 'We need a DevOps engineer to help us scale our infrastructure. Remote work available with flexible hours.',
                'skills_required': 'Kubernetes, Docker, AWS, Terraform, CI/CD',
                'street_address': '410 Terry Avenue North',
                'post_code': '98109',
                'city': 'Seattle',
                'state': 'WA',
                'country': 'USA',
                'salary_min': Decimal('130000.00'),
                'salary_max': Decimal('190000.00'),
                'remote': True,
                'visa_sponsorship': True,
                'recruiter': recruiters[2],
            },
            {
                'title': 'Data Scientist',
                'description': 'Looking for a data scientist to analyze large datasets and build machine learning models. Remote position with occasional team meetups.',
                'skills_required': 'Python, TensorFlow, SQL, Statistics, Machine Learning',
                'street_address': '1 Microsoft Way',
                'post_code': '98052',
                'city': 'Redmond',
                'state': 'WA',
                'country': 'USA',
                'salary_min': Decimal('110000.00'),
                'salary_max': Decimal('160000.00'),
                'remote': True,
                'visa_sponsorship': True,
                'recruiter': recruiters[3],
            },
            
            # In-person jobs - San Francisco, CA
            {
                'title': 'Frontend Developer',
                'description': 'Join our San Francisco office as a frontend developer. Work on beautiful user interfaces and collaborate with a talented team.',
                'skills_required': 'React, TypeScript, CSS, HTML, Redux',
                'street_address': '1355 Market Street',
                'post_code': '94103',
                'city': 'San Francisco',
                'state': 'CA',
                'country': 'USA',
                'salary_min': Decimal('95000.00'),
                'salary_max': Decimal('140000.00'),
                'remote': False,
                'visa_sponsorship': True,
                'recruiter': recruiters[0],
            },
            {
                'title': 'Backend Engineer',
                'description': 'We are hiring a backend engineer for our San Francisco headquarters. Build robust APIs and scalable systems.',
                'skills_required': 'Java, Spring Boot, PostgreSQL, Redis, Microservices',
                'street_address': '1 Market Plaza',
                'post_code': '94105',
                'city': 'San Francisco',
                'state': 'CA',
                'country': 'USA',
                'salary_min': Decimal('110000.00'),
                'salary_max': Decimal('160000.00'),
                'remote': False,
                'visa_sponsorship': True,
                'recruiter': recruiters[1],
            },
            
            # In-person jobs - New York, NY
            {
                'title': 'Product Manager',
                'description': 'Lead product development at our New York office. Work with engineering and design teams to build amazing products.',
                'skills_required': 'Product Management, Agile, Analytics, Communication',
                'street_address': '350 5th Avenue',
                'post_code': '10118',
                'city': 'New York',
                'state': 'NY',
                'country': 'USA',
                'salary_min': Decimal('120000.00'),
                'salary_max': Decimal('170000.00'),
                'remote': False,
                'visa_sponsorship': False,
                'recruiter': recruiters[2],
            },
            {
                'title': 'UX Designer',
                'description': 'Create beautiful and intuitive user experiences at our New York design studio. Collaborate with cross-functional teams.',
                'skills_required': 'Figma, User Research, Prototyping, Design Systems',
                'street_address': '1 World Trade Center',
                'post_code': '10007',
                'city': 'New York',
                'state': 'NY',
                'country': 'USA',
                'salary_min': Decimal('85000.00'),
                'salary_max': Decimal('130000.00'),
                'remote': False,
                'visa_sponsorship': False,
                'recruiter': recruiters[3],
            },
            
            # In-person jobs - Austin, TX
            {
                'title': 'Software Engineer',
                'description': 'Join our growing Austin office. Work on innovative projects with a collaborative team in a vibrant tech hub.',
                'skills_required': 'Python, JavaScript, React, Node.js, Git',
                'street_address': '300 W 6th Street',
                'post_code': '78701',
                'city': 'Austin',
                'state': 'TX',
                'country': 'USA',
                'salary_min': Decimal('90000.00'),
                'salary_max': Decimal('135000.00'),
                'remote': False,
                'visa_sponsorship': True,
                'recruiter': recruiters[0],
            },
            
            # In-person jobs - Boston, MA
            {
                'title': 'Machine Learning Engineer',
                'description': 'Work on cutting-edge ML projects at our Boston research center. Collaborate with top researchers and engineers.',
                'skills_required': 'Python, PyTorch, TensorFlow, Computer Vision, NLP',
                'street_address': '1 Main Street',
                'post_code': '02129',
                'city': 'Boston',
                'state': 'MA',
                'country': 'USA',
                'salary_min': Decimal('125000.00'),
                'salary_max': Decimal('180000.00'),
                'remote': False,
                'visa_sponsorship': True,
                'recruiter': recruiters[1],
            },
            
            # In-person jobs - Chicago, IL
            {
                'title': 'Cloud Architect',
                'description': 'Design and implement cloud infrastructure solutions at our Chicago office. Lead technical architecture decisions.',
                'skills_required': 'AWS, Azure, Kubernetes, Terraform, System Design',
                'street_address': '233 S Wacker Drive',
                'post_code': '60606',
                'city': 'Chicago',
                'state': 'IL',
                'country': 'USA',
                'salary_min': Decimal('140000.00'),
                'salary_max': Decimal('200000.00'),
                'remote': False,
                'visa_sponsorship': True,
                'recruiter': recruiters[2],
            },
            
            # In-person jobs - Seattle, WA
            {
                'title': 'Mobile Developer',
                'description': 'Build amazing mobile apps for iOS and Android at our Seattle office. Work with modern mobile technologies.',
                'skills_required': 'Swift, Kotlin, React Native, iOS, Android',
                'street_address': '410 Terry Avenue North',
                'post_code': '98109',
                'city': 'Seattle',
                'state': 'WA',
                'country': 'USA',
                'salary_min': Decimal('100000.00'),
                'salary_max': Decimal('150000.00'),
                'remote': False,
                'visa_sponsorship': True,
                'recruiter': recruiters[3],
            },
        ]
        
        # Create job postings
        created_count = 0
        for job_data in test_jobs:
            job = JobPosting.objects.create(
                title=job_data['title'],
                description=job_data['description'],
                skills_required=job_data['skills_required'],
                location=f"{job_data['city']}, {job_data['state']}",  # Keep for backward compatibility
                street_address=job_data['street_address'],
                post_code=job_data['post_code'],
                city=job_data['city'],
                state=job_data['state'],
                country=job_data['country'],
                salary_min=job_data['salary_min'],
                salary_max=job_data['salary_max'],
                remote=job_data['remote'],
                visa_sponsorship=job_data['visa_sponsorship'],
                recruiter=job_data['recruiter'],
                is_draft=False,
                is_closed=False,
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created: {job.title} at {job.recruiter.company_name} ({job.city}, {job.state}) - {"Remote" if job.remote else "In-Person"}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} test job postings!'))
        self.stdout.write(self.style.SUCCESS(f'Total jobs in database: {JobPosting.objects.count()}'))




