from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8000"  # use "host" instead of "base_url"

    @task
    def get_campaign(self):
        self.client.get("/campaigns/12/")  # This will be appended to the host
