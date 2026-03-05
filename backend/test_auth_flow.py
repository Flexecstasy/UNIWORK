import requests

BASE = "http://127.0.0.1:8000"


def main() -> None:
    print("Testing login and /me...")
    r = requests.post(
        f"{BASE}/api/auth/login",
        json={"email": "employer@uniwork.kz", "password": "employer123"},
    )
    print("LOGIN:", r.status_code, r.text)
    r.raise_for_status()

    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r2 = requests.get(f"{BASE}/api/auth/me", headers=headers)
    print("ME:", r2.status_code, r2.text)


if __name__ == "__main__":
    main()

