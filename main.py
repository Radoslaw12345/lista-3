import subprocess
import json

def send_request(url):
    result = subprocess.run(['curl', '-s', '-w', '%{http_code}', url], capture_output=True, text=True)
    body, status = result.stdout[:-3], int(result.stdout[-3:])
    return body, status

def test_api():
    tests = [
        {"name": "GET /posts/1", "url": "https://jsonplaceholder.typicode.com/posts/1", "expected_status": 200, "expected_keys": ["userId", "id", "title", "body"]},
        {"name": "GET /users/1", "url": "https://jsonplaceholder.typicode.com/users/1", "expected_status": 200, "expected_keys": ["id", "name", "username", "email"]},
        {"name": "GET /comments/1", "url": "https://jsonplaceholder.typicode.com/comments/1", "expected_status": 200, "expected_keys": ["postId", "id", "name", "email", "body"]}
    ]

    for test in tests:
        body, status = send_request(test["url"])
        if status != test["expected_status"]:
            print(f'{test["name"]}: FAILED (Expected status {test["expected_status"]}, got {status})')
            continue

        try:
            json_data = json.loads(body)
        except json.JSONDecodeError:
            print(f'{test["name"]}: FAILED (Invalid JSON response)')
            continue

        if all(key in json_data for key in test["expected_keys"]):
            print(f'{test["name"]}: PASSED')
        else:
            print(f'{test["name"]}: FAILED (Missing keys)')

if __name__ == "__main__":
    test_api()