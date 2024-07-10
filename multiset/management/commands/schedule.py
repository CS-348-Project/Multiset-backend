# modified from code provided at https://pypi.org/project/django-apscheduler/
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from notifications.smtp.send import send_email_notifications


@util.close_old_connections
def send_email_notifications_job():
    # Your job processing logic here...
    print("Sending email notifications...")
    send_email_notifications()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_email_notifications_job,
            # to test this, you can change the trigger to IntervalTrigger(minutes=1) for once a minute
            # or you can just wait a whole day if you have the patience
            trigger=IntervalTrigger(days=1),  # Every day
            id="send_email_notifications_job",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=IntervalTrigger(weeks=1),  # every week
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        try:
            print("Starting scheduler...")
            scheduler.start()
            print("Scheduler started!")
        except KeyboardInterrupt:
            print("Stopping scheduler...")
            scheduler.shutdown()
            print("Scheduler stopped!")
