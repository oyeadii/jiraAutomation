from helper.connection import DbConnection
from helper import jira_auto,send_mail
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from os import environ
from datetime import datetime,timedelta


def jira_automation():
    on_date=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d") 
    emp_list=jira_auto.JiraAutomation(email=environ.get("JIRA_USER"),user_pwd=environ.get("JIRA_PWD"), on_date=on_date).jira_timesheet()
    if emp_list!="Failed":
        dbClass=DbConnection()
        all_emps = dbClass.get(condition_1="emp_name,emp_email",table_name="sb_emp_master")
        df_emps=pd.DataFrame(all_emps)
        print(df_emps)


        to_send_list=[]
        mail_subject="Test Mail"
        mail_body="test MAIl body"
        send_mail.SendMail(email=environ.get("GMAIL_USER"), password=environ.get("GMAIL_PWD")).send_mail(mail_subject=mail_subject,mail_body=mail_body, to_send_list=to_send_list)
        print("SUCCESS")
        return "SUCCESS"
    print("FAILED")
    return "FAILED"