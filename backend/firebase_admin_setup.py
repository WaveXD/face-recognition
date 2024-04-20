import firebase_admin
from firebase_admin import credentials, firestore, storage

# ที่นี่คุณต้องแทนที่ "path/to/your/serviceAccountKey.json" ด้วยเส้นทางที่ถูกต้องไปยังไฟล์ serviceAccountKey.json ที่คุณดาวน์โหลดจาก Firebase
cred_data = {
  "type": "service_account",
  "project_id": "database-8b747",
  "private_key_id": "eea9fb1dcc71d374722fba2562ef51a93f7090fb",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCvDf2NC55lZOJA\n/jxlIq5v1my1JDJUMnYZT7/sMPwdYLRzOxIlWhGZzRA42+M5srrHCSi0sVQsIkRw\nXetUYUfVc6qksK/EHbvWoF+sYjf15TbylOyscmdz5JBhE2438IPfDwEBgrOrC/H1\nRxReqPjQLX7ZiJ88XRpMs79s0RXvNMfROJMqHQ0lKAPHB3bQYeEyY/maqWVEdKFc\nF7Knl4WV+oGCwmJ9FlECxBkxKzB1tujr+Wx7r1Na2Te+CY9v8Rdgl0U4AI4r0v7s\nUnoYNGcK1znO623Ou0Sk7WkudOiLpof+gEfyQHJumnAzDK/vziaIpEhw+jc8rb9/\nkLP6jYcjAgMBAAECggEAFiA7EYZL7X3sWRGpWZEiIjGkiNq738eHBNj/JZ/lZeMw\nu7XWK9FwExQHvmAQntzX3ctrETeur2tfYiKE2aP4G+MkSO+qL6wgb1bS8OtzLknc\nAZpQNdW5/LyBgTue/UQRrvJrCqFWC0MVwI5M5VAPLuTpOR6bHdqYteQsSFk/H/5C\n0mPLejsOKfACjZzA+7Yona/5VpNFQ7MK/hShatoEkinOtNsrEiKZ1GB1lRvaDtSi\niisa4XDrxx0qXVpND4hVz4OqiKE+gFfwjTzLqJV/IXTcafhJLpwJw9fMIyT3dATR\nBSLPG9/rHK8EMTHmn8IpScZFoFd/y2p3nxiEzh63vQKBgQDYV2g+2eYexUe/d45L\nnr9csaT7cYPkcsmk8lRXWUTqIHFUGdad6DNyg+JRHGMqB/+Ex/k9vVvkp+rCiuPm\n0m4eHMtfPpQZ/CMPGCV2dbE3hr4RdAQu7VE+gj1hpDrr2o/a6JLUEasTWtMnpICJ\nCvNaO2ciKlTHzO2juhcXtNUa/wKBgQDPJQ3BuyTqulwmKLWNxA60iKOz/NdRqMGC\neXGJRwQEyuYQ2Ud+4cGxo1ND6iZzGYaUvpj5dk7xx9cgFl6eb/IYxuU5LSZTqABi\nonxRtD88GIDg0NB+t7d9ofOiY+qyoPqVGuCqevuqrscOM7chcyWl54tzLddbmSef\nfFmUpmfH3QKBgGFkH/LDZzwM9bq1GKLkSSNyeWIUfRqXrj0KNnvIHSUFC9+fbiVS\nBe8Ufgqjq+SdCyN8XrCzkS3DhgSkP+qGaro1njw3ULbN8f52kU7dtrTXfLMgtk1l\n2oA4Y2eUZk4M61vR/V9owMoKxin/fTm0a08AlPIlelsj3wso2AJ9Dr6DAoGAHaHA\nUQlTY5ybF/5U0l3MeLjfKh0uNAk+/UogGrIk+gaIWLqsRpNG4QFrJNj2/RoWrWqC\neZUZ/+5FcNqiWGnNKQwyuDYkOG1c+L8jp5BwR0l+Dirw2F+xiPBE6OMALONoVTIO\nF3UWUTlFUlvFg6x0I0J3KVfSadED4QWpzuDrEaUCgYAyvhpGL6QXVr/4+/+DJGlT\nJqomJA5Y6yB7n7aBSyZDKW/FubvJx26VwE1F18pSbwGiczFWl0TKkLHXfHH0e3GC\nHqm4nALEcnsjflg+UqX2KzH9ZA0KNB2k9EWVB847a2645yUYdNUd1ZCzndfYPU9h\nSCWPvHaZszOd1iXeV+Zd8g==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-5gshe@database-8b747.iam.gserviceaccount.com",
  "client_id": "115368915921602947861",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-5gshe%40database-8b747.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(cred_data)

firebase_admin.initialize_app(cred, {
    'storageBucket': 'database-8b747.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()
