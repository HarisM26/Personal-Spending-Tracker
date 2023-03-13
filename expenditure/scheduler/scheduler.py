from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
import expenditure.models
from expenditure.helpers import get_end_date, create_notification_about_refresh
from datetime import timedelta

logger = logging.getLogger(__name__)


def refresh_time_limit():
    print('================== Attempt to refresh =========================')
    # get limits with end date as a day before current day
    expired_limits = expenditure.models.Limit.objects.filter(
        end_date=datetime.date(datetime.now())-timedelta(days=1))

    for limit in expired_limits:
        category = expenditure.models.SpendingCategory.objects.get(limit=limit)
        transactions = expenditure.models.SpendingTransaction.objects.filter(
            spending_category=category)

        for transaction in transactions:
            transaction.is_current = False
            transaction.save()

        limit.remaining_amount = limit.limit_amount
        limit.status = 'not reached'
        limit.start_date = datetime.date(datetime.now())
        limit.end_date = get_end_date(limit.time_limit_type)
        limit.save()

        create_notification_about_refresh(category.user, category)


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

# class Command(BaseCommand):
    # help = 'Run APScheduler'

""" def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    scheduler.add_job(
        refresh_time_limit,
        trigger=CronTrigger(hour='*/2'),  # hour='00', minute='00'),
        id='refresh_time_limit',
        max_instances=1,
        replace_existing=True,
    )
    register_events(scheduler)
    logger.info('Added job "my_job".')

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added weekly job: 'delete_old_job_executions'.")

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
 """
