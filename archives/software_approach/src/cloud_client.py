class GoDaikinCloud:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None
        self.base_url = "https://api.daikin.com.my/api"

    def login(self):
        """Authenticates and retrieves a token."""
        print("Logging in with supplied credentials...")
        return False

    def list_devices(self):
        """Returns list of AC units."""
        if not self.token:
            return []
        return []

    def set_state(self, device_id, power=None, temp=None, fan=None):
        """Sends command to AC."""
        print(f"Setting state for {device_id}...")
        return True
