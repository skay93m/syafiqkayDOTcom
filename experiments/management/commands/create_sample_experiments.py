from django.core.management.base import BaseCommand
from django.utils.text import slugify
from experiments.models import Experiment, ExperimentResource


class Command(BaseCommand):
    help = 'Create sample experiments for testing the admin interface'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of sample experiments to create (default: 5)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        sample_experiments = [
            {
                'title': 'Machine Learning Model Performance Analysis',
                'description': 'Analyzing the performance of different ML models on customer data',
                'hypothesis': 'Random Forest will outperform Linear Regression for customer churn prediction',
                'methodology': 'Compare accuracy, precision, and recall of different models using cross-validation',
                'status': 'testing',
                'tags': 'machine learning, data science, customer analytics',
                'is_published': True,
                'resources': [
                    {'title': 'Scikit-learn Documentation', 'url': 'https://scikit-learn.org/stable/'},
                    {'title': 'Customer Dataset', 'url': 'https://example.com/dataset'},
                ]
            },
            {
                'title': 'Web Performance Optimization Study',
                'description': 'Testing various techniques to improve website loading speed',
                'hypothesis': 'Implementing lazy loading will reduce initial page load time by 30%',
                'methodology': 'A/B test with performance metrics monitoring using Lighthouse',
                'status': 'analyzing',
                'tags': 'web performance, optimization, user experience',
                'is_published': True,
                'resources': [
                    {'title': 'Google Lighthouse', 'url': 'https://developers.google.com/web/tools/lighthouse'},
                ]
            },
            {
                'title': 'User Interface Color Psychology Research',
                'description': 'Investigating how color choices affect user behavior and conversion rates',
                'hypothesis': 'Warm colors (red, orange) increase click-through rates compared to cool colors',
                'methodology': 'Controlled experiment with color variations on call-to-action buttons',
                'status': 'completed',
                'tags': 'ui/ux, psychology, conversion optimization',
                'is_published': True,
                'results': 'Warm colors showed 15% higher CTR than cool colors',
                'conclusions': 'Color psychology significantly impacts user engagement',
                'resources': [
                    {'title': 'Color Theory Guide', 'url': 'https://example.com/color-theory'},
                ]
            },
            {
                'title': 'Database Query Optimization Analysis',
                'description': 'Comparing different indexing strategies for large database tables',
                'hypothesis': 'Composite indexes will improve query performance by 40% over single-column indexes',
                'methodology': 'Benchmark queries with different indexing approaches using PostgreSQL',
                'status': 'designing',
                'tags': 'database, performance, optimization, postgresql',
                'is_published': True,
                'resources': [
                    {'title': 'PostgreSQL Documentation', 'url': 'https://www.postgresql.org/docs/'},
                    {'title': 'Query Optimization Guide', 'url': 'https://example.com/query-optimization'},
                ]
            },
            {
                'title': 'Mobile App Push Notification Effectiveness',
                'description': 'Testing optimal timing and content for push notifications',
                'hypothesis': 'Personalized notifications sent at 7 PM increase app engagement by 25%',
                'methodology': 'Randomized controlled trial with different notification strategies',
                'status': 'conceptualizing',
                'tags': 'mobile, notifications, engagement, personalization',
                'is_published': True,
                'resources': [
                    {'title': 'Push Notification Best Practices', 'url': 'https://example.com/push-notifications'},
                ]
            },
            {
                'title': 'API Rate Limiting Impact Study',
                'description': 'Analyzing how different rate limiting strategies affect API performance',
                'hypothesis': 'Sliding window rate limiting provides better user experience than fixed window',
                'methodology': 'Load testing with different rate limiting algorithms',
                'status': 'abandoned',
                'tags': 'api, rate limiting, performance, scalability',
                'is_published': True,
                'resources': [
                    {'title': 'Rate Limiting Algorithms', 'url': 'https://example.com/rate-limiting'},
                ]
            },
        ]

        created_count = 0
        for i in range(min(count, len(sample_experiments))):
            experiment_data = sample_experiments[i]
            resources_data = experiment_data.pop('resources', [])
            
            # Create slug from title
            experiment_data['slug'] = slugify(experiment_data['title'])
            
            # Create experiment
            experiment, created = Experiment.objects.get_or_create(
                slug=experiment_data['slug'],
                defaults=experiment_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created experiment: {experiment.title}')
                )
                
                # Create resources
                for resource_data in resources_data:
                    resource = ExperimentResource.objects.create(
                        experiment=experiment,
                        **resource_data
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'  - Added resource: {resource.title}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Experiment already exists: {experiment.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new experiments')
        )
