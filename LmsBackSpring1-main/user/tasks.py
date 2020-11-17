from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone

# @periodic_task(run_every=crontab(second='*/10'))
# @celery.decorators.periodic_task(run_every=datetime.timedelta(minutes=1))
def delete_otp():
    # Query all the foos in our database
    print("Hello1")
    foos = Otp.objects.all()
    print("Hello")

    # Iterate through them
    for foo in foos:

        # If the expiration date is bigger than now delete it
        if foo.expiration_date < timezone.now():
            foo.delete()
            # log deletion
    return "completed deleting foos at {}".format(timezone.now())