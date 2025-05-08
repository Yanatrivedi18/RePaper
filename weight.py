import firebase_admin
from firebase_admin import credentials, firestore
import time

securityjson = {
  "type": "service_account",
  "project_id": "repaper-18551",
  "private_key_id": "73283a8f20e81b82ff0042d163c5c6bd5d2a8a5c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC4GNM6Eoi+1m8S\nSWluwwgB1SHCv8hwcCvfxF8JxBSptNRperZhBizMyxaZK+xyCmN1OkT3W2GkqKL9\nJSevfYX4148jmeQkOvkE0TkN99a/dLMlI8zvO5by4VB4J8yqrOdBvN6at3cXQ+20\n7TbV6qnd1G+3UP7JlX2nUrchJ3H+kGsrBvySUNXuSXjwk68b1no/VgGldj/ze3zD\n+YvH3vm7rTZZzleFuHJtvDhZzFkFkJTff3P2B0lC135LBfU+DmbOMwvC3RatIwlW\n8WYyyhg+ydfWG27756zh6RJd0V+mUwO/8eexbzPIxUHt/nQ2F0AWvPK8GZ62MRtt\nd6BtXXMPAgMBAAECggEAJjxFtqR90UEBLaegpbgNFDBbhDLH4w5xFlcXNBSNBBhC\nG6w4b9tT967ggSydvavJr2HMTCGnHIdH3tLWNL0Z066VlJvURfAXozf/JRcJ+5a1\n1Gtkl3Vlawl/6Iy/ld02ZLFg/HpJWkQp/S9deb10zVVfZJAGcwDA6b0kutaR9wBV\n3I4U9+fMiUnbuL38yBCjAe7NLT3Eg+FkjA2ln9ZAU34r/IH9LXxuC30nUymtafBr\nL9wOcW6rWQBEjL15BA7/THFAtMF+GOSaUkCY2nQmu8qxj7IHJfSX0Lk9eMWxcuud\n1v7f0jikyN3nc/czjZkYuhcjEGEdWSxEflN0woHiyQKBgQD1lMCI1jYwHe50MYlv\nexP4RzdhD6VbyTuzcp6cwVF+FlYhtvzY6ePplZdVFwvXp9BQ3Qh3q6OqPlf9u9nk\n6xvsB4ZHIxoKBYcRmKhQWlShFGvxEXvAimun57Rm4GcqRfWBU0egJ4bR+4RSN+h6\nNy4Nqqu8GwskSUcdowkMru3G6QKBgQC/6Evb3QpmJf+AHOx8KzHilSq6WdIZe1vZ\nRu6ga1+PpKdaGT2zZI11vyeIoVhKdIVUYF3fI5PWscBxp3FkrPXSFQuX49UWtaU3\nkdg4AjYxb/JtkuUMAIyti043Y+PLr1GGLKsN02Fhe1owYj0RXjTTYjlYkTLINVg/\neYDw77WfNwKBgC30sDLrIyjN8Rl9S6K4/XuwmARp0R/kAHAMOvJKmt1lgKi+fYJ6\nAlRr0e3yahzpImp/cl4ymGX7VKv+wz+7X3ZD0jTttKm7bxMz5gtjXALot2pdQzM8\ns/ivu2qlA6k9fju9QeIOg4Q39QMNw0tbmBqmnYyN4v/fVpeNMtxUv9pBAoGAZNMn\nB9yaGhDcq/KGTLZk/yZfzIhkWf71wrIBrUa8bjuTsUKRqC6sI7DKlH4wZO3THwGC\nUDng8mtxMEVIzhwRCs8DyElrKwNESm3Vq5d94XtvYyJKNIQVZRhLf857YAg8TMIr\nHJhyEUU9nS3/56AXIPf6KQ4gIA/mzXKIzA0k3wECgYBYWJcCDljIXArSvahV0smP\nJ5Nhp5IBM1PQFdDySakDW3IEK8lZyeWrfNBatg/0rxjnGqxQ30xxYRRX6D9rihAv\n88nICKyRVQQY2vsuLZsuM4LlsfawGolIhTUsFxbaJNskiym/P+8I6xa+vxVvDEIm\n1rsNPvnqqCc7HbXV75Upmw==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@repaper-18551.iam.gserviceaccount.com",
  "client_id": "106150029686915053334",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40repaper-18551.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# Initialize Firebase Admin SDK
cred = credentials.Certificate(securityjson)  # Update with your JSON file path
print(cred)
firebase_admin.initialize_app(cred)
db = firestore.client()

def log_weight():
    try:
        # Get input
        print("\nRepaper Weight Logger")
        user_id = input("Enter user ID (Firebase UID from Firestore 'users' collection): ")
        weight = float(input("Enter paper weight in kg (e.g., 0.5): "))
        if weight <= 0:
            print("Error: Weight must be positive!")
            return

        # Calculate credits
        credits = int(weight * 10)  # 10 points per kg

        # Store in paper_logs
        log = {
            "userId": user_id,
            "weight": weight,
            "credits": credits,
            "timestamp": time.time()
        }
        db.collection("paper_logs").add(log)

        # Update user credits
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()
        if user.exists:
            current_credits = user.to_dict().get("credits", 0)
            new_credits = current_credits + credits
            user_ref.update({"credits": new_credits})
            print(f"Success: Logged {weight}kg, added {credits} credits for user {user_id}")
            print(f"Total Credits: {new_credits}")
        else:
            print(f"Error: User {user_id} not found in Firestore! Register user via webpage first.")

    except ValueError:
        print("Error: Invalid input! Please enter a valid number for weight.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        log_weight()
        again = input("\nLog another weight? (y/n): ")
        if again.lower() != "y":
            print("Exiting Repaper Weight Logger. Keep recycling!")
            break