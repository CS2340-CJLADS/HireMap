from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
from messages.models import Message
from accounts.models import Applicant, Recruiter

class Command(BaseCommand):
    help = 'Generate fake chat messages between users for frontend development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--conversations',
            type=int,
            default=5,
            help='Number of conversations to create (default: 5)',
        )
        parser.add_argument(
            '--messages-per-conversation',
            type=int,
            default=10,
            help='Number of messages per conversation (default: 10)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing messages before generating new ones',
        )

    def handle(self, *args, **options):
        conversations_count = options['conversations']
        messages_per_conversation = options['messages_per_conversation']
        clear_existing = options['clear']

        if clear_existing:
            Message.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all existing messages'))

        # Get all applicants and recruiters
        applicants = Applicant.objects.all()
        recruiters = Recruiter.objects.all()

        if not applicants.exists():
            self.stdout.write(
                self.style.ERROR('No applicants found. Please create some applicants first.')
            )
            return

        if not recruiters.exists():
            self.stdout.write(
                self.style.ERROR('No recruiters found. Please create some recruiters first.')
            )
            return

        # Sample conversation starters
        recruiter_starters = [
            "Hi! I came across your profile and I'm impressed with your experience.",
            "Hello! We have an exciting opportunity that might be a great fit for you.",
            "Hi there! Your skills align perfectly with a role we're hiring for.",
            "Hello! I'd love to discuss a potential opportunity with you.",
            "Hi! Your background in {skill} caught my attention. Are you open to new opportunities?",
            "Hello! We're looking for someone with your exact skill set.",
            "Hi there! I think you'd be a great fit for our team.",
            "Hello! I'd like to schedule a quick call to discuss a role.",
        ]

        applicant_responses = [
            "Hi! Thanks for reaching out. I'd love to learn more.",
            "Hello! That sounds interesting. Can you tell me more about the role?",
            "Hi there! I'm definitely open to hearing about opportunities.",
            "Hello! I'd be happy to discuss. What's the position?",
            "Hi! That's great to hear. What does the role entail?",
            "Hello! I'm interested. Can you share more details?",
            "Hi there! When would be a good time to chat?",
            "Hello! I'd like to know more about the company and position.",
        ]

        follow_up_messages = [
            "The role is for a {role} position. It's a {type} role with great benefits.",
            "We're a {company_type} company looking to expand our team.",
            "The position offers competitive salary and remote work options.",
            "We're looking for someone who can start within the next month.",
            "The team is really collaborative and supportive.",
            "We offer great growth opportunities and professional development.",
            "The role involves working on exciting projects with cutting-edge technology.",
            "We have a flexible work schedule and excellent work-life balance.",
            "The position is based in {location}, but we're open to remote candidates.",
            "We'd love to have you come in for an interview.",
            "When would be a good time for you to discuss this further?",
            "I can send you the full job description if you're interested.",
            "The salary range is competitive for the market.",
            "We're looking to fill this position as soon as possible.",
            "I think you'd be a perfect fit for our team culture.",
        ]

        applicant_follow_ups = [
            "That sounds great! I'd love to see the job description.",
            "I'm definitely interested. What's the next step?",
            "The role sounds interesting. Can we schedule a call?",
            "I'd like to learn more about the team and company culture.",
            "What's the salary range for this position?",
            "I'm available for an interview. When works best for you?",
            "This sounds like a great opportunity. I'm very interested.",
            "Can you tell me more about the day-to-day responsibilities?",
            "I'd love to discuss this further. When can we chat?",
            "The remote work option is appealing. What's the timezone requirement?",
        ]

        # Generate conversations
        created_count = 0
        applicant_list = list(applicants)
        recruiter_list = list(recruiters)

        for i in range(conversations_count):
            # Pick random applicant and recruiter
            applicant = random.choice(applicant_list)
            recruiter = random.choice(recruiter_list)
            
            applicant_user = applicant.user
            recruiter_user = recruiter.user

            # Start conversation from a random time in the past (within last 30 days)
            base_time = timezone.now() - timedelta(days=random.randint(1, 30))
            
            # First message from recruiter
            starter = random.choice(recruiter_starters)
            # Replace placeholders if any
            starter = starter.replace('{skill}', random.choice(['Python', 'JavaScript', 'React', 'Django', 'Full Stack Development']))
            
            first_message = Message.objects.create(
                sender=recruiter_user,
                recipient=applicant_user,
                content=starter,
                timestamp=base_time
            )
            created_count += 1

            # Generate back-and-forth messages
            current_time = base_time
            is_recruiter_turn = False  # Next message is from applicant

            for j in range(messages_per_conversation - 1):
                # Add some time between messages (few minutes to few hours)
                current_time += timedelta(
                    minutes=random.randint(5, 180)
                )

                if is_recruiter_turn:
                    # Recruiter message
                    if j < 3:
                        # Early in conversation, use follow-up messages
                        message_text = random.choice(follow_up_messages)
                        message_text = message_text.replace('{role}', random.choice(['Software Engineer', 'Developer', 'Full Stack Developer', 'Backend Developer']))
                        message_text = message_text.replace('{type}', random.choice(['full-time', 'contract', 'part-time']))
                        message_text = message_text.replace('{company_type}', random.choice(['tech', 'startup', 'established', 'growing']))
                        message_text = message_text.replace('{location}', random.choice(['San Francisco', 'New York', 'Remote', 'Austin']))
                    else:
                        # Later in conversation, use more varied messages
                        message_text = random.choice([
                            "Great! I'll send you the details via email.",
                            "Perfect! Let me know what times work for you.",
                            "Sounds good! I'll set up a call for next week.",
                            "Excellent! I'll forward your profile to the hiring manager.",
                            "I'll send you a calendar invite for the interview.",
                            "Looking forward to speaking with you!",
                            "I'll be in touch soon with more details.",
                        ])
                    sender = recruiter_user
                    recipient = applicant_user
                else:
                    # Applicant message
                    if j < 3:
                        message_text = random.choice(applicant_responses)
                    else:
                        message_text = random.choice(applicant_follow_ups)
                    sender = applicant_user
                    recipient = recruiter_user

                message = Message.objects.create(
                    sender=sender,
                    recipient=recipient,
                    content=message_text,
                    timestamp=current_time
                )
                created_count += 1
                is_recruiter_turn = not is_recruiter_turn

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} messages across {conversations_count} conversations!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'You can now view these messages at /messages/'
            )
        )

