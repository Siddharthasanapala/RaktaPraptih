from locust import HttpUser, task, between
import json

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Called when a user starts"""
        # Login if authentication is required
        self.login()
    
    def login(self):
        """Login user"""
        response = self.client.post("/login/", json={
            "email": "pavan@gmail.com",
            "password": "1234"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.client.headers.update({"Authorization": f"Token {self.token}"})
    
    @task(3)
    def view_homepage(self):
        """View homepage - higher weight (3)"""
        self.client.get("/")
    
    @task(2)
    def bloodbanks_view(self):
        """View API endpoint - medium weight (2)"""
        self.client.get("/bloodbanks/")
    
    @task(1)
    def donors_view(self):
        """View resource detail"""
        self.client.get("/donors/")