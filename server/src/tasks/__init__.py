from celery.signals import task_postrun, task_prerun
from etasks import emails
from etasks import engage
from etasks import mailchimp_sync
from profile import tasks as ptasks
from main import database as d

@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from 
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors 
    # won't propagate across tasks)
    if d.session:
        d.session.remove()

@task_prerun.connect
def on_task_init(*args, **kwargs):
    d.engine.dispose()
