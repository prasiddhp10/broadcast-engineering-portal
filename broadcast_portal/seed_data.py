import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'broadcast_engineering.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from organization.models import Department
from teams.models import Team, TeamMember, TeamDependency, CodeRepo, ContactChannel
from messaging.models import Message
from schedule.models import MeetingSchedule, MeetingParticipant


def make_username(full_name):
    parts = full_name.lower().split()
    return parts[0][0] + parts[1]


def run():
    print("Seeding database...")

    # ─────────────────────────────────────────
    # USERS
    # ─────────────────────────────────────────

    all_people = [
        ('Sebastian', 'Holt'),
        ('Nora',      'Chandler'),
        ('Mason',     'Briggs'),
        ('Violet',    'Ramsey'),
        ('Adam',      'Sinclair'),
        ('Lucy',      'Vaughn'),
        ('Theodore',  'Knox'),
        ('Bella',     'Monroe'),
        ('Olivia',    'Carter'),
        ('James',     'Bennett'),
        ('Emma',      'Richardson'),
        ('Benjamin',  'Hayes'),
        ('Sophia',    'Mitchell'),
        ('William',   'Cooper'),
        ('Isabella',  'Ross'),
        ('Elijah',    'Parker'),
        ('Ava',       'Sullivan'),
        ('Noah',      'Campbell'),
        ('Mia',       'Henderson'),
        ('Lucas',     'Foster'),
        ('Charlotte', 'Murphy'),
        ('Henry',     'Ward'),
        ('Amelia',    'Brooks'),
        ('Alexander', 'Perry'),
        ('Evelyn',    'Hughes'),
        ('Daniel',    'Scott'),
        ('Harper',    'Lewis'),
        ('Matthew',   'Reed'),
        ('Scarlett',  'Edwards'),
        ('Jack',      'Turner'),
        ('Lily',      'Phillips'),
        ('Samuel',    'Morgan'),
        ('Grace',     'Patterson'),
        ('Owen',      'Barnes'),
        ('Chloe',     'Hall'),
        ('Nathan',    'Fisher'),
        ('Zoey',      'Stevens'),
        ('Caleb',     'Bryant'),
        ('Hannah',    'Simmons'),
        ('Isaac',     'Jenkins'),
        ('Madison',   'Clarke'),
        ('Gabriel',   'Coleman'),
        ('Riley',     'Sanders'),
        ('Leo',       'Watson'),
        ('Victoria',  'Price'),
        ('Julian',    'Bell'),
        ('Layla',     'Russell'),
        ('Ethan',     'Griffin'),
        ('Aurora',    'Cooper'),
        ('Dylan',     'Spencer'),
        ('Stella',    'Martinez'),
        ('Levi',      'Bishop'),
        ('Eleanor',   'Freeman'),
        ('Hudson',    'Ford'),
    ]

    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@broadcastportal.com',
            password='Admin1234!',
            first_name='Admin',
            last_name='User'
        )
        print("Created superuser: admin / Admin1234!")
    else:
        admin = User.objects.get(username='admin')

    user_map = {}
    for first, last in all_people:
        username = make_username(f"{first} {last}")
        if not User.objects.filter(username=username).exists():
            u = User.objects.create_user(
                username=username,
                email=f"{username}@broadcastportal.com",
                password='Portal123!',
                first_name=first,
                last_name=last,
            )
        else:
            u = User.objects.get(username=username)
        user_map[f"{first} {last}"] = u

    print(f"Users ready: {User.objects.count()} total")

    # ─────────────────────────────────────────
    # DEPARTMENTS
    # ─────────────────────────────────────────

    dept_xtvweb, _      = Department.objects.get_or_create(
        department_name='xTV_Web',
        defaults={'department_head': user_map['Sebastian Holt']}
    )
    dept_nativeTVs, _   = Department.objects.get_or_create(
        department_name='Native TVs',
        defaults={'department_head': user_map['Mason Briggs']}
    )
    dept_mobile, _      = Department.objects.get_or_create(
        department_name='Mobile',
        defaults={'department_head': user_map['Violet Ramsey']}
    )
    dept_reliability, _ = Department.objects.get_or_create(
        department_name='Reliability_Tool',
        defaults={'department_head': user_map['Lucy Vaughn']}
    )
    dept_arch, _        = Department.objects.get_or_create(
        department_name='Arch',
        defaults={'department_head': user_map['Theodore Knox']}
    )
    dept_programme, _   = Department.objects.get_or_create(
        department_name='Programme',
        defaults={'department_head': user_map['Bella Monroe']}
    )

    print("Departments created")

    # ─────────────────────────────────────────
    # TEAMS — exact data from Excel sheet
    # (name, dept, leader, team_type, jira,
    #  focus, skills, agile, status)
    # ─────────────────────────────────────────

    teams_data = [
        # ── xTV_Web (head: Sebastian Holt) ──────────────────────────────
        ('Code Warriors',        dept_xtvweb,      'Olivia Carter',
         'Frontend',          'Client Lightning Xtv',
         'Infrastructure scalability, CI/CD integration, platform resilience',
         'AWS/GCP, Terraform, Kubernetes, CI/CD, Docker, Python, Bash',
         '', 'ACTIVE'),
        ('The Debuggers',        dept_xtvweb,      'James Bennett',
         'Backend',           'Client Lightning Xtv',
         'Advanced debugging tools, automated error detection, root cause analysis',
         'Debugging tools (GDB, LLDB), Stack traces, Log analysis, Python, Java',
         '', 'ACTIVE'),
        ('Bit Masters',          dept_xtvweb,      'Emma Richardson',
         'Security',          'Client Lightning Xtv',
         'Security compliance, encryption techniques, data integrity',
         'Cryptography, Penetration Testing, Security Compliance (ISO 27001)',
         '', 'ACTIVE'),
        ('Agile Avengers',       dept_xtvweb,      'Benjamin Hayes',
         'Agile Coaching',    'Client Lightning Xtv',
         'Agile transformation, workflow optimization, lean process improvement',
         'Agile frameworks (Scrum, SAFe, Kanban), Jira, Miro, Confluence',
         '', 'ACTIVE'),
        ('Syntax Squad',         dept_xtvweb,      'Sophia Mitchell',
         'DevOps',            'Client Lightning Xtv',
         'Automated deployment pipelines, release management, rollback strategies',
         'CI/CD, GitHub Actions, Jenkins, YAML, Kubernetes, Helm Charts',
         '', 'ACTIVE'),
        ('The Codebreakers',     dept_xtvweb,      'William Cooper',
         'Security',          'Client Lightning Xtv',
         'Cryptographic security, authentication protocols, secure APIs',
         'Cybersecurity, Ethical Hacking, Encryption (AES, RSA), SSL/TLS',
         '', 'ACTIVE'),
        ('DevOps Dynasty',       dept_xtvweb,      'Isabella Ross',
         'DevOps',            '',
         'DevOps best practices, Kubernetes orchestration, cloud automation',
         'Kubernetes, Terraform, Ansible, CI/CD, AWS/GCP, Docker, Linux',
         '', 'ACTIVE'),
        ('Byte Force',           dept_xtvweb,      'Elijah Parker',
         'Cloud',             'Client Lightning Xtv',
         'Cloud infrastructure, API gateway development, serverless architecture',
         'AWS Lambda, API Gateway, Microservices, GraphQL, Node.js, Go',
         '', 'ACTIVE'),
        ('The Cloud Architects', dept_xtvweb,      'Ava Sullivan',
         'Cloud',             'Client Lightning Xtv',
         'Cloud-native applications, distributed systems, multi-region deployments',
         'Kubernetes, Istio, Terraform, AWS/GCP/Azure, Load Balancing',
         '', 'ACTIVE'),
        ('Full Stack Ninjas',    dept_xtvweb,      'Noah Campbell',
         'Full Stack',        'Client Lightning Xtv',
         'Frontend and backend synchronization, API integration, UX/UI consistency',
         'React, Node.js, TypeScript, GraphQL, Next.js, Django, REST APIs',
         '', 'ACTIVE'),
        # ── xTV_Web (head: Nora Chandler) ───────────────────────────────
        ('The Error Handlers',   dept_xtvweb,      'Mia Henderson',
         'Monitoring',        'Client Web',
         'Log aggregation, AI-driven anomaly detection, real-time monitoring',
         'Logging (ELK, Splunk), APM (Datadog, New Relic), Exception Handling',
         '', 'ACTIVE'),
        ('Stack Overflow Survivors', dept_xtvweb,  'Lucas Foster',
         'Knowledge',         'Client Web',
         'Knowledge management, engineering playbooks, documentation automation',
         'Technical Documentation, Knowledge Sharing, Confluence, AI Bots',
         '', 'ACTIVE'),
        ('The Binary Beasts',    dept_xtvweb,      'Charlotte Murphy',
         'Performance',       'Client Web',
         'High-performance computing, low-latency data processing, algorithm efficiency',
         'C/C++, Data Structures, Parallel Computing, GPU Programming',
         '', 'ACTIVE'),
        ('API Avengers',         dept_xtvweb,      'Henry Ward',
         'API',               'Client Web',
         'API security, authentication layers, API scalability',
         'API Security (OAuth, JWT), Postman, OpenAPI/Swagger, REST, gRPC',
         '', 'ACTIVE'),
        ('The Algorithm Alliance', dept_xtvweb,    'Amelia Brooks',
         'Data Science',      'Client Web',
         'Machine learning models, AI-driven analytics, data science applications',
         'Machine Learning, Data Science (Pandas, NumPy, Scikit-learn)',
         '', 'ACTIVE'),
        # ── Native TVs ───────────────────────────────────────────────────
        ('Data Wranglers',       dept_nativeTVs,   'Alexander Perry',
         'Data Engineering',  'Client Roku TV',
         'Big data engineering, real-time data streaming, database optimization',
         'SQL, NoSQL, Big Data (Hadoop, Spark, Kafka), Python, ETL',
         '', 'ACTIVE'),
        ('The Sprint Kings',     dept_nativeTVs,   'Evelyn Hughes',
         'Agile',             'Client Roku TV',
         'Agile backlog management, sprint retrospectives, delivery forecasting',
         'Agile methodologies, Jira, Velocity Metrics, Sprint Planning',
         '', 'ACTIVE'),
        ('Exception Catchers',   dept_nativeTVs,   'Daniel Scott',
         'Reliability',       'Client Roku TV',
         'Fault tolerance, system resilience, disaster recovery planning',
         'Fault Tolerance, Failover Strategies, Incident Response, SRE',
         '', 'ACTIVE'),
        ('Code Monkeys',         dept_nativeTVs,   'Harper Lewis',
         'DevOps',            'Client Roku TV',
         'Patch deployment, rollback automation, version control best practices',
         'Git, Hotfix Management, Patch Deployment, Bash, CI/CD',
         '', 'ACTIVE'),
        ('The Compile Crew',     dept_nativeTVs,   'Matthew Reed',
         'Build Engineering', 'Client Roku TV',
         'Compiler optimization, static code analysis, build system improvements',
         'Build Systems (Bazel, CMake, Make), Compiler Optimization',
         '', 'ACTIVE'),
        ('Git Good',             dept_nativeTVs,   'Scarlett Edwards',
         'Version Control',   'Client Apple TV',
         'Branching strategies, merge conflict resolution, Git best practices',
         'Git, GitOps, Merge Strategies, Branching Models, GitLab CI/CD',
         '', 'ACTIVE'),
        ('The CI/CD Squad',      dept_nativeTVs,   'Jack Turner',
         'CI/CD',             'Client Apple TV',
         'Continuous integration, automated testing, deployment pipelines',
         'Jenkins, GitHub Actions, GitOps, Terraform, AWS CodePipeline',
         '', 'ACTIVE'),
        ('Bug Exterminators',    dept_nativeTVs,   'Lily Phillips',
         'QA',                'Client Apple TV',
         'Performance profiling, automated test generation, security patching',
         'Test Automation (Selenium, Cypress), Load Testing (JMeter)',
         'Scrum', 'ACTIVE'),
        ('The Agile Alchemists', dept_nativeTVs,   'Samuel Morgan',
         'Agile',             'Client Apple TV',
         'Agile maturity assessments, coaching and mentorship, SAFe/LeSS frameworks',
         'Agile Transformation, SAFe, Jira, Value Stream Mapping',
         '', 'ACTIVE'),
        ('The Hotfix Heroes',    dept_nativeTVs,   'Grace Patterson',
         'Reliability',       'Client Apple TV',
         'Emergency response, rollback strategies, live system debugging',
         'Real-time Debugging, Rollback Automation, Patch Deployment',
         '', 'ACTIVE'),
        # ── Mobile (head: Violet Ramsey) ─────────────────────────────────
        ('Cache Me Outside',     dept_mobile,      'Owen Barnes',
         'Performance',       'Client Mobile',
         'Caching strategies, distributed cache systems, database query optimization',
         'Redis, Memcached, CDN Caching, Cache Invalidation Strategies',
         '', 'ACTIVE'),
        ('The Scrum Lords',      dept_mobile,      'Chloe Hall',
         'Agile',             'Client Mobile',
         'Agile training, sprint planning automation, process governance',
         'Scrum Mastery, Agile Coaching, Jira, Retrospective Analysis',
         '', 'ACTIVE'),
        ('The 404 Not Found',    dept_mobile,      'Nathan Fisher',
         'Reliability',       'Client Mobile',
         'Error page personalization, debugging-as-a-service, incident response',
         'Incident Response, HTTP Error Handling, Observability',
         '', 'ACTIVE'),
        ('The Version Controllers', dept_mobile,   'Zoey Stevens',
         'Version Control',   'Client Mobile',
         'GitOps workflows, repository security, automated versioning',
         'Git, Repository Management, DevSecOps, GitOps',
         '', 'ACTIVE'),
        ('DevNull Pioneers',     dept_mobile,      'Caleb Bryant',
         'Observability',     'Client Mobile',
         'Logging frameworks, observability enhancements, error handling APIs',
         'Logging Systems, Observability (Grafana, Prometheus)',
         '', 'ACTIVE'),
        ('The Code Refactors',   dept_mobile,      'Hannah Simmons',
         'Commerce',          'Client Mobile',
         'Code maintainability, tech debt reduction, automated refactoring tools',
         'Code Cleanup, Tech Debt Management, SonarQube, Refactoring',
         'Scrum', 'ACTIVE'),
        ('The Jenkins Juggernauts', dept_mobile,   'Isaac Jenkins',
         'CI/CD',             'Client Mobile',
         'CI/CD pipeline optimization, Jenkins plugin development, infrastructure as code',
         'CI/CD Pipelines, Jenkins Scripting, Kubernetes, YAML',
         '', 'ACTIVE'),
        ('Infinite Loopers',     dept_mobile,      'Madison Clarke',
         'Frontend',          'Client Mobile',
         'Frontend performance optimization, UI/UX consistency, component reusability',
         'Frontend Optimization, Performance Metrics, JavaScript, CSS',
         '', 'ACTIVE'),
        ('The Feature Crafters', dept_mobile,      'Gabriel Coleman',
         'Product',           'Client Mobile',
         'Feature flagging, A/B testing automation, rapid prototyping',
         'A/B Testing, Feature Flagging, Frontend Frameworks',
         '', 'ACTIVE'),
        ('The Bit Manipulators', dept_mobile,      'Riley Sanders',
         'Data Engineering',  'Client Mobile',
         'Binary data processing, encoding/decoding algorithms, compression techniques',
         'Bitwise Operations, Low-level Optimization, Assembly, C++',
         '', 'ACTIVE'),
        ('Kernel Crushers',      dept_mobile,      'Leo Watson',
         'Systems',           'Client Mobile',
         'Low-level optimization, OS kernel tuning, hardware acceleration',
         'Linux Kernel Development, System Performance, Rust, C',
         '', 'ACTIVE'),
        # ── Mobile (head: Adam Sinclair) ─────────────────────────────────
        ('The Git Masters',      dept_mobile,      'Victoria Price',
         'Version Control',   'Client Mobile',
         'Git automation, monorepo strategies, repository analytics',
         'GitOps, Repository Scaling, Git Automation',
         '', 'ACTIVE'),
        ('The API Explorers',    dept_mobile,      'Julian Bell',
         'API',               '',
         'API documentation, API analytics, developer experience optimization',
         'API Testing (Postman, Swagger), API Gateway Management',
         '', 'ACTIVE'),
        # ── Reliability_Tool ─────────────────────────────────────────────
        ('The Lambda Legends',   dept_reliability, 'Layla Russell',
         'Serverless',        'Client Automation QA',
         'Serverless architecture, event-driven development, microservice automation',
         'Serverless Computing, AWS Lambda, Node.js, Python',
         '', 'ACTIVE'),
        ('The Encryption Squad', dept_reliability, 'Ethan Griffin',
         'Security',          '',
         'Cybersecurity research, cryptographic key management, secure data storage',
         'Cryptography (AES, RSA, SHA-256), Security Audits',
         '', 'ACTIVE'),
        ('The UX Wizards',       dept_reliability, 'Aurora Cooper',
         'Design',            'Client Device as a Service',
         'Accessibility, user behavior analytics, UI/UX best practices',
         'UI/UX Design, Figma, Adobe XD, Usability Testing',
         '', 'ACTIVE'),
        ('The Hackathon Hustlers', dept_reliability, 'Dylan Spencer',
         'Innovation',        'Client SRE',
         'Rapid prototyping, proof-of-concept development, hackathon facilitation',
         'Rapid Prototyping, MVP Development, No-Code Tools',
         '', 'ACTIVE'),
        ('The Frontend Phantoms', dept_reliability, 'Stella Martinez',
         'Frontend',          'Client Apps Tooling',
         'Frontend frameworks, web performance tuning, component libraries',
         'Frontend Frameworks (React, Vue, Angular), Performance Optimization',
         '', 'ACTIVE'),
        # ── Arch ─────────────────────────────────────────────────────────
        ('The Dev Dragons',      dept_arch,        'Levi Bishop',
         'Architecture',      '',
         'API integrations, SDK development, plugin architecture',
         'API Development, SDK Development, Plugin Architecture',
         '', 'ACTIVE'),
        ('The Microservice Mavericks', dept_arch,  'Eleanor Freeman',
         'Architecture',      'Client CLIP Backend for Frontend',
         'Microservice governance, inter-service communication, API gateways',
         'Service Mesh (Istio, Envoy), API Gateway, gRPC',
         '', 'ACTIVE'),
        # ── Programme ────────────────────────────────────────────────────
        ('The Quantum Coders',   dept_programme,   'Hudson Ford',
         'Research',          'Client Support',
         'Quantum computing simulations, parallel processing, AI-assisted coding',
         'Quantum Computing, Qiskit, Parallel Computing',
         '', 'ACTIVE'),
    ]

    team_map = {}
    for (name, dept, leader_name, ttype, jira,
         focus, skills, agile, status) in teams_data:
        team, _ = Team.objects.get_or_create(
            name=name,
            defaults={
                'department': dept,
                'team_leader': user_map[leader_name],
                'team_type': ttype,
                'jira_project_name': jira,
                'development_focus': focus,
                'key_skills': skills,
                'agile_practices': agile,
                'status': status,
            }
        )
        team_map[name] = team

    print(f"Teams created: {Team.objects.count()} total")

    # ─────────────────────────────────────────
    # TEAM MEMBERS — leader as member
    # ─────────────────────────────────────────

    for (name, dept, leader_name, *rest) in teams_data:
        TeamMember.objects.get_or_create(
            team=team_map[name],
            user=user_map[leader_name],
            defaults={'role_in_team': 'Team Lead'}
        )

    print("Team members created")

    # ─────────────────────────────────────────
    # TEAM DEPENDENCIES — exact from Excel
    # Downstream Dependencies column = who
    # this team depends on, and exact type
    # ─────────────────────────────────────────

    deps_data = [
        # xTV_Web
        ('Code Warriors',              'The Debuggers',            'Infrastructure Support'),
        ('The Debuggers',              'Bit Masters',              'Bug Resolution'),
        ('Bit Masters',                'API Avengers',             'Security Fixes'),
        ('Agile Avengers',             'The Sprint Kings',         'Agile Coaching'),
        ('Syntax Squad',               'The Feature Crafters',     'Deployment Pipeline'),
        ('The Codebreakers',           'The Encryption Squad',     'Encryption Logic'),
        ('DevOps Dynasty',             'Code Warriors',            'CI/CD Infrastructure'),
        ('Byte Force',                 'API Avengers',             'Cloud Hosting Services'),
        ('The Cloud Architects',       'Byte Force',               'Service Orchestration'),
        ('The Cloud Architects',       'Cache Me Outside',         'Service Orchestration'),
        ('Full Stack Ninjas',          'The API Explorers',        'Frontend Design'),
        ('The Error Handlers',         'The Debuggers',            'Error Logging Services'),
        ('Stack Overflow Survivors',   'The Scrum Lords',          'Best Practices Sharing'),
        ('The Binary Beasts',          'The Algorithm Alliance',   'Data Processing'),
        ('API Avengers',               'The Dev Dragons',          'Secure API Development'),
        ('The Algorithm Alliance',     'The Codebreakers',         'Advanced Algorithm Support'),
        # Native TVs
        ('Data Wranglers',             'The Bit Manipulators',     'User Data Insights'),
        ('The Sprint Kings',           'The Agile Alchemists',     'Sprint Planning'),
        ('Exception Catchers',         'The Debuggers',            'Critical Fixes'),
        ('Code Monkeys',               'The Version Controllers',  'Patch Management'),
        ('The Compile Crew',           'The Bit Manipulators',     'Code Base Management'),
        ('Git Good',                   'The Version Controllers',  'Automated Merging'),
        ('The CI/CD Squad',            'Syntax Squad',             'Deployment Rollback Support'),
        ('Bug Exterminators',          'The Debuggers',            'Performance Tuning'),
        ('The Agile Alchemists',       'Stack Overflow Survivors', 'Agile Adoption Coaching'),
        ('The Hotfix Heroes',          'The CI/CD Squad',          'Emergency Fixes'),
        ('The Hotfix Heroes',          'Code Monkeys',             'Emergency Fixes'),
        # Mobile
        ('Cache Me Outside',           'The UX Wizards',           'Distributed Caching Services'),
        ('The Scrum Lords',            'The Sprint Kings',         'Agile Process Coordination'),
        ('The Scrum Lords',            'Agile Avengers',           'Agile Process Coordination'),
        ('The 404 Not Found',          'The Scrum Lords',          'Repository Management'),
        ('The Version Controllers',    'The Compile Crew',         'Branching Strategy'),
        ('The Version Controllers',    'The 404 Not Found',        'Branching Strategy'),
        ('DevNull Pioneers',           'The API Explorers',        'API Documentation'),
        ('The Code Refactors',         'Bug Exterminators',        'Legacy Code Cleanup'),
        ('The Jenkins Juggernauts',    'DevOps Dynasty',           'Automated Testing'),
        ('The Jenkins Juggernauts',    'Git Good',                 'Automated Testing'),
        ('Infinite Loopers',           'The Feature Crafters',     'UI Responsiveness'),
        ('The Feature Crafters',       'The Error Handlers',       'Design Feedback'),
        ('The Feature Crafters',       'Syntax Squad',             'Design Feedback'),
        ('The Bit Manipulators',       'The Binary Beasts',        'ETL Pipelines'),
        ('Kernel Crushers',            'API Avengers',             'Low-Level Optimization'),
        ('The Git Masters',            'The Version Controllers',  'Best Practices'),
        ('The API Explorers',          'Full Stack Ninjas',        'Secure Communication'),
        # Reliability_Tool
        ('The Lambda Legends',         'API Avengers',             'Serverless Functions'),
        ('The Encryption Squad',       'API Avengers',             'Cryptographic Security'),
        ('The Encryption Squad',       'The API Explorers',        'Cryptographic Security'),
        ('The UX Wizards',             'Full Stack Ninjas',        'UI Components'),
        ('The UX Wizards',             'The Feature Crafters',     'UI Components'),
        ('The Hackathon Hustlers',     'The UX Wizards',           'Rapid Prototyping'),
        ('The Frontend Phantoms',      'The API Explorers',        'UI Enhancements'),
        # Arch
        ('The Dev Dragons',            'The Feature Crafters',     'API Integration'),
        ('The Microservice Mavericks', 'The Code Refactors',       'Service Scaling'),
        ('The Microservice Mavericks', 'The Lambda Legends',       'Service Scaling'),
        # Programme
        ('The Quantum Coders',         'Kernel Crushers',          'High-Performance Computing'),
    ]

    for team_name, depends_on_name, dep_type in deps_data:
        if team_name in team_map and depends_on_name in team_map:
            TeamDependency.objects.get_or_create(
                team=team_map[team_name],
                depends_on_team=team_map[depends_on_name],
                defaults={'dependency_type': dep_type}
            )

    print(f"Dependencies created: {TeamDependency.objects.count()} total")

    # ─────────────────────────────────────────
    # CODE REPOS — exact URLs from Excel
    # ─────────────────────────────────────────

    repos_data = [
        ('Code Warriors',             'Code Warriors Repo',           'https://tiny.cc/x9b4t'),
        ('The Debuggers',             'The Debuggers Repo',           'https://bit.ly/3FgTzX'),
        ('Bit Masters',               'Bit Masters Repo',             'https://t.ly/8YpQm'),
        ('Agile Avengers',            'Agile Avengers Repo',          'https://goo.gl/R2X7Pd'),
        ('Syntax Squad',              'Syntax Squad Repo',            'https://tinyurl.com/y7n3lxp2'),
        ('The Codebreakers',          'The Codebreakers Repo',        'https://bit.do/rJ4mT'),
        ('DevOps Dynasty',            'DevOps Dynasty Repo',          'https://is.gd/Kp4XQ9'),
        ('Byte Force',                'Byte Force Repo',              'https://short.io/L2rYQ5'),
        ('The Cloud Architects',      'The Cloud Architects Repo',    'https://tiny.cc/mQ7nX8'),
        ('Full Stack Ninjas',         'Full Stack Ninjas Repo',       'https://bit.ly/4Yx9TmR'),
        ('The Error Handlers',        'The Error Handlers Repo',      'https://t.ly/xM7p9Q'),
        ('Stack Overflow Survivors',  'Stack Overflow Survivors Repo','https://goo.gl/YX34Pn'),
        ('The Binary Beasts',         'The Binary Beasts Repo',       'https://tinyurl.com/98tXmLp'),
        ('API Avengers',              'API Avengers Repo',            'https://bit.do/ZpL4TQ'),
        ('The Algorithm Alliance',    'The Algorithm Alliance Repo',  'https://is.gd/QxN7T9'),
        ('Data Wranglers',            'Data Wranglers Repo',          'https://short.io/7LpX4YQ'),
        ('The Sprint Kings',          'The Sprint Kings Repo',        'https://tiny.cc/QpM74X'),
        ('Exception Catchers',        'Exception Catchers Repo',      'https://bit.ly/X7pL4TQ'),
        ('Code Monkeys',              'Code Monkeys Repo',            'https://t.ly/M98X7TQ'),
        ('The Compile Crew',          'The Compile Crew Repo',        'https://goo.gl/LpX7TQ9'),
        ('Git Good',                  'Git Good Repo',                'https://tinyurl.com/YXpM749'),
        ('The CI/CD Squad',           'The CI/CD Squad Repo',         'https://bit.do/QX74MT9'),
        ('Bug Exterminators',         'Bug Exterminators Repo',       'https://is.gd/MX74TQ9'),
        ('The Agile Alchemists',      'The Agile Alchemists Repo',    'https://short.io/T9Q7MX4'),
        ('The Hotfix Heroes',         'The Hotfix Heroes Repo',       'https://tiny.cc/X7T9Q4M'),
        ('Cache Me Outside',          'Cache Me Outside Repo',        'https://bit.ly/74QMXT9'),
        ('The Scrum Lords',           'The Scrum Lords Repo',         'https://t.ly/QX7M94T'),
        ('The 404 Not Found',         'The 404 Not Found Repo',       'https://goo.gl/T9XQ74M'),
        ('The Version Controllers',   'The Version Controllers Repo', 'https://tinyurl.com/X74MT9Q'),
        ('DevNull Pioneers',          'DevNull Pioneers Repo',        'https://bit.do/TQX794M'),
        ('The Code Refactors',        'The Code Refactors Repo',      'https://is.gd/MTX974Q'),
        ('The Jenkins Juggernauts',   'The Jenkins Juggernauts Repo', 'https://short.io/9X74TQM'),
        ('Infinite Loopers',          'Infinite Loopers Repo',        'https://tiny.cc/QMTX749'),
        ('The Feature Crafters',      'The Feature Crafters Repo',    'https://bit.ly/X7Q9T4M'),
        ('The Bit Manipulators',      'The Bit Manipulators Repo',    'https://t.ly/MTQX794'),
        ('Kernel Crushers',           'Kernel Crushers Repo',         'https://goo.gl/7QXMT49'),
        ('The Git Masters',           'The Git Masters Repo',         'https://tinyurl.com/MTX749Q'),
        ('The API Explorers',         'The API Explorers Repo',       'https://bit.do/X7TQ49M'),
        ('The Lambda Legends',        'The Lambda Legends Repo',      'https://is.gd/MTQ974X'),
        ('The Encryption Squad',      'The Encryption Squad Repo',    'https://short.io/T9X47QM'),
        ('The UX Wizards',            'The UX Wizards Repo',          'https://tiny.cc/Q7MTX94'),
        ('The Hackathon Hustlers',    'The Hackathon Hustlers Repo',  'https://bit.ly/MT7XQ49'),
        ('The Frontend Phantoms',     'The Frontend Phantoms Repo',   'https://t.ly/9T7QX4M'),
        ('The Dev Dragons',           'The Dev Dragons Repo',         'https://goo.gl/QXMT974'),
        ('The Microservice Mavericks','The Microservice Mavericks Repo','https://tinyurl.com/7T9QMX4'),
        ('The Quantum Coders',        'The Quantum Coders Repo',      'https://bit.do/X9T7Q4M'),
    ]

    for team_name, repo_name, repo_url in repos_data:
        if team_name in team_map:
            CodeRepo.objects.get_or_create(
                team=team_map[team_name],
                repo_name=repo_name,
                defaults={'repo_url': repo_url}
            )

    print(f"Code repos created: {CodeRepo.objects.count()} total")

    # ─────────────────────────────────────────
    # CONTACT CHANNELS — exact from Excel
    # ─────────────────────────────────────────

    channels_data = [
        # Jira board links from Excel
        ('Code Warriors',            'JIRA',    'Code Warriors Board',          'https://short.ly/a7XbP3'),
        ('The Debuggers',            'JIRA',    'The Debuggers Board',          'https://tiny.link/ZpQ4M9'),
        ('Bit Masters',              'JIRA',    'Bit Masters Board',            'https://bitly.io/7XQM94T'),
        ('Agile Avengers',           'JIRA',    'Agile Avengers Board',         'https://shrt.me/M7QXT49'),
        ('Syntax Squad',             'JIRA',    'Syntax Squad Board',           'https://fakeurl.net/X94TQM7'),
        ('The Codebreakers',         'JIRA',    'The Codebreakers Board',       'https://notreal.ly/MTQX947'),
        ('DevOps Dynasty',           'JIRA',    'DevOps Dynasty Board',         'https://quick.li/9X7TQ4M'),
        ('Byte Force',               'JIRA',    'Byte Force Board',             'https://go2.cc/MT7XQ49'),
        ('The Cloud Architects',     'JIRA',    'The Cloud Architects Board',   'https://linktr.ee/7TQX94M'),
        ('Full Stack Ninjas',        'JIRA',    'Full Stack Ninjas Board',      'https://jumpto.me/QX97MT4'),
        ('The Error Handlers',       'JIRA',    'The Error Handlers Board',     'https://tinygo.co/T9X7Q4M'),
        ('Stack Overflow Survivors', 'JIRA',    'Stack Overflow Survivors Board','https://click4.cc/X7TQM94'),
        ('The Binary Beasts',        'JIRA',    'The Binary Beasts Board',      'https://shortr.io/M9X7QT4'),
        ('API Avengers',             'JIRA',    'API Avengers Board',           'https://fake.li/QXMT749'),
        ('The Algorithm Alliance',   'JIRA',    'The Algorithm Alliance Board', 'https://notreal.cc/7QX9MT4'),
        ('Data Wranglers',           'JIRA',    'Data Wranglers Board',         'https://trythis.me/TQX79M4'),
        ('The Sprint Kings',         'JIRA',    'The Sprint Kings Board',       'https://shrtn.co/M7XQT49'),
        ('Exception Catchers',       'JIRA',    'Exception Catchers Board',     'https://smallurl.io/Q7MTX49'),
        ('Code Monkeys',             'JIRA',    'Code Monkeys Board',           'https://void.li/MT9X74Q'),
        ('The Compile Crew',         'JIRA',    'The Compile Crew Board',       'https://jumpnow.co/XQT79M4'),
        ('Git Good',                 'JIRA',    'Git Good Board',               'https://fakeclick.me/7T9XQ4M'),
        ('The CI/CD Squad',          'JIRA',    'The CI/CD Squad Board',        'https://shortjump.io/TX7Q94M'),
        ('Bug Exterminators',        'JIRA',    'Bug Exterminators Board',      'https://redirect.cc/QX79T4M'),
        ('The Agile Alchemists',     'JIRA',    'The Agile Alchemists Board',   'https://zaplink.io/M7XQT94'),
        ('The Hotfix Heroes',        'JIRA',    'The Hotfix Heroes Board',      'https://noway.to/TQ79MX4'),
        ('Cache Me Outside',         'JIRA',    'Cache Me Outside Board',       'https://linkdrop.cc/MTX97Q4'),
        ('The Scrum Lords',          'JIRA',    'The Scrum Lords Board',        'https://shrinkto.me/QX7MT49'),
        ('The 404 Not Found',        'JIRA',    'The 404 Not Found Board',      'https://quicktap.io/X79TQ4M'),
        ('The Version Controllers',  'JIRA',    'The Version Controllers Board','https://tapgo.co/MX74TQ9'),
        ('DevNull Pioneers',         'JIRA',    'DevNull Pioneers Board',       'https://notareallink.com/Q7X9T4M'),
        ('The Code Refactors',       'JIRA',    'The Code Refactors Board',     'https://urlfake.io/MT9X7Q4'),
        ('The Jenkins Juggernauts',  'JIRA',    'The Jenkins Juggernauts Board','https://snapurl.cc/7XMT9Q4'),
        ('Infinite Loopers',         'JIRA',    'Infinite Loopers Board',       'https://random.ly/XQ79MT4'),
        ('The Feature Crafters',     'JIRA',    'The Feature Crafters Board',   'https://clickthis.to/MTQ79X4'),
        ('The Bit Manipulators',     'JIRA',    'The Bit Manipulators Board',   'https://noreal.co/QX97MT4'),
        ('Kernel Crushers',          'JIRA',    'Kernel Crushers Board',        'https://fastgo.io/TQ97X4M'),
        ('The Git Masters',          'JIRA',    'The Git Masters Board',        'https://shrinkme.co/MXQ79T4'),
        ('The API Explorers',        'JIRA',    'The API Explorers Board',      'https://url-shorten.cc/7T9XQ4M'),
        ('The Lambda Legends',       'JIRA',    'The Lambda Legends Board',     'https://tinyway.me/Q7XMT94'),
        ('The Encryption Squad',     'JIRA',    'The Encryption Squad Board',   'https://jumpfast.io/TQX79M4'),
        ('The UX Wizards',           'JIRA',    'The UX Wizards Board',         'https://micro.link/X7MT9Q4'),
        ('The Hackathon Hustlers',   'JIRA',    'The Hackathon Hustlers Board', 'https://quickmove.cc/MTX97Q4'),
        ('The Frontend Phantoms',    'JIRA',    'The Frontend Phantoms Board',  'https://fakejump.io/QX7T9M4'),
        ('The Dev Dragons',          'JIRA',    'The Dev Dragons Board',        'https://shorty.cc/T79XQ4M'),
        ('The Microservice Mavericks','JIRA',   'Microservice Mavericks Board', 'https://zapit.io/7XMTQ94'),
        ('The Quantum Coders',       'JIRA',    'The Quantum Coders Board',     'https://bitnotreal.com/QXMT749'),
        # Slack channels from Excel (where specified)
        ('Agile Avengers',           'SLACK',   'Agile Avengers Slack',         'peacock-bravo, gst-xtv-commerce, gst-xtv-bravo-frontdoor'),
        ('The Code Refactors',       'SLACK',   'The Code Refactors Slack',     '#gst-mobile-commerce-poker-face'),
        # Standup times from Excel (where specified)
        ('Bug Exterminators',        'STANDUP', 'Bug Exterminators Standup',    '0.40625'),
    ]

    for team_name, ch_type, ch_name, value in channels_data:
        if team_name in team_map:
            ContactChannel.objects.get_or_create(
                team=team_map[team_name],
                channel_name=ch_name,
                defaults={
                    'channel_type': ch_type,
                    'value': value,
                }
            )

    print(f"Contact channels created: {ContactChannel.objects.count()} total")

    # ─────────────────────────────────────────
    # MESSAGES
    # ─────────────────────────────────────────

    msgs_data = [
        ('Olivia Carter',   'James Bennett',   'Sprint Review Notes',
         'Hi James, here are the notes from this weeks sprint review. Please review and share with your team.',
         'SENT'),
        ('James Bennett',   'Olivia Carter',   'Re: Sprint Review Notes',
         'Thanks Olivia, I have shared these with the team. We will action the feedback in the next sprint.',
         'SENT'),
        ('Emma Richardson', 'Henry Ward',      'Security Audit Request',
         'Henry, we need to run a joint security audit on the API endpoints. Can we schedule this for next week?',
         'SENT'),
        ('Henry Ward',      'Emma Richardson', 'Re: Security Audit Request',
         'Sure Emma, I am available Tuesday and Thursday afternoon. Let me know which works for you.',
         'SENT'),
        ('Benjamin Hayes',  'Evelyn Hughes',   'Agile Coaching Session',
         'Evelyn, I would like to arrange an agile coaching session for the Sprint Kings team. Are you available?',
         'SENT'),
        ('Evelyn Hughes',   'Benjamin Hayes',  'Re: Agile Coaching Session',
         'Absolutely Benjamin. How about next Wednesday at 2pm? I can run a full retrospective workshop.',
         'SENT'),
        ('Sophia Mitchell', 'Jack Turner',     'Deployment Pipeline Issue',
         'Jack, we are seeing failures in the deployment pipeline for the Apple TV client. Can you investigate?',
         'SENT'),
        ('Jack Turner',     'Sophia Mitchell', 'Re: Deployment Pipeline Issue',
         'Hi Sophia, I have identified the root cause. It was a misconfigured YAML step. Fixed and redeployed.',
         'SENT'),
        ('Alexander Perry', 'Riley Sanders',   'Data Pipeline Collaboration',
         'Riley, we need your team to help with the ETL pipeline optimisation for the Roku TV data stream.',
         'SENT'),
        ('Grace Patterson', 'Daniel Scott',    'Emergency Hotfix Coordination',
         'Daniel, we have a live incident on the Apple TV client. Can your team support with fault tolerance?',
         'SENT'),
        ('Layla Russell',   'Henry Ward',      'Serverless API Integration',
         'Henry, the Lambda Legends need access to the API Avengers secure endpoints. Can you provision access?',
         'SENT'),
        ('Aurora Cooper',   'Noah Campbell',   'UI Component Review',
         'Noah, we have completed the new UI component library. Can the Full Stack Ninjas review and provide feedback?',
         'SENT'),
        ('Olivia Carter',   'Sebastian Holt',  'Draft: Q2 Team Report',
         'Sebastian, here is a draft of the Q2 team performance report. Will finalise once you review.',
         'DRAFT'),
        ('Mason Briggs',    'Evelyn Hughes',   'Draft: Native TVs Roadmap',
         'Evelyn, I have started drafting the Native TVs roadmap for Q3. Please review when ready.',
         'DRAFT'),
    ]

    for sender_name, recipient_name, subject, body, status in msgs_data:
        if sender_name in user_map and recipient_name in user_map:
            Message.objects.get_or_create(
                sender=user_map[sender_name],
                recipient=user_map[recipient_name],
                subject=subject,
                defaults={'body': body, 'status': status}
            )

    print(f"Messages created: {Message.objects.count()} total")

    # ─────────────────────────────────────────
    # MEETINGS
    # ─────────────────────────────────────────

    now = timezone.now()

    meetings_data = [
        (
            'xTV_Web Sprint Planning',
            'Code Warriors', 'Olivia Carter', 'Zoom',
            'https://zoom.us/j/111111111',
            now + datetime.timedelta(days=1, hours=2),
            'Weekly sprint planning for xTV_Web teams.',
            ['James Bennett', 'Emma Richardson', 'Benjamin Hayes'],
        ),
        (
            'Security and API Review',
            'API Avengers', 'Henry Ward', 'Teams',
            'https://teams.microsoft.com/meeting/sec-api',
            now + datetime.timedelta(days=2, hours=3),
            'Joint security and API review session.',
            ['Emma Richardson', 'William Cooper', 'Ethan Griffin'],
        ),
        (
            'Native TVs Agile Retrospective',
            'The Sprint Kings', 'Evelyn Hughes', 'Meet',
            'https://meet.google.com/native-retro',
            now + datetime.timedelta(days=3, hours=1),
            'Monthly agile retrospective for Native TVs teams.',
            ['Samuel Morgan', 'Daniel Scott', 'Grace Patterson'],
        ),
        (
            'CI/CD Pipeline Review',
            'The CI/CD Squad', 'Jack Turner', 'Zoom',
            'https://zoom.us/j/cicd-review',
            now + datetime.timedelta(days=4, hours=4),
            'Review of deployment pipeline issues and improvements.',
            ['Sophia Mitchell', 'Isaac Jenkins', 'Isabella Ross'],
        ),
        (
            'Mobile Performance Sync',
            'Cache Me Outside', 'Owen Barnes', 'Zoom',
            'https://zoom.us/j/mobile-perf',
            now + datetime.timedelta(days=5, hours=2),
            'Monthly sync on caching performance and mobile optimisation.',
            ['Madison Clarke', 'Gabriel Coleman', 'Leo Watson'],
        ),
        (
            'Data Engineering Monthly Review',
            'Data Wranglers', 'Alexander Perry', 'Meet',
            'https://meet.google.com/data-monthly',
            now + datetime.timedelta(days=7, hours=3),
            'Monthly review of data pipelines and ETL performance.',
            ['Riley Sanders', 'Matthew Reed', 'Mason Briggs'],
        ),
        (
            'UX and Frontend Collaboration',
            'The UX Wizards', 'Aurora Cooper', 'Teams',
            'https://teams.microsoft.com/meeting/ux-frontend',
            now + datetime.timedelta(days=8, hours=2),
            'Collaboration session between UX and Frontend teams.',
            ['Noah Campbell', 'Gabriel Coleman', 'Stella Martinez'],
        ),
        (
            'Architecture Review Board',
            'The Microservice Mavericks', 'Eleanor Freeman', 'Zoom',
            'https://zoom.us/j/arch-review',
            now + datetime.timedelta(days=10, hours=5),
            'Quarterly architecture review for all platform services.',
            ['Levi Bishop', 'Theodore Knox', 'Layla Russell'],
        ),
        (
            'Emergency Hotfix Stand-up',
            'The Hotfix Heroes', 'Grace Patterson', 'Slack',
            '',
            now + datetime.timedelta(days=11, hours=1),
            'Emergency stand-up to coordinate live incident response.',
            ['Daniel Scott', 'Jack Turner', 'Harper Lewis'],
        ),
        (
            'All Departments All Hands',
            'Code Warriors', 'Olivia Carter', 'Zoom',
            'https://zoom.us/j/allhands-q2',
            now + datetime.timedelta(days=14, hours=6),
            'Q2 all-hands meeting across all departments.',
            [
                'Sebastian Holt', 'Mason Briggs', 'Violet Ramsey',
                'Lucy Vaughn', 'Theodore Knox', 'Bella Monroe',
                'James Bennett', 'Henry Ward', 'Alexander Perry',
            ],
        ),
    ]

    for (title, team_name, organizer_name, platform,
         link, sched_time, desc, participants) in meetings_data:
        if team_name in team_map and organizer_name in user_map:
            meeting, _ = MeetingSchedule.objects.get_or_create(
                title=title,
                defaults={
                    'team': team_map[team_name],
                    'organizer': user_map[organizer_name],
                    'platform': platform,
                    'meeting_link': link,
                    'schedule_time': sched_time,
                    'description': desc,
                }
            )
            MeetingParticipant.objects.get_or_create(
                meeting=meeting, user=user_map[organizer_name]
            )
            for p_name in participants:
                if p_name in user_map:
                    MeetingParticipant.objects.get_or_create(
                        meeting=meeting, user=user_map[p_name]
                    )

    print(f"Meetings created: {MeetingSchedule.objects.count()} total")

    # ─────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────

    print("")
    print("=" * 55)
    print("  Database seeded successfully!")
    print("=" * 55)
    print(f"  Departments  : {Department.objects.count()}")
    print(f"  Teams        : {Team.objects.count()}")
    print(f"  Users        : {User.objects.count()}")
    print(f"  Dependencies : {TeamDependency.objects.count()}")
    print(f"  Code Repos   : {CodeRepo.objects.count()}")
    print(f"  Channels     : {ContactChannel.objects.count()}")
    print(f"  Messages     : {Message.objects.count()}")
    print(f"  Meetings     : {MeetingSchedule.objects.count()}")
    print("=" * 55)
    print("")
    print("  Admin login:")
    print("    Username : admin")
    print("    Password : Admin1234!")
    print("")
    print("  All other users password : Portal123!")
    print("  Username = first initial + last name")
    print("  Examples:")
    print("    Olivia Carter    -> ocarter")
    print("    James Bennett    -> jbennett")
    print("    Alexander Perry  -> aperry")
    print("    Sebastian Holt   -> sholt")
    print("    Mason Briggs     -> mbriggs")
    print("=" * 55)


if __name__ == '__main__':
    run()
