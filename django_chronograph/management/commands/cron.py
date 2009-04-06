from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Runs all jobs that are due.'
    
    def handle(self, *args, **options):
        from django_chronograph.models import Job
        for job in Job.objects.due():
            job.run()