from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Applicant, Recruiter, Project, ApplicantPrivacySettings
from jobs.models import JobPosting
from decimal import Decimal
import json
import random


class Command(BaseCommand):
    help = 'Create 20 test users (applicants and recruiters) and 20 job postings'

    def handle(self, *args, **options):
        # Cities and states for variety
        locations = [
            {'city': 'San Francisco', 'state': 'CA', 'post_code': '94102'},
            {'city': 'New York', 'state': 'NY', 'post_code': '10001'},
            {'city': 'Austin', 'state': 'TX', 'post_code': '78701'},
            {'city': 'Seattle', 'state': 'WA', 'post_code': '98101'},
            {'city': 'Boston', 'state': 'MA', 'post_code': '02101'},
            {'city': 'Chicago', 'state': 'IL', 'post_code': '60601'},
            {'city': 'Denver', 'state': 'CO', 'post_code': '80202'},
            {'city': 'Los Angeles', 'state': 'CA', 'post_code': '90001'},
        ]
        
        # First names and last names
        first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn', 'Sage', 'River', 'Dakota', 'Phoenix', 'Blake', 'Cameron', 'Drew', 'Emery', 'Finley', 'Hayden', 'Jamie', 'Kai']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee']
        
        # Skills lists
        tech_skills = [
            'Python, Django, React, PostgreSQL, AWS',
            'JavaScript, Node.js, React, MongoDB, Docker',
            'Java, Spring Boot, PostgreSQL, Redis, Microservices',
            'Python, TensorFlow, SQL, Statistics, Machine Learning',
            'React, TypeScript, CSS, HTML, Redux',
            'Swift, Kotlin, React Native, iOS, Android',
            'Kubernetes, Docker, AWS, Terraform, CI/CD',
            'Python, PyTorch, TensorFlow, Computer Vision, NLP',
            'AWS, Azure, Kubernetes, Terraform, System Design',
            'C++, Python, Embedded Systems, Linux, Git',
        ]
        
        # Education options
        educations = [
            'Bachelor of Science in Computer Science, MIT',
            'Master of Science in Software Engineering, Stanford University',
            'Bachelor of Science in Information Systems, UC Berkeley',
            'Master of Science in Data Science, Carnegie Mellon',
            'Bachelor of Science in Computer Engineering, Georgia Tech',
            'Master of Business Administration, Harvard Business School',
            'Bachelor of Science in Mathematics, Princeton University',
        ]
        
        # Experience options
        experiences = [
            '5 years of experience building scalable web applications. Led a team of 5 engineers.',
            '3 years developing mobile applications for iOS and Android platforms.',
            '7 years in backend development with expertise in microservices architecture.',
            '4 years as a full-stack developer working with modern JavaScript frameworks.',
            '6 years in data science and machine learning, published 3 research papers.',
            '2 years as a junior developer, eager to grow and learn new technologies.',
            '8 years in DevOps and cloud infrastructure, certified AWS Solutions Architect.',
        ]
        
        # Company names
        companies = [
            'TechCorp Solutions', 'Innovate Labs', 'Digital Dynamics', 'Cloud Systems Inc',
            'DataFlow Technologies', 'CodeForge', 'NextGen Software', 'Agile Innovations',
            'Smart Solutions Group', 'Future Tech', 'Elite Systems', 'Prime Development',
        ]
        
        # Job titles
        job_titles = [
            'Senior Software Engineer', 'Full Stack Developer', 'DevOps Engineer', 'Data Scientist',
            'Frontend Developer', 'Backend Engineer', 'Product Manager', 'UX Designer',
            'Software Engineer', 'Machine Learning Engineer', 'Cloud Architect', 'Mobile Developer',
            'Security Engineer', 'QA Engineer', 'Technical Lead', 'Systems Administrator',
            'Database Administrator', 'Network Engineer', 'Business Analyst', 'Scrum Master',
        ]
        
        # Job descriptions
        job_descriptions = [
            'We are looking for an experienced software engineer to join our team. You will work on building scalable web applications using modern technologies.',
            'Join our team as a full stack developer. Work on exciting projects with cutting-edge technologies in a collaborative environment.',
            'We need a DevOps engineer to help us scale our infrastructure. Work with cloud technologies and automation tools.',
            'Looking for a data scientist to analyze large datasets and build machine learning models. Work with cutting-edge AI technologies.',
            'Join our team as a frontend developer. Create beautiful user interfaces and collaborate with design teams.',
            'We are hiring a backend engineer. Build robust APIs and scalable systems using modern frameworks.',
            'Lead product development initiatives. Work with engineering and design teams to build amazing products.',
            'Create beautiful and intuitive user experiences. Collaborate with cross-functional teams on design projects.',
            'Work on innovative software projects with a collaborative team. Build scalable applications.',
            'Work on cutting-edge ML projects. Collaborate with top researchers and engineers.',
            'Design and implement cloud infrastructure solutions. Lead technical architecture decisions.',
            'Build amazing mobile apps for iOS and Android. Work with modern mobile technologies.',
            'Ensure the security of our systems and applications. Conduct security audits and implement best practices.',
            'Test and ensure quality of our software products. Work with development teams to improve code quality.',
            'Lead a team of engineers on technical projects. Make architectural decisions and mentor junior developers.',
            'Maintain and optimize our IT infrastructure. Ensure systems are running smoothly and efficiently.',
            'Manage and optimize our database systems. Ensure data integrity and performance.',
            'Design and maintain our network infrastructure. Troubleshoot network issues and optimize performance.',
            'Analyze business requirements and translate them into technical solutions. Work with stakeholders.',
            'Facilitate agile development processes. Help teams deliver high-quality software efficiently.',
        ]
        
        # Create 10 recruiters
        self.stdout.write(self.style.WARNING('\nCreating 10 recruiters...'))
        recruiters = []
        for i in range(10):
            loc = random.choice(locations)
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            company = random.choice(companies)
            email = f"{company.lower().replace(' ', '').replace('.', '')}@example.com"
            username = email
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            
            recruiter, created = Recruiter.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'company_name': company,
                    'street_address': f"{random.randint(100, 9999)} Main Street",
                    'city': loc['city'],
                    'state': loc['state'],
                    'post_code': loc['post_code'],
                    'country': 'USA',
                }
            )
            recruiters.append(recruiter)
            if created:
                self.stdout.write(f'  [OK] Created recruiter: {company} ({loc["city"]}, {loc["state"]})')
        
        # Create 10 applicants
        self.stdout.write(self.style.WARNING('\nCreating 10 applicants...'))
        applicants = []
        availability_options = ['available', 'open-to-work', 'not-looking']
        
        for i in range(10):
            loc = random.choice(locations)
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
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
            if random.random() > 0.3:  # 70% chance of having LinkedIn
                links_data.append({'name': 'LinkedIn', 'url': f'https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}'})
            if random.random() > 0.4:  # 60% chance of having GitHub
                links_data.append({'name': 'GitHub', 'url': f'https://github.com/{first_name.lower()}{last_name.lower()}'})
            if random.random() > 0.7:  # 30% chance of having Portfolio
                links_data.append({'name': 'Portfolio', 'url': f'https://{first_name.lower()}{last_name.lower()}.com'})
            links_json = json.dumps(links_data) if links_data else ''
            
            applicant, created = Applicant.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'skills': random.choice(tech_skills),
                    'education': random.choice(educations),
                    'experience': random.choice(experiences),
                    'links': links_json,
                    'phone': f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
                    'street_address': f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Park', 'Maple', 'Cedar'])} Street",
                    'city': loc['city'],
                    'state': loc['state'],
                    'post_code': loc['post_code'],
                    'country': 'USA',
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
            
            # Create 1-3 projects for some applicants
            if random.random() > 0.3:  # 70% chance of having projects
                num_projects = random.randint(1, 3)
                project_titles = [
                    'E-Commerce Platform', 'Task Management App', 'Weather Dashboard',
                    'Social Media Clone', 'Blog Platform', 'Chat Application',
                    'Analytics Dashboard', 'API Gateway', 'Authentication System',
                ]
                project_descriptions = [
                    'A full-stack e-commerce platform with payment integration.',
                    'A task management application with real-time updates.',
                    'A weather dashboard showing forecasts and historical data.',
                    'A social media platform with posts, comments, and likes.',
                    'A blog platform with markdown support and comments.',
                    'A real-time chat application with multiple rooms.',
                    'An analytics dashboard with data visualization.',
                    'An API gateway for microservices architecture.',
                    'A secure authentication system with OAuth support.',
                ]
                project_techs = [
                    'React, Node.js, MongoDB', 'Django, PostgreSQL, React',
                    'Python, Flask, SQLite', 'Vue.js, Express, MySQL',
                    'Angular, Spring Boot, PostgreSQL', 'React Native, Firebase',
                ]
                
                for j in range(num_projects):
                    Project.objects.create(
                        applicant=applicant,
                        title=random.choice(project_titles),
                        description=random.choice(project_descriptions),
                        technologies=random.choice(project_techs),
                        url=f'https://github.com/{first_name.lower()}{last_name.lower()}/project{j+1}' if random.random() > 0.3 else '',
                    )
            
            applicants.append(applicant)
            if created:
                self.stdout.write(f'  [OK] Created applicant: {first_name} {last_name} ({loc["city"]}, {loc["state"]})')
        
        # Create 20 job postings
        self.stdout.write(self.style.WARNING('\nCreating 20 job postings...'))
        created_count = 0
        
        for i in range(20):
            recruiter = random.choice(recruiters)
            loc = random.choice(locations)
            title = random.choice(job_titles)
            description = random.choice(job_descriptions)
            skills = random.choice(tech_skills)
            
            # Mix of remote and in-person
            is_remote = random.random() > 0.5
            
            # Salary ranges based on title
            if 'Senior' in title or 'Lead' in title or 'Architect' in title:
                salary_min = Decimal(random.randint(130000, 150000))
                salary_max = Decimal(random.randint(180000, 220000))
            elif 'Manager' in title:
                salary_min = Decimal(random.randint(120000, 140000))
                salary_max = Decimal(random.randint(170000, 200000))
            else:
                salary_min = Decimal(random.randint(80000, 110000))
                salary_max = Decimal(random.randint(130000, 160000))
            
            job = JobPosting.objects.create(
                title=title,
                description=description,
                skills_required=skills,
                location=f"{loc['city']}, {loc['state']}",  # Keep for backward compatibility
                street_address=f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Park', 'Maple', 'Cedar'])} Street",
                city=loc['city'],
                state=loc['state'],
                post_code=loc['post_code'],
                country='USA',
                salary_min=salary_min,
                salary_max=salary_max,
                remote=is_remote,
                visa_sponsorship=random.choice([True, False]),
                recruiter=recruiter,
                is_draft=False,
                is_closed=False,
            )
            created_count += 1
            self.stdout.write(f'  [OK] Created: {title} at {recruiter.company_name} ({loc["city"]}, {loc["state"]}) - {"Remote" if is_remote else "In-Person"}')
        
        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Successfully created:'))
        self.stdout.write(f'  - {len(recruiters)} Recruiters')
        self.stdout.write(f'  - {len(applicants)} Applicants')
        self.stdout.write(f'  - {created_count} Job Postings')
        self.stdout.write(f'  - {Project.objects.count()} Projects')
        self.stdout.write(f'\nTotal in database:')
        self.stdout.write(f'  - Users: {User.objects.count()}')
        self.stdout.write(f'  - Jobs: {JobPosting.objects.count()}')

