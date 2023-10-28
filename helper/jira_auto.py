import gc
from playwright.sync_api import sync_playwright


class JiraAutomation():
    def __init__(self, email, user_pwd, on_date, **kwargs):
        self.PLAY=sync_playwright().start()
        self.BROWSER=self.PLAY.chromium.launch(headless=False)
        self.page=self.BROWSER.new_page()
        self.email=email
        self.user_pwd=user_pwd
        self.on_date=on_date
        self.login_url="https://id.atlassian.com/login"

    def browser_close(self):
        self.BROWSER.close()

    def do_login(self):
        self.page.goto(self.login_url)
        self.page.wait_for_timeout(3000)    
        self.page.wait_for_load_state()
        self.page.wait_for_selector("#username")
        email = self.page.locator("#username")
        email.click()
        email.fill(self.email)
        self.page.keyboard.press("Enter")
        password=self.page.locator("#password")
        password.click()
        password.fill(self.user_pwd)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(5000)
        return "Success"
    
    def jira_timesheet(self):
        if self.do_login()!="Success":
            self.browser_close()
            return "Failed"
        
        self.page.goto("add your jira work url endpoint")
        self.page.wait_for_timeout(5000)
        self.page.wait_for_load_state()
        self.page.get_by_text("Apps").click()
        self.page.wait_for_timeout(2000)
        self.page.get_by_text("Timesheet").click()
        self.page.wait_for_timeout(30000)

        iframe_context = self.page.frames[1]
        jql_button=iframe_context.get_by_text('JQL',exact=True)
        jql_button.scroll_into_view_if_needed()
        jql_button.click()

        iframe_context.wait_for_timeout(1000)
        query=iframe_context.locator('[data-testid=jql-editor-input]')
        # date format = 2023-03-02 (year-month-date)
        query.fill(f"""worklogDate >= {self.on_date} AND worklogDate <= {self.on_date} order by created DESC""")
        self.page.wait_for_timeout(2000)
        generate_button=iframe_context.get_by_text("Generate", exact=True)
        generate_button.click()
        iframe_context.wait_for_timeout(10000)
        clocked_users=iframe_context.locator('//*[@id="grid-wrapper"]/div/div/div[2]/div[2]/div[1]/div[2]/div/div/div')
        users=[]
        for i in range(clocked_users.count()):
            users.append(clocked_users.nth(i).text_content().strip())

        self.browser_close()
        gc.collect()
        return users
