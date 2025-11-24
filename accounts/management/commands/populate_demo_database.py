from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Applicant, Recruiter, Project, ApplicantPrivacySettings
from jobs.models import JobPosting, Application
from decimal import Decimal
import json
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create a comprehensive demo database with realistic recruiters, candidates, and job postings with logical matching'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing data before creating new demo data',
        )

    def handle(self, *args, **options):
        if options['clear_existing']:
            self.stdout.write(self.style.WARNING('\nClearing existing data...'))
            Application.objects.all().delete()
            JobPosting.objects.all().delete()
            Project.objects.all().delete()
            ApplicantPrivacySettings.objects.all().delete()
            Applicant.objects.all().delete()
            Recruiter.objects.all().delete()
            # Don't delete all users in case there are admin users
            User.objects.filter(email__contains='@demo.').delete()
            User.objects.filter(email__contains='@example.com').delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing demo data'))

        # Major tech cities with real addresses
        locations = [
            {
                'city': 'San Francisco', 'state': 'CA', 'post_code': '94105', 
                'lat': 37.7749, 'lon': -122.4194,
                'addresses': [
                    '1355 Market Street', '1 Market Plaza', '50 California Street',
                    '101 California Street', '555 Mission Street', '600 Market Street',
                    '1 Market Street', '425 Market Street', '201 Spear Street',
                ]
            },
            {
                'city': 'New York', 'state': 'NY', 'post_code': '10018',
                'lat': 40.7128, 'lon': -74.0060,
                'addresses': [
                    '350 5th Avenue', '1 World Trade Center', '200 Park Avenue',
                    '1 Times Square', '1290 Avenue of the Americas', '40 Wall Street',
                    '55 Water Street', '1 Penn Plaza', '4 World Trade Center',
                ]
            },
            {
                'city': 'Austin', 'state': 'TX', 'post_code': '78701',
                'lat': 30.2672, 'lon': -97.7431,
                'addresses': [
                    '300 W 6th Street', '100 Congress Avenue', '515 Congress Avenue',
                    '200 E Cesar Chavez Street', '98 San Jacinto Boulevard', '301 Congress Avenue',
                    '500 W 2nd Street', '111 Congress Avenue', '600 Congress Avenue',
                ]
            },
            {
                'city': 'Seattle', 'state': 'WA', 'post_code': '98101',
                'lat': 47.6062, 'lon': -122.3321,
                'addresses': [
                    '410 Terry Avenue North', '701 5th Avenue', '999 3rd Avenue',
                    '2001 6th Avenue', '1000 4th Avenue', '500 Union Street',
                    '1301 5th Avenue', '800 5th Avenue', '1201 3rd Avenue',
                ]
            },
            {
                'city': 'Boston', 'state': 'MA', 'post_code': '02110',
                'lat': 42.3601, 'lon': -71.0589,
                'addresses': [
                    '1 Main Street', '1 Federal Street', '200 State Street',
                    '1 International Place', '100 Summer Street', '1 Post Office Square',
                    '200 Clarendon Street', '1 Boston Place', '125 High Street',
                ]
            },
            {
                'city': 'Chicago', 'state': 'IL', 'post_code': '60606',
                'lat': 41.8781, 'lon': -87.6298,
                'addresses': [
                    '233 S Wacker Drive', '200 W Adams Street', '1 N Wacker Drive',
                    '300 N LaSalle Drive', '225 W Wacker Drive', '150 N Riverside Plaza',
                    '111 W Jackson Boulevard', '1 S Wacker Drive', '500 W Madison Street',
                ]
            },
            {
                'city': 'Denver', 'state': 'CO', 'post_code': '80202',
                'lat': 39.7392, 'lon': -104.9903,
                'addresses': [
                    '1801 California Street', '1515 Arapahoe Street', '1200 17th Street',
                    '410 17th Street', '1600 Broadway', '1700 Broadway',
                    '1400 Lawrence Street', '1550 17th Street', '1999 Broadway',
                ]
            },
            {
                'city': 'Los Angeles', 'state': 'CA', 'post_code': '90071',
                'lat': 34.0522, 'lon': -118.2437,
                'addresses': [
                    '333 S Grand Avenue', '515 S Flower Street', '601 S Figueroa Street',
                    '700 S Flower Street', '800 W 1st Street', '550 S Hope Street',
                    '444 S Flower Street', '725 S Figueroa Street', '900 W 1st Street',
                ]
            },
            {
                'city': 'Atlanta', 'state': 'GA', 'post_code': '30303',
                'lat': 33.7490, 'lon': -84.3880,
                'addresses': [
                    '191 Peachtree Street NE', '100 Peachtree Street NW', '250 Piedmont Avenue NE',
                    '1201 W Peachtree Street NE', '55 Park Place NE', '1 Atlantic Center',
                    '303 Peachtree Street NE', '200 Peachtree Street NW', '133 Peachtree Street NE',
                ]
            },
            {
                'city': 'Portland', 'state': 'OR', 'post_code': '97204',
                'lat': 45.5152, 'lon': -122.6784,
                'addresses': [
                    '1000 SW Broadway', '121 SW Salmon Street', '111 SW 5th Avenue',
                    '200 SW Market Street', '888 SW 5th Avenue', '1 SW Columbia Street',
                    '1300 SW 5th Avenue', '500 SW Broadway', '111 SW Columbia Street',
                ]
            },
        ]

        # Realistic first and last names
        first_names = [
            'James', 'Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'Daniel', 'Ashley',
            'Christopher', 'Amanda', 'Matthew', 'Melissa', 'Andrew', 'Nicole', 'Joshua', 'Michelle',
            'Ryan', 'Stephanie', 'Justin', 'Lauren', 'Brandon', 'Rachel', 'Tyler', 'Samantha',
            'Kevin', 'Jennifer', 'Brian', 'Lisa', 'Jonathan', 'Elizabeth', 'Nathan', 'Megan',
            'Robert', 'Kimberly', 'William', 'Amy', 'Joseph', 'Angela', 'Thomas', 'Rebecca'
        ]
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas', 'Taylor',
            'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris', 'Sanchez',
            'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King',
            'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green', 'Adams'
        ]

        # Skill profiles - organized by role type for logical matching
        skill_profiles = {
            'fullstack': [
                'Python, Django, React, PostgreSQL, AWS, Docker',
                'JavaScript, Node.js, React, MongoDB, Express, Git',
                'TypeScript, Next.js, React, Node.js, PostgreSQL, Vercel',
                'Python, Flask, Vue.js, MySQL, Redis, Docker',
                'Java, Spring Boot, React, PostgreSQL, Microservices, Kubernetes',
            ],
            'frontend': [
                'React, TypeScript, CSS, HTML, Redux, Jest',
                'Vue.js, JavaScript, Tailwind CSS, Webpack, Git',
                'Angular, TypeScript, RxJS, SCSS, Jasmine',
                'React, Next.js, TypeScript, Styled Components, Storybook',
            ],
            'backend': [
                'Python, Django, PostgreSQL, Redis, Celery, AWS',
                'Java, Spring Boot, PostgreSQL, Kafka, Docker, Kubernetes',
                'Node.js, Express, MongoDB, GraphQL, Docker, AWS',
                'C#, .NET, SQL Server, Azure, Entity Framework, Docker',
                'Go, PostgreSQL, gRPC, Docker, Kubernetes, AWS',
            ],
            'devops': [
                'Kubernetes, Docker, AWS, Terraform, CI/CD, Jenkins',
                'AWS, Azure, Kubernetes, Terraform, Ansible, GitLab CI',
                'Docker, Kubernetes, AWS, Jenkins, Prometheus, Grafana',
                'Azure, Kubernetes, Terraform, GitHub Actions, Helm',
            ],
            'data_science': [
                'Python, TensorFlow, SQL, Statistics, Machine Learning, Pandas',
                'Python, PyTorch, TensorFlow, Computer Vision, NLP, Scikit-learn',
                'R, Python, SQL, Statistics, Machine Learning, Tableau',
                'Python, Spark, Hadoop, SQL, Machine Learning, Airflow',
            ],
            'mobile': [
                'Swift, Kotlin, React Native, iOS, Android, Git',
                'Swift, Objective-C, iOS, Xcode, Core Data, Firebase',
                'Kotlin, Java, Android, Jetpack Compose, Room, Retrofit',
                'React Native, TypeScript, Redux, Firebase, Jest',
            ],
            'cloud': [
                'AWS, Azure, Kubernetes, Terraform, System Design, Linux',
                'AWS, GCP, Kubernetes, Docker, Terraform, CloudFormation',
                'Azure, AWS, Kubernetes, Terraform, PowerShell, ARM Templates',
            ],
            'security': [
                'Penetration Testing, OWASP, Security Auditing, Python, Linux',
                'Cybersecurity, Network Security, SIEM, Python, Splunk',
                'Application Security, Code Review, Threat Modeling, Python',
            ],
        }

        # Education options with realistic universities
        educations = [
            'Bachelor of Science in Computer Science, MIT',
            'Master of Science in Software Engineering, Stanford University',
            'Bachelor of Science in Computer Science, UC Berkeley',
            'Master of Science in Data Science, Carnegie Mellon University',
            'Bachelor of Science in Computer Engineering, Georgia Tech',
            'Master of Science in Computer Science, University of Washington',
            'Bachelor of Science in Information Systems, University of Texas at Austin',
            'Master of Science in Computer Science, University of Illinois Urbana-Champaign',
            'Bachelor of Science in Computer Science, Cornell University',
            'Master of Business Administration, Harvard Business School',
            'Bachelor of Science in Mathematics and Computer Science, Princeton University',
            'Master of Science in Machine Learning, University of California San Diego',
        ]

        # Experience descriptions matching skill levels
        experiences = {
            'junior': [
                '2 years of experience as a software developer. Strong foundation in programming fundamentals and eager to learn new technologies.',
                '1.5 years developing web applications. Experience with modern frameworks and version control systems.',
                '2 years as a junior developer working on full-stack projects. Passionate about clean code and best practices.',
            ],
            'mid': [
                '4 years of experience building scalable web applications. Proficient in multiple programming languages and frameworks.',
                '5 years as a full-stack developer working with modern JavaScript frameworks and cloud technologies.',
                '4 years in backend development with expertise in microservices architecture and database design.',
                '3 years developing mobile applications for iOS and Android platforms with published apps.',
            ],
            'senior': [
                '7 years in backend development with expertise in microservices architecture. Led a team of 5 engineers.',
                '8 years in DevOps and cloud infrastructure, certified AWS Solutions Architect. Designed scalable systems.',
                '6 years in data science and machine learning, published 3 research papers. Built production ML systems.',
                '7 years as a full-stack engineer. Led multiple product launches and mentored junior developers.',
                '9 years in software engineering. Technical lead on multiple projects, expertise in system design.',
            ],
        }

        # Professional company names
        companies = [
            'TechVenture Solutions', 'CloudScale Innovations', 'DataFlow Systems', 'CodeForge Technologies',
            'NextGen Software', 'Agile Dynamics', 'SmartStack Solutions', 'FutureTech Labs',
            'EliteCode Systems', 'PrimeDev Technologies', 'InnovateHub', 'DigitalCraft Solutions',
            'CloudBridge Inc', 'TechNova Systems', 'DataSphere Technologies', 'CodeCraft Solutions',
            'VelocityTech', 'QuantumSoft Solutions', 'ApexCode Systems', 'NexusTech Innovations',
            'StellarCode Labs', 'InfiniteLoop Technologies', 'ByteForge Solutions', 'CloudVault Systems',
        ]

        # Job definitions with matching skills and descriptions
        job_definitions = [
            {
                'title': 'Senior Full Stack Engineer',
                'skills': 'Python, Django, React, PostgreSQL, AWS, Docker',
                'description': 'We are seeking an experienced full stack engineer to lead development of our core platform. You will architect scalable solutions, mentor junior developers, and work with cutting-edge technologies. This role offers the opportunity to make a significant impact on our product roadmap.',
                'salary_min': 140000, 'salary_max': 200000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'Full Stack Developer',
                'skills': 'JavaScript, Node.js, React, MongoDB, Express, Git',
                'description': 'Join our dynamic team as a full stack developer. You will build and maintain web applications using modern JavaScript technologies. Work on exciting projects in a collaborative, fast-paced environment with opportunities for growth.',
                'salary_min': 95000, 'salary_max': 140000,
                'remote': True, 'visa_sponsorship': False,
            },
            {
                'title': 'Frontend Engineer',
                'skills': 'React, TypeScript, CSS, HTML, Redux, Jest',
                'description': 'Create beautiful and intuitive user interfaces as a frontend engineer. You will work closely with designers and backend engineers to deliver exceptional user experiences. Strong focus on performance and accessibility.',
                'salary_min': 100000, 'salary_max': 150000,
                'remote': False, 'visa_sponsorship': True,
            },
            {
                'title': 'Backend Engineer',
                'skills': 'Python, Django, PostgreSQL, Redis, Celery, AWS',
                'description': 'Build robust and scalable backend systems. You will design APIs, optimize database performance, and work on distributed systems. Experience with microservices architecture is a plus.',
                'salary_min': 110000, 'salary_max': 160000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'Senior Backend Engineer',
                'skills': 'Java, Spring Boot, PostgreSQL, Kafka, Docker, Kubernetes',
                'description': 'Lead backend development initiatives for our enterprise platform. You will architect distributed systems, make technical decisions, and mentor team members. Strong system design skills required.',
                'salary_min': 150000, 'salary_max': 210000,
                'remote': False, 'visa_sponsorship': True,
            },
            {
                'title': 'DevOps Engineer',
                'skills': 'Kubernetes, Docker, AWS, Terraform, CI/CD, Jenkins',
                'description': 'Help us scale our infrastructure and improve our deployment processes. You will work with cloud technologies, automation tools, and ensure high availability of our systems. On-call rotation required.',
                'salary_min': 120000, 'salary_max': 170000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'Data Scientist',
                'skills': 'Python, TensorFlow, SQL, Statistics, Machine Learning, Pandas',
                'description': 'Analyze large datasets and build machine learning models to drive business decisions. You will work with data engineers and product teams to deploy models to production. Strong statistical background required.',
                'salary_min': 115000, 'salary_max': 165000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'Machine Learning Engineer',
                'skills': 'Python, PyTorch, TensorFlow, Computer Vision, NLP, Scikit-learn',
                'description': 'Work on cutting-edge ML projects including computer vision and NLP applications. You will research, prototype, and deploy ML models at scale. Experience with deep learning frameworks essential.',
                'salary_min': 130000, 'salary_max': 190000,
                'remote': False, 'visa_sponsorship': True,
            },
            {
                'title': 'Mobile Developer',
                'skills': 'Swift, Kotlin, React Native, iOS, Android, Git',
                'description': 'Build amazing mobile applications for iOS and Android. You will work with cross-platform frameworks and native technologies to deliver polished user experiences. Published apps in app stores preferred.',
                'salary_min': 105000, 'salary_max': 155000,
                'remote': True, 'visa_sponsorship': False,
            },
            {
                'title': 'Cloud Architect',
                'skills': 'AWS, Azure, Kubernetes, Terraform, System Design, Linux',
                'description': 'Design and implement cloud infrastructure solutions. You will lead technical architecture decisions, optimize costs, and ensure scalability. AWS or Azure certifications preferred.',
                'salary_min': 145000, 'salary_max': 205000,
                'remote': False, 'visa_sponsorship': True,
            },
            {
                'title': 'Software Engineer',
                'skills': 'Python, JavaScript, React, Node.js, Git, Docker',
                'description': 'Work on innovative software projects with a collaborative team. You will build scalable applications, write clean code, and participate in code reviews. Great opportunity for growth and learning.',
                'salary_min': 90000, 'salary_max': 130000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'Senior Frontend Engineer',
                'skills': 'React, Next.js, TypeScript, Styled Components, Storybook',
                'description': 'Lead frontend development and establish best practices for our design system. You will mentor developers, make architectural decisions, and ensure high code quality. Strong leadership skills required.',
                'salary_min': 140000, 'salary_max': 195000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'Full Stack Developer (TypeScript)',
                'skills': 'TypeScript, Next.js, React, Node.js, PostgreSQL, Vercel',
                'description': 'Build modern web applications using TypeScript and Next.js. You will work on both frontend and backend, ensuring type safety and excellent developer experience. Experience with serverless architecture a plus.',
                'salary_min': 100000, 'salary_max': 145000,
                'remote': True, 'visa_sponsorship': False,
            },
            {
                'title': 'Backend Engineer (Node.js)',
                'skills': 'Node.js, Express, MongoDB, GraphQL, Docker, AWS',
                'description': 'Develop scalable backend services using Node.js. You will build RESTful and GraphQL APIs, work with NoSQL databases, and deploy to cloud infrastructure. Experience with microservices preferred.',
                'salary_min': 105000, 'salary_max': 150000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'DevOps Engineer (AWS)',
                'skills': 'AWS, GCP, Kubernetes, Docker, Terraform, CloudFormation',
                'description': 'Manage and optimize our cloud infrastructure on AWS and GCP. You will automate deployments, monitor systems, and ensure reliability. Strong scripting skills and cloud certifications preferred.',
                'salary_min': 125000, 'salary_max': 175000,
                'remote': False, 'visa_sponsorship': True,
            },
            {
                'title': 'Data Engineer',
                'skills': 'Python, Spark, Hadoop, SQL, Machine Learning, Airflow',
                'description': 'Build and maintain data pipelines for our analytics platform. You will work with big data technologies, optimize ETL processes, and ensure data quality. Experience with distributed systems required.',
                'salary_min': 120000, 'salary_max': 170000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'iOS Developer',
                'skills': 'Swift, Objective-C, iOS, Xcode, Core Data, Firebase',
                'description': 'Develop native iOS applications with Swift. You will work on user-facing features, optimize performance, and ensure app store compliance. Published apps and strong portfolio required.',
                'salary_min': 110000, 'salary_max': 160000,
                'remote': False, 'visa_sponsorship': False,
            },
            {
                'title': 'Android Developer',
                'skills': 'Kotlin, Java, Android, Jetpack Compose, Room, Retrofit',
                'description': 'Build native Android applications using Kotlin and modern Android libraries. You will create smooth user experiences, work with Material Design, and optimize app performance.',
                'salary_min': 105000, 'salary_max': 155000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'Security Engineer',
                'skills': 'Penetration Testing, OWASP, Security Auditing, Python, Linux',
                'description': 'Ensure the security of our systems and applications. You will conduct security audits, implement best practices, and respond to security incidents. Security certifications preferred.',
                'salary_min': 130000, 'salary_max': 185000,
                'remote': False, 'visa_sponsorship': True,
            },
            {
                'title': 'Technical Lead',
                'skills': 'Python, Django, React, PostgreSQL, AWS, System Design',
                'description': 'Lead a team of engineers on technical projects. You will make architectural decisions, mentor developers, and ensure delivery of high-quality software. Strong leadership and communication skills required.',
                'salary_min': 155000, 'salary_max': 220000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'Product Engineer',
                'skills': 'JavaScript, React, Node.js, Product Management, Analytics',
                'description': 'Work at the intersection of engineering and product. You will build features, analyze metrics, and work closely with product managers to deliver value to users. Strong product sense required.',
                'salary_min': 115000, 'salary_max': 165000,
                'remote': True, 'visa_sponsorship': False,
            },
            {
                'title': 'Backend Engineer (Go)',
                'skills': 'Go, PostgreSQL, gRPC, Docker, Kubernetes, AWS',
                'description': 'Build high-performance backend services using Go. You will work on distributed systems, optimize for performance, and contribute to our microservices architecture. Experience with concurrency required.',
                'salary_min': 120000, 'salary_max': 170000,
                'remote': True, 'visa_sponsorship': True,
            },
            {
                'title': 'Full Stack Engineer (Vue.js)',
                'skills': 'Python, Flask, Vue.js, MySQL, Redis, Docker',
                'description': 'Develop full-stack applications using Python and Vue.js. You will work on both frontend and backend, ensuring seamless integration and excellent user experience. Modern development practices required.',
                'salary_min': 95000, 'salary_max': 140000,
                'remote': False, 'visa_sponsorship': True,
            },
        ]

        # Create 25 recruiters
        self.stdout.write(self.style.WARNING('\n=== Creating Recruiters ==='))
        recruiters = []
        used_companies = set()
        
        for i in range(25):
            # Ensure unique company names
            company = random.choice(companies)
            attempts = 0
            while company in used_companies and attempts < 50:
                company = random.choice(companies)
                attempts += 1
            used_companies.add(company)
            
            loc = random.choice(locations)
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            # Create unique email
            company_slug = company.lower().replace(' ', '').replace('.', '').replace('inc', '')
            email = f"{company_slug}{i}@demo.hiremap.com"
            username = email
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            
            # Check if recruiter already exists, if not create with raw SQL to include country field
            try:
                recruiter = Recruiter.objects.get(user=user)
                created = False
            except Recruiter.DoesNotExist:
                # Use raw SQL to insert with all fields including country (exists in DB but not in model)
                from django.db import connection
                from django.conf import settings
                street_addr = random.choice(loc['addresses'])
                
                # Temporarily disable SQL debugging to avoid formatting issues
                old_debug = settings.DEBUG
                settings.DEBUG = False
                try:
                    with connection.cursor() as cursor:
                        params = [user.id, first_name, last_name, company, f"{loc['city']}, {loc['state']}", 
                                 street_addr, loc['city'], loc['state'], loc['post_code'], 'USA']
                        sql = "INSERT INTO accounts_recruiter (user_id, first_name, last_name, company_name, location, street_address, city, state, post_code, country) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                        cursor.execute(sql, params)
                finally:
                    settings.DEBUG = old_debug
                    
                recruiter = Recruiter.objects.get(user=user)
                created = True
            recruiters.append(recruiter)
            if created:
                self.stdout.write(f'  [OK] Created: {company} - {first_name} {last_name} ({loc["city"]}, {loc["state"]})')

        # Create 25 applicants with matching skills
        self.stdout.write(self.style.WARNING('\n=== Creating Candidates ==='))
        applicants = []
        availability_options = ['available', 'open-to-work', 'open-to-work', 'open-to-work', 'not-looking']  # Weighted
        
        # Create candidates that match job requirements
        candidate_profiles = []
        for job_def in job_definitions[:20]:  # Use first 20 job definitions
            skill_profile_type = None
            for profile_type, skills_list in skill_profiles.items():
                if any(skill in job_def['skills'] for skill in skills_list[0].split(', ')[:2]):
                    skill_profile_type = profile_type
                    break
            
            if not skill_profile_type:
                skill_profile_type = 'fullstack'  # Default
            
            candidate_profiles.append({
                'skills': job_def['skills'],
                'skill_type': skill_profile_type,
                'experience_level': 'senior' if 'Senior' in job_def['title'] or 'Lead' in job_def['title'] or 'Architect' in job_def['title'] else ('mid' if 'Engineer' in job_def['title'] or 'Developer' in job_def['title'] else 'junior'),
            })
        
        # Add 5 more diverse candidates
        for _ in range(5):
            profile_type = random.choice(list(skill_profiles.keys()))
            candidate_profiles.append({
                'skills': random.choice(skill_profiles[profile_type]),
                'skill_type': profile_type,
                'experience_level': random.choice(['junior', 'mid', 'senior']),
            })
        
        for i, profile in enumerate(candidate_profiles):
            loc = random.choice(locations)
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@demo.hiremap.com"
            username = email
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            
            # Create links as JSON
            links_data = []
            if random.random() > 0.2:  # 80% have LinkedIn
                links_data.append({'name': 'LinkedIn', 'url': f'https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{i}'})
            if random.random() > 0.3:  # 70% have GitHub
                links_data.append({'name': 'GitHub', 'url': f'https://github.com/{first_name.lower()}{last_name.lower()}{i}'})
            if random.random() > 0.6:  # 40% have Portfolio
                links_data.append({'name': 'Portfolio', 'url': f'https://{first_name.lower()}{last_name.lower()}{i}.dev'})
            links_json = json.dumps(links_data) if links_data else ''
            
            applicant, created = Applicant.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'skills': profile['skills'],
                    'education': random.choice(educations),
                    'experience': random.choice(experiences[profile['experience_level']]),
                    'links': links_json,
                    'phone': f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
                    'street_address': random.choice(loc['addresses']),
                    'city': loc['city'],
                    'state': loc['state'],
                    'post_code': loc['post_code'],
                    'country': 'USA',
                    'location': f"{loc['city']}, {loc['state']}",
                    'location_lat': loc['lat'] + random.uniform(-0.05, 0.05),
                    'location_lon': loc['lon'] + random.uniform(-0.05, 0.05),
                    'availability': random.choice(availability_options),
                }
            )
            
            # Create privacy settings
            ApplicantPrivacySettings.objects.get_or_create(
                applicant=applicant,
                defaults={
                    'show_skills': True,
                    'show_education': True,
                    'show_experience': True,
                    'show_projects': True,
                    'show_links': True,
                    'show_phone': random.choice([True, False]),
                    'show_location': True,
                    'show_availability': True,
                    'allow_email_contact': True,
                }
            )
            
            # Create 1-3 projects for most applicants
            if random.random() > 0.25:  # 75% have projects
                num_projects = random.randint(1, 3)
                project_templates = [
                    {'title': 'E-Commerce Platform', 'desc': 'A full-stack e-commerce platform with payment integration, inventory management, and admin dashboard.', 'tech': 'React, Node.js, MongoDB, Stripe'},
                    {'title': 'Task Management App', 'desc': 'A collaborative task management application with real-time updates, notifications, and team collaboration features.', 'tech': 'React, Django, PostgreSQL, WebSockets'},
                    {'title': 'Weather Dashboard', 'desc': 'A weather dashboard showing forecasts, historical data, and interactive maps with location-based services.', 'tech': 'Vue.js, Express, MySQL, OpenWeather API'},
                    {'title': 'Social Media Clone', 'desc': 'A social media platform with posts, comments, likes, and real-time messaging features.', 'tech': 'React, Node.js, MongoDB, Socket.io'},
                    {'title': 'Blog Platform', 'desc': 'A modern blog platform with markdown support, comments, tags, and search functionality.', 'tech': 'Next.js, TypeScript, PostgreSQL, Prisma'},
                    {'title': 'Chat Application', 'desc': 'A real-time chat application with multiple rooms, file sharing, and message history.', 'tech': 'React Native, Firebase, Node.js'},
                    {'title': 'Analytics Dashboard', 'desc': 'An analytics dashboard with data visualization, custom reports, and real-time metrics.', 'tech': 'React, Python, PostgreSQL, D3.js'},
                    {'title': 'API Gateway', 'desc': 'An API gateway for microservices architecture with authentication, rate limiting, and load balancing.', 'tech': 'Node.js, Express, Redis, Docker'},
                    {'title': 'Authentication System', 'desc': 'A secure authentication system with OAuth support, 2FA, and session management.', 'tech': 'Django, PostgreSQL, JWT, OAuth2'},
                    {'title': 'ML Model API', 'desc': 'A RESTful API for serving machine learning models with batch processing and real-time predictions.', 'tech': 'Python, Flask, TensorFlow, Redis'},
                ]
                
                for j in range(num_projects):
                    proj = random.choice(project_templates)
                    Project.objects.create(
                        applicant=applicant,
                        title=proj['title'],
                        description=proj['desc'],
                        technologies=proj['tech'],
                        url=f'https://github.com/{first_name.lower()}{last_name.lower()}{i}/{proj["title"].lower().replace(" ", "-")}' if random.random() > 0.3 else '',
                    )
            
            applicants.append(applicant)
            if created:
                exp_level = profile['experience_level'].title()
                self.stdout.write(f'  [OK] Created: {first_name} {last_name} - {exp_level} ({loc["city"]}, {loc["state"]}) - {profile["skill_type"].replace("_", " ").title()}')

        # Create 25 job postings with logical distribution
        self.stdout.write(self.style.WARNING('\n=== Creating Job Postings ==='))
        jobs = []
        
        # Use job definitions and create variations
        for i, job_def in enumerate(job_definitions[:23]):  # Use 23 job definitions
            recruiter = random.choice(recruiters)
            loc = random.choice(locations)
            
            # Vary remote status - 60% remote, 40% in-person
            is_remote = random.random() < 0.6
            
            # Vary visa sponsorship - 70% offer it
            visa_sponsorship = random.random() < 0.7
            
            # Add some variation to salary
            salary_variance = random.uniform(0.95, 1.05)
            salary_min = Decimal(int(job_def['salary_min'] * salary_variance))
            salary_max = Decimal(int(job_def['salary_max'] * salary_variance))
            
            job = JobPosting.objects.create(
                title=job_def['title'],
                description=job_def['description'],
                skills_required=job_def['skills'],
                location=f"{loc['city']}, {loc['state']}",
                street_address=random.choice(loc['addresses']),
                city=loc['city'],
                state=loc['state'],
                post_code=loc['post_code'],
                country='USA',
                location_lat=loc['lat'] + random.uniform(-0.02, 0.02),
                location_lon=loc['lon'] + random.uniform(-0.02, 0.02),
                salary_min=salary_min,
                salary_max=salary_max,
                remote=is_remote,
                visa_sponsorship=visa_sponsorship,
                recruiter=recruiter,
                is_draft=False,
                is_closed=False,
                created_at=datetime.now() - timedelta(days=random.randint(0, 90)),
            )
            jobs.append(job)
            self.stdout.write(f'  [OK] Created: {job_def["title"]} at {recruiter.company_name} ({loc["city"]}, {loc["state"]}) - {"Remote" if is_remote else "In-Person"} - ${salary_min:,.0f}-${salary_max:,.0f}')

        # Create 2 more jobs with random combinations
        for i in range(2):
            recruiter = random.choice(recruiters)
            loc = random.choice(locations)
            job_def = random.choice(job_definitions)
            
            is_remote = random.random() < 0.6
            visa_sponsorship = random.random() < 0.7
            salary_variance = random.uniform(0.95, 1.05)
            salary_min = Decimal(int(job_def['salary_min'] * salary_variance))
            salary_max = Decimal(int(job_def['salary_max'] * salary_variance))
            
            job = JobPosting.objects.create(
                title=job_def['title'],
                description=job_def['description'],
                skills_required=job_def['skills'],
                location=f"{loc['city']}, {loc['state']}",
                street_address=random.choice(loc['addresses']),
                city=loc['city'],
                state=loc['state'],
                post_code=loc['post_code'],
                country='USA',
                location_lat=loc['lat'] + random.uniform(-0.02, 0.02),
                location_lon=loc['lon'] + random.uniform(-0.02, 0.02),
                salary_min=salary_min,
                salary_max=salary_max,
                remote=is_remote,
                visa_sponsorship=visa_sponsorship,
                recruiter=recruiter,
                is_draft=False,
                is_closed=False,
                created_at=datetime.now() - timedelta(days=random.randint(0, 90)),
            )
            jobs.append(job)
            self.stdout.write(f'  [OK] Created: {job_def["title"]} at {recruiter.company_name} ({loc["city"]}, {loc["state"]}) - {"Remote" if is_remote else "In-Person"}')

        # Create some applications to show relationships
        self.stdout.write(self.style.WARNING('\n=== Creating Applications ==='))
        application_count = 0
        
        # Create applications where candidate skills match job requirements
        for applicant in applicants:
            # Each candidate applies to 2-5 jobs that match their skills
            num_applications = random.randint(2, 5)
            applicant_skills = set(skill.strip() for skill in applicant.skills.split(',') if skill.strip())
            
            matching_jobs = []
            for job in jobs:
                job_skills = set(skill.strip() for skill in job.skills_required.split(',') if skill.strip())
                # Check if there's skill overlap
                if applicant_skills & job_skills:  # Intersection
                    matching_jobs.append(job)
            
            # If no perfect matches, just pick random jobs
            if not matching_jobs:
                matching_jobs = random.sample(jobs, min(num_applications, len(jobs)))
            else:
                matching_jobs = random.sample(matching_jobs, min(num_applications, len(matching_jobs)))
            
            for job in matching_jobs:
                # Skip if already applied
                if Application.objects.filter(applicant=applicant, listing=job).exists():
                    continue
                
                # Different application stages
                stages = ['Applied', 'Applied', 'Applied', 'Under Review', 'Interview', 'Offer']
                status = random.choice(stages)
                
                messages = [
                    'I am very interested in this position and believe my skills align well with your requirements.',
                    'I would love to discuss how my experience can contribute to your team.',
                    'This role seems like a perfect fit for my background and career goals.',
                    '',
                    '',
                ]
                
                Application.objects.create(
                    applicant=applicant,
                    listing=job,
                    status=status,
                    message=random.choice(messages),
                    created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
                )
                application_count += 1
        
        self.stdout.write(f'  [OK] Created {application_count} applications')

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('DEMO DATABASE CREATED SUCCESSFULLY!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'  • Recruiters: {len(recruiters)}')
        self.stdout.write(f'  • Candidates: {len(applicants)}')
        self.stdout.write(f'  • Job Postings: {len(jobs)}')
        self.stdout.write(f'  • Applications: {application_count}')
        self.stdout.write(f'  • Projects: {Project.objects.count()}')
        self.stdout.write(f'\nDatabase Totals:')
        self.stdout.write(f'  • Total Users: {User.objects.count()}')
        self.stdout.write(f'  • Total Jobs: {JobPosting.objects.count()}')
        self.stdout.write(f'  • Total Applications: {Application.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Demo database is ready for your presentation!'))

