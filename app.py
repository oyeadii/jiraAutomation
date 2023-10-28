from flask import Flask
from flask_apscheduler import APScheduler
from scheduler.jira_auto_script import jira_automation

class Config:
    SCHEDULER_API_ENABLED = True

# creating the flask app
scheduler = APScheduler()
app = Flask(__name__)
app.config.from_object(Config())
scheduler.init_app(app)
scheduler.start()

app.apscheduler.add_job(func=jira_automation, trigger='interval', id='jira_timelog_email', seconds=60, misfire_grace_time=None, coalesce=False,max_instances=3)


# driver function
if __name__ == '__main__':
    app.run(debug = True)
