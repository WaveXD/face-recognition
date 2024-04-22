import datetime
import firebase_admin
from firebase_admin import credentials, firestore, storage
import face_recognition
import requests
from io import BytesIO
import json

# Initialize Firebase admin
cred = credentials.Certificate("C:/Users/Wave/Desktop/finalproject/backend/database-8b747-firebase-adminsdk-5gshe-eea9fb1dcc.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'database-8b747.appspot.com'
})

def extract_face_encodings(image_url):
    """Extract face encodings from an image URL."""
    response = requests.get(image_url)
    image = face_recognition.load_image_file(BytesIO(response.content))
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings

def save_encodings_to_firestore(user_name, encodings):
    """Save face encodings to Firestore."""
    db = firestore.client()
    db.collection('users').document(user_name).set({
        'face_encodings': [json.dumps(encoding.tolist()) for encoding in encodings],
        'processed': True
    }, merge=True)
   

def check_if_processed(user_name):
    """Check if the user's image has already been processed."""
    db = firestore.client()
    doc_ref = db.collection('users').document(user_name)
    doc = doc_ref.get()
    if doc.exists:
        if doc.to_dict().get('processed'):
            return True
    return False

def list_and_process_images():
    """get images from photoURL and process them."""
    db = firestore.client()
    docs = db.collection('users').stream()
    for doc in docs:
        user_name = doc.id
        photoURL = doc.to_dict().get('photoURL')
        if not check_if_processed(user_name):
            encodings = extract_face_encodings(photoURL)
            save_encodings_to_firestore(user_name, encodings)
            print(f'{user_name} processed.')
        else:
            print(f'{user_name} already processed.')








if __name__ == "__main__":
    list_and_process_images()
