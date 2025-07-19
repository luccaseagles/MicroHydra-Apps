class Roku:
    def __init__(self, ip, debug=False):
        self.base_url = f"http://{ip}:8060"
        self.debug = debug
        try:
            import urequests as requests  # MicroPython
        except ImportError:
            import requests  # Standard Python
        self.requests = requests

    def keypress(self, key):
        url = f"{self.base_url}/keypress/{key}"
        try:
            resp = self.requests.post(url)
            if hasattr(resp, "close"): resp.close()
            if self.debug:
                print(f"[DEBUG] Sent keypress: {key} to {url}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send keypress {key}: {e}")
            return False

if __name__ == "__main__":
    # Replace with your Roku's IP
    roku = Roku("192.168.68.49", debug=True)

    test_keys = ["Lit_%20"]

    for key in test_keys:
        roku.keypress(key)
