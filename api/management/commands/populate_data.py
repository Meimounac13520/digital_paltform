from django.core.management.base import BaseCommand
from faker import Faker
import random
from api.models import (
    Role, Agency, User, Direction, Department, TaskPriority, TaskStatus, Task, 
    TaskAssignment, IncidentSeverity, IncidentStatus, IncidentCategory, Incident,
    ComplaintStatus, ComplaintCategory, ComplaintChannel, Complaint,
    ActionPlan, Objective, Milestone, InternalRequest, ApprovalStep,
    KPIIndicator, KPIValue, Notification, Comment, Attachment
)
from django.contrib.auth.hashers import make_password

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with fake data for testing'

    def handle(self, *args, **kwargs):
        # Create Roles
        roles = []
        for _ in range(3):
            role = Role.objects.create(name=fake.job(), description=fake.text())
            roles.append(role)

        # Create Agencies
        agencies = []
        for _ in range(3):
            agency = Agency.objects.create(
                code=fake.unique.lexify(text='AG???'),
                name=fake.company(),
                type=fake.word(),
                location=fake.city()
            )
            agencies.append(agency)

        # Create Users
        users = []
        for i in range(5):
            user = User.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                phone=fake.phone_number(),
                role=random.choice(roles),
                agency=random.choice(agencies),
                password=make_password('password123')  # password for all users
            )
            users.append(user)

        # Assign Directors to Agencies
        for agency in agencies:
            agency.director = random.choice(users)
            agency.save()

        # Create Directions and Departments
        directions = []
        for _ in range(3):
            direction = Direction.objects.create(
                code=fake.unique.lexify(text='DIR??'),
                name=fake.company(),
                responsible=random.choice(users)
            )
            directions.append(direction)
            for _ in range(2):
                Department.objects.create(
                    code=fake.unique.lexify(text='DEP??'),
                    name=fake.bs(),
                    direction=direction
                )

        # Create TaskPriorities, TaskStatuses
        priorities = [TaskPriority.objects.create(name=fake.word(), level=random.randint(1, 5)) for _ in range(3)]
        statuses = [TaskStatus.objects.create(code=fake.word(), label=fake.word()) for _ in range(3)]

        # Create Tasks
        tasks = []
        for _ in range(5):
            task = Task.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                due_date=fake.future_date(),
                priority=random.choice(priorities),
                status=random.choice(statuses),
                creator=random.choice(users),
                agency=random.choice(agencies)
            )
            tasks.append(task)

        # Task Assignments
        for task in tasks:
            TaskAssignment.objects.create(task=task, assignee=random.choice(users))

        # Incidents
        severities = [IncidentSeverity.objects.create(code=fake.word(), label=fake.word()) for _ in range(3)]
        incident_statuses = [IncidentStatus.objects.create(code=fake.word(), label=fake.word()) for _ in range(3)]
        incident_categories = [IncidentCategory.objects.create(code=fake.word(), label=fake.word()) for _ in range(3)]

        for _ in range(5):
            Incident.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                category=random.choice(incident_categories),
                severity=random.choice(severities),
                status=random.choice(incident_statuses),
                agency=random.choice(agencies),
                reporter=random.choice(users)
            )

        # Complaints
        complaint_statuses = [ComplaintStatus.objects.create(code=fake.word(), label=fake.word()) for _ in range(3)]
        complaint_categories = [ComplaintCategory.objects.create(code=fake.word(), label=fake.word()) for _ in range(3)]
        complaint_channels = [ComplaintChannel.objects.create(code=fake.word(), label=fake.word()) for _ in range(3)]

        for _ in range(5):
            Complaint.objects.create(
                reference=fake.unique.lexify(text='CMP?????'),
                client_name=fake.name(),
                description=fake.text(),
                channel=random.choice(complaint_channels),
                category=random.choice(complaint_categories),
                status=random.choice(complaint_statuses),
                agency=random.choice(agencies)
            )

        # ActionPlans, Objectives, Milestones
        for _ in range(3):
            action_plan = ActionPlan.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                status=fake.word(),
                start_date=fake.date_this_year(),
                end_date=fake.future_date(),
                agency=random.choice(agencies)
            )
            for _ in range(2):
                objective = Objective.objects.create(
                    label=fake.sentence(),
                    target_value=round(random.uniform(1000, 5000), 2),
                    unit="Units",
                    due_date=fake.future_date(),
                    status=fake.word(),
                    action_plan=action_plan
                )
                for _ in range(2):
                    Milestone.objects.create(
                        label=fake.sentence(),
                        due_date=fake.future_date(),
                        completed_on=None,
                        objective=objective
                    )

        # Internal Requests and Approvals
        for _ in range(5):
            request = InternalRequest.objects.create(
                subject=fake.sentence(),
                description=fake.text(),
                type=fake.word(),
                status=fake.word(),
                amount=round(random.uniform(1000, 10000), 2),
                requester=random.choice(users),
                agency=random.choice(agencies)
            )
            ApprovalStep.objects.create(
                request=request,
                approver_role=random.choice(roles),
                decision='Pending',
                comment=''
            )

        # KPI Indicators & Values
        indicators = []
        for _ in range(3):
            indicator = KPIIndicator.objects.create(
                code=fake.lexify(text='KPI??'),
                name=fake.word(),
                description=fake.text(),
                formula=fake.text()
            )
            indicators.append(indicator)

        for indicator in indicators:
            KPIValue.objects.create(
                indicator=indicator,
                period='2024-Q1',
                value=round(random.uniform(0, 100), 2)
            )

        # Notifications & Comments
        for _ in range(5):
            Notification.objects.create(
                title=fake.sentence(),
                message=fake.text(),
                recipient=random.choice(users)
            )

        self.stdout.write(self.style.SUCCESS('✅ Fake data successfully populated.'))
