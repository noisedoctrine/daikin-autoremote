import getpass
import json
import os
import urllib.error
import urllib.request


def login_aws(email, password):
    base_url = os.getenv(
        "DAIKIN_AUTH_BASE_URL",
        "https://bq53w7rpb6.execute-api.ap-southeast-1.amazonaws.com/prod",
    )
    api_key = os.getenv("DAIKIN_API_KEY")
    if not api_key:
        raise RuntimeError("DAIKIN_API_KEY is not set")

    paths = ["/v1/member/login", "/member/login", "/login"]
    for path in paths:
        url = f"{base_url}{path}"
        print(f"Trying {url}...")
        data = {"email": email, "password": password, "app_id": "my.com.daikin.app"}

        request = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"))
        request.add_header("Content-Type", "application/json")
        request.add_header("User-Agent", "Go Daikin/1.4.0 (Android)")
        request.add_header("x-api-key", api_key)

        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                response_data = json.loads(response.read().decode("utf-8"))
                token = response_data.get("data", {}).get("access_token") or response_data.get("access_token")
                if token:
                    return token
        except urllib.error.HTTPError:
            continue
    return None


if __name__ == "__main__":
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    token = login_aws(email, password)
    if token:
        print("\n[SUCCESS] Token retrieved!")
