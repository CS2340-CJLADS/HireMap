from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Applicant, Recruiter, Project, ApplicantPrivacySettings
from jobs.models import JobPosting, Application
from decimal import Decimal
import json
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Flood the app with demo data for a specific user (recruiter or applicant) for demo videos'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='Username or email of the user to flood data for',
        )
        parser.add_argument(
            '--candidates',
            type=int,
            default=100,
            help='Number of candidates to create (for recruiters)',
        )
        parser.add_argument(
            '--jobs',
            type=int,
            default=50,
            help='Number of job postings to create (for recruiters)',
        )
        parser.add_argument(
            '--applications',
            type=int,
            default=30,
            help='Number of applications to create (for applicants)',
        )
        parser.add_argument(
            '--projects',
            type=int,
            default=10,
            help='Number of projects to create (for applicants)',
        )
        parser.add_argument(
            '--clear-demo',
            action='store_true',
            help='Clear all demo data (@demo.com users) before creating new data',
        )

    def handle(self, *args, **options):
        username = options['username']
        num_candidates = options['candidates']
        num_jobs = options['jobs']
        num_applications = options['applications']
        num_projects = options['projects']
        clear_demo = options['clear_demo']

        # Clear demo data if requested
        if clear_demo:
            self.stdout.write(self.style.WARNING('\n=== Clearing Demo Data ==='))
            
            # Delete applications from demo users
            demo_users = User.objects.filter(email__contains='@demo.com')
            if demo_users.exists():
                Application.objects.filter(applicant__user__in=demo_users).delete()
                Application.objects.filter(listing__recruiter__user__in=demo_users).delete()
                self.stdout.write('  [OK] Deleted demo applications')
            
            # Delete job postings from demo recruiters
            demo_recruiters = Recruiter.objects.filter(user__email__contains='@demo.com')
            if demo_recruiters.exists():
                JobPosting.objects.filter(recruiter__in=demo_recruiters).delete()
                self.stdout.write('  [OK] Deleted demo job postings')
            
            # Delete projects from demo applicants
            demo_applicants = Applicant.objects.filter(user__email__contains='@demo.com')
            if demo_applicants.exists():
                Project.objects.filter(applicant__in=demo_applicants).delete()
                ApplicantPrivacySettings.objects.filter(applicant__in=demo_applicants).delete()
                self.stdout.write('  [OK] Deleted demo projects and privacy settings')
            
            # Delete demo users (this will cascade delete applicants/recruiters)
            deleted_count = demo_users.delete()[0]
            if deleted_count > 0:
                self.stdout.write(f'  [OK] Deleted {deleted_count} demo users')
            
            self.stdout.write(self.style.SUCCESS('Demo data cleared!\n'))

        # Find the user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" not found!'))
            return

        # Determine if user is recruiter or applicant
        is_recruiter = hasattr(user, 'recruiter')
        is_applicant = hasattr(user, 'applicant')

        if not is_recruiter and not is_applicant:
            self.stdout.write(self.style.ERROR(f'User "{username}" is neither a recruiter nor an applicant!'))
            return

        self.stdout.write(self.style.SUCCESS(f'\n=== Flooding Demo Data for {username} ==='))
        self.stdout.write(f'User Type: {"Recruiter" if is_recruiter else "Applicant"}\n')

        # Locations data
        locations = [
            {'city': 'San Francisco', 'state': 'CA', 'post_code': '94105', 'lat': 37.7749, 'lon': -122.4194},
            {'city': 'New York', 'state': 'NY', 'post_code': '10018', 'lat': 40.7128, 'lon': -74.0060},
            {'city': 'Austin', 'state': 'TX', 'post_code': '78701', 'lat': 30.2672, 'lon': -97.7431},
            {'city': 'Seattle', 'state': 'WA', 'post_code': '98101', 'lat': 47.6062, 'lon': -122.3321},
            {'city': 'Boston', 'state': 'MA', 'post_code': '02110', 'lat': 42.3601, 'lon': -71.0589},
            {'city': 'Chicago', 'state': 'IL', 'post_code': '60606', 'lat': 41.8781, 'lon': -87.6298},
            {'city': 'Denver', 'state': 'CO', 'post_code': '80202', 'lat': 39.7392, 'lon': -104.9903},
            {'city': 'Los Angeles', 'state': 'CA', 'post_code': '90001', 'lat': 34.0522, 'lon': -118.2437},
            {'city': 'Miami', 'state': 'FL', 'post_code': '33101', 'lat': 25.7617, 'lon': -80.1918},
            {'city': 'Portland', 'state': 'OR', 'post_code': '97201', 'lat': 45.5152, 'lon': -122.6784},
        ]

        # Tech skills
        tech_skills = [
            'Python', 'JavaScript', 'Java', 'React', 'Node.js', 'Django', 'Flask', 'Vue.js',
            'Angular', 'TypeScript', 'SQL', 'PostgreSQL', 'MongoDB', 'AWS', 'Docker', 'Kubernetes',
            'Git', 'REST API', 'GraphQL', 'Microservices', 'Machine Learning', 'Data Science',
            'TensorFlow', 'PyTorch', 'C++', 'C#', 'Go', 'Rust', 'Swift', 'Kotlin', 'PHP',
            'Ruby', 'Ruby on Rails', 'Spring Boot', 'Express.js', 'Next.js', 'Nuxt.js',
            'Redux', 'MobX', 'Jest', 'Cypress', 'Selenium', 'CI/CD', 'Jenkins', 'GitHub Actions',
            'Terraform', 'Ansible', 'Linux', 'System Design', 'Agile', 'Scrum'
        ]

        # Job titles
        job_titles = [
            'Senior Software Engineer', 'Full Stack Developer', 'Backend Engineer', 'Frontend Developer',
            'DevOps Engineer', 'Data Engineer', 'Machine Learning Engineer', 'Software Architect',
            'Product Manager', 'Technical Lead', 'Engineering Manager', 'Cloud Engineer',
            'Security Engineer', 'Mobile Developer', 'QA Engineer', 'Site Reliability Engineer',
            'Solutions Architect', 'Platform Engineer', 'API Developer', 'Blockchain Developer'
        ]

        # First and last names
        first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn', 'Sage',
                      'River', 'Dakota', 'Phoenix', 'Blake', 'Cameron', 'Drew', 'Emery', 'Finley',
                      'Hayden', 'Jamie', 'Kai', 'Sam', 'Chris', 'Pat', 'Dana', 'Lee', 'Max', 'Noah',
                      'Emma', 'Olivia', 'Sophia', 'Isabella', 'Mia', 'Charlotte', 'Amelia', 'Harper',
                      'Evelyn', 'Abigail', 'Emily', 'Elizabeth', 'Sofia', 'Avery', 'Ella', 'Madison']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                     'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas',
                     'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris',
                     'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'King']

        # Company names
        company_names = [
            'TechCorp', 'InnovateLabs', 'StartupXYZ', 'BigTech Inc', 'CloudSolutions', 'DataDriven Co',
            'CodeMasters', 'DevOps Pro', 'AI Innovations', 'FutureTech', 'NextGen Systems', 'SmartCode',
            'Digital Dynamics', 'TechVenture', 'CodeForge', 'Innovation Hub', 'TechStart', 'DevStudio',
            'CodeWorks', 'TechFlow', 'DataStream', 'CloudNine', 'TechBridge', 'CodeCraft', 'DevLab'
        ]

        if is_recruiter:
            recruiter = user.recruiter
            self.stdout.write(self.style.WARNING(f'\n=== Creating {num_jobs} Job Postings ==='))
            
            # Create lots of job postings
            job_postings = []
            for i in range(num_jobs):
                loc = random.choice(locations)
                job_title = random.choice(job_titles)
                
                # Select relevant skills for the job
                num_skills = random.randint(3, 8)
                required_skills = random.sample(tech_skills, num_skills)
                skills_text = ', '.join(required_skills)
                
                # Salary range
                base_salary = random.randint(80000, 180000)
                salary_min = Decimal(str(base_salary))
                salary_max = Decimal(str(base_salary + random.randint(20000, 50000)))
                
                # Job description
                description = f"""
We are looking for a talented {job_title} to join our growing team. 

Key Responsibilities:
- Design and develop scalable software solutions
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews and technical discussions
- Contribute to architectural decisions

Required Skills: {skills_text}

This is an exciting opportunity to work on cutting-edge technology and make a real impact. We offer competitive compensation, comprehensive benefits, and a great work environment.
                """.strip()
                
                job = JobPosting.objects.create(
                    recruiter=recruiter,
                    title=job_title,
                    description=description,
                    skills_required=skills_text,
                    street_address=f"{random.randint(100, 999)} Main Street",
                    city=loc['city'],
                    state=loc['state'],
                    post_code=loc['post_code'],
                    country='USA',
                    location_lat=loc['lat'],
                    location_lon=loc['lon'],
                    salary_min=salary_min,
                    salary_max=salary_max,
                    remote=random.choice([True, False, False, False]),  # 25% remote
                    visa_sponsorship=random.choice([True, False]),
                    visibility='public',
                    is_draft=False,
                    is_closed=random.choice([False, False, False, True])  # 25% closed
                )
                job_postings.append(job)
                
                if (i + 1) % 10 == 0:
                    self.stdout.write(f'  Created {i + 1}/{num_jobs} job postings...')
            
            self.stdout.write(self.style.SUCCESS(f'✓ Created {len(job_postings)} job postings'))
            
            # Create candidates with applications
            self.stdout.write(self.style.WARNING(f'\n=== Creating {num_candidates} Candidates with Applications ==='))
            
            applicants_created = 0
            applications_created = 0
            
            for i in range(num_candidates):
                loc = random.choice(locations)
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                email = f"candidate.{first_name.lower()}.{last_name.lower()}.{i}@demo.com"
                username = email
                
                # Create user
                user_obj, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                    }
                )
                
                if not created:
                    continue
                
                # Select skills
                num_skills = random.randint(4, 10)
                candidate_skills = random.sample(tech_skills, num_skills)
                skills_text = ', '.join(candidate_skills)
                
                # Education
                education_levels = [
                    "Bachelor's in Computer Science, MIT",
                    "Master's in Software Engineering, Stanford University",
                    "Bachelor's in Information Systems, UC Berkeley",
                    "PhD in Computer Science, Carnegie Mellon",
                    "Bachelor's in Computer Engineering, Georgia Tech",
                    "Master's in Data Science, NYU",
                    "Bachelor's in Software Development, University of Washington"
                ]
                
                # Experience
                years_exp = random.randint(1, 10)
                experience_text = f"{years_exp} years of experience in software development. Specialized in {', '.join(candidate_skills[:3])}."
                
                # Links
                links_data = []
                if random.random() > 0.2:
                    links_data.append({'name': 'LinkedIn', 'url': f'https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{i}'})
                if random.random() > 0.3:
                    links_data.append({'name': 'GitHub', 'url': f'https://github.com/{first_name.lower()}{last_name.lower()}{i}'})
                if random.random() > 0.6:
                    links_data.append({'name': 'Portfolio', 'url': f'https://{first_name.lower()}{last_name.lower()}{i}.com'})
                links_json = json.dumps(links_data) if links_data else ''
                
                # Create applicant
                applicant = Applicant.objects.create(
                    user=user_obj,
                    first_name=first_name,
                    last_name=last_name,
                    skills=skills_text,
                    education=random.choice(education_levels),
                    experience=experience_text,
                    links=links_json,
                    phone=f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
                    city=loc['city'],
                    state=loc['state'],
                    post_code=loc['post_code'],
                    country='USA',
                    location_lat=loc['lat'],
                    location_lon=loc['lon'],
                    availability=random.choice(['available', 'open-to-work', 'open-to-work', 'not-looking'])
                )
                
                # Create privacy settings (most visible)
                ApplicantPrivacySettings.objects.create(
                    applicant=applicant,
                    show_skills=True,
                    show_education=True,
                    show_experience=True,
                    show_projects=True,
                    show_links=True,
                    show_phone=random.choice([True, False]),
                    show_location=True,
                    show_availability=True
                )
                
                # Create projects
                num_projs = random.randint(2, 5)
                for p in range(num_projs):
                    project_tech = random.sample(candidate_skills, random.randint(2, 4))
                    Project.objects.create(
                        applicant=applicant,
                        title=f"{random.choice(['E-commerce', 'Social Media', 'Analytics', 'Dashboard', 'API', 'Mobile App'])} Platform",
                        description=f"A full-stack application built with {', '.join(project_tech)}. Features include user authentication, data visualization, and real-time updates.",
                        technologies=', '.join(project_tech),
                        url=f"https://github.com/{first_name.lower()}{last_name.lower()}{i}/project-{p+1}" if random.random() > 0.3 else None
                    )
                
                # Create applications to some of the job postings
                num_apps = random.randint(1, min(5, len(job_postings)))
                selected_jobs = random.sample(job_postings, num_apps)
                
                for job in selected_jobs:
                    Application.objects.get_or_create(
                        applicant=applicant,
                        listing=job,
                        defaults={
                            'status': random.choice(['Applied', 'Under Review', 'Interview', 'Offer', 'Closed']),
                            'message': f"Hi, I'm interested in the {job.title} position. I have experience with {', '.join(candidate_skills[:3])} and would love to discuss how I can contribute to your team."
                        }
                    )
                    applications_created += 1
                
                applicants_created += 1
                
                if (i + 1) % 20 == 0:
                    self.stdout.write(f'  Created {i + 1}/{num_candidates} candidates...')
            
            self.stdout.write(self.style.SUCCESS(f'✓ Created {applicants_created} candidates'))
            self.stdout.write(self.style.SUCCESS(f'✓ Created {applications_created} applications'))
            
        elif is_applicant:
            applicant = user.applicant
            self.stdout.write(self.style.WARNING(f'\n=== Creating {num_projects} Projects ==='))
            
            # Get applicant's skills
            applicant_skills = applicant.skills.split(', ') if applicant.skills else tech_skills[:5]
            
            # Create projects
            for i in range(num_projects):
                project_tech = random.sample(tech_skills, random.randint(3, 6))
                Project.objects.create(
                    applicant=applicant,
                    title=f"{random.choice(['E-commerce', 'Social Media', 'Analytics Dashboard', 'Task Management', 'API Gateway', 'Mobile App', 'Data Visualization', 'Chat Application'])} Platform",
                    description=f"A comprehensive full-stack application built with {', '.join(project_tech)}. Features include user authentication, real-time updates, responsive design, and scalable architecture. Implemented best practices for code quality and performance optimization.",
                    technologies=', '.join(project_tech),
                    url=f"https://github.com/{user.username}/project-{i+1}" if random.random() > 0.2 else None
                )
            
            self.stdout.write(self.style.SUCCESS(f'✓ Created {num_projects} projects'))
            
            # Create other recruiters and jobs
            self.stdout.write(self.style.WARNING(f'\n=== Creating Recruiters and Job Postings ==='))
            
            recruiters_created = 0
            jobs_created = 0
            
            for i in range(20):  # Create 20 recruiters
                loc = random.choice(locations)
                company = random.choice(company_names)
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                email = f"recruiter.{company.lower().replace(' ', '')}.{i}@demo.com"
                username = email
                
                user_obj, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                    }
                )
                
                if not created:
                    continue
                
                recruiter_obj, created = Recruiter.objects.get_or_create(
                    user=user_obj,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'company_name': company,
                        'city': loc['city'],
                        'state': loc['state'],
                        'post_code': loc['post_code'],
                        'country': 'USA',
                    }
                )
                
                if created:
                    recruiters_created += 1
                
                # Create job postings for this recruiter
                num_jobs_for_recruiter = random.randint(2, 8)
                for j in range(num_jobs_for_recruiter):
                    job_loc = random.choice(locations)
                    job_title = random.choice(job_titles)
                    
                    num_skills = random.randint(3, 8)
                    required_skills = random.sample(tech_skills, num_skills)
                    skills_text = ', '.join(required_skills)
                    
                    base_salary = random.randint(80000, 180000)
                    salary_min = Decimal(str(base_salary))
                    salary_max = Decimal(str(base_salary + random.randint(20000, 50000)))
                    
                    description = f"""
We are seeking a talented {job_title} to join our innovative team.

Key Responsibilities:
- Design and implement scalable software solutions
- Collaborate with product managers and designers
- Write clean, testable code
- Participate in agile development processes
- Mentor junior developers

Required Skills: {skills_text}

We offer competitive salary, comprehensive benefits, flexible work arrangements, and opportunities for professional growth.
                    """.strip()
                    
                    JobPosting.objects.create(
                        recruiter=recruiter_obj,
                        title=job_title,
                        description=description,
                        skills_required=skills_text,
                        street_address=f"{random.randint(100, 999)} Business Park Drive",
                        city=job_loc['city'],
                        state=job_loc['state'],
                        post_code=job_loc['post_code'],
                        country='USA',
                        location_lat=job_loc['lat'],
                        location_lon=job_loc['lon'],
                        salary_min=salary_min,
                        salary_max=salary_max,
                        remote=random.choice([True, False, False]),
                        visa_sponsorship=random.choice([True, False]),
                        visibility='public',
                        is_draft=False,
                        is_closed=random.choice([False, False, True])
                    )
                    jobs_created += 1
            
            self.stdout.write(self.style.SUCCESS(f'✓ Created {recruiters_created} recruiters'))
            self.stdout.write(self.style.SUCCESS(f'✓ Created {jobs_created} job postings'))
            
            # Create applications
            self.stdout.write(self.style.WARNING(f'\n=== Creating {num_applications} Applications ==='))
            
            all_jobs = list(JobPosting.objects.filter(is_draft=False, is_closed=False)[:100])
            
            if all_jobs:
                applications_created = 0
                for i in range(min(num_applications, len(all_jobs))):
                    job = random.choice(all_jobs)
                    Application.objects.get_or_create(
                        applicant=applicant,
                        listing=job,
                        defaults={
                            'status': random.choice(['Applied', 'Under Review', 'Interview', 'Offer']),
                            'message': f"Hi, I'm very interested in the {job.title} position. I have relevant experience and skills that align with your requirements. I would love the opportunity to discuss how I can contribute to your team."
                        }
                    )
                    applications_created += 1
                
                self.stdout.write(self.style.SUCCESS(f'✓ Created {applications_created} applications'))
            else:
                self.stdout.write(self.style.WARNING('No jobs available to apply to'))

        self.stdout.write(self.style.SUCCESS('\n=== Demo Data Flood Complete! ==='))
        self.stdout.write(self.style.SUCCESS('Your app is now flooded with demo data! 🎉'))


