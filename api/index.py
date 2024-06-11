from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import speech, storage
from google.oauth2 import service_account
from pydub import AudioSegment


app = FastAPI(
    title="ICC Transcription API",
    timeout=7200,
)

api_key = 'AIzaSyC-2h5qSYjd9MRPzrCZ'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

credentials_details = {
    "type": "service_account",
    "project_id": "icc-tag-dom",
    "private_key_id": "9f74e2a80aaf443d2f9fc210448069cbdfe182a9",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQD6wgfW82CCbTzH\nGOnxHfHEqGFFfdRFnmgCKPJKU7IfXdxb9+G/tx6oVJX8o1QReoX0WxvMqZxhJ3Ut\n0Aj4pPeZKlBMvLCgwYbYcdb6Tewi3C51y8CfFo2zLORG0yxe5gd6YqDSZMI5iLJX\notycUAtseW1C5kDErq1Ir1+n6tlFCEq00cpte83Y8ZzHhVkXYYu+LC0gQqIaqdFh\nT6nRv3HVAQRrRMvDjpUBIdql0YHIBSzr0EPjl+yDqs/qSihja+JZebzLq8ptgTlK\nT7wACNymwviNWG/Dvt25PFmoWR+enEwoj+iQDy7RmmMVfnjPmKVFqb14fUuJ7iha\nquVwZRNfAgMBAAECggEAFY9dmDGIdekJhZQn99IbdE1b67B+x1ZFhWYFiwwjhQc6\nHUg0se9Uj07n2cx7O8jSlVNzZ5yaXvoYXPja70dT0z4BoHoaylT0EKPHwvFfNmdt\nsTV0btlEFAiYlK8Ed3ZaDz+aqexS4hqAPFZllyUEuRi++GEOvDpz7gtyHeBsj5Q+\n3MF2zpEuhKLUqiXv3CJxPsdN9paVttjri6rLOK+F8ZwVcqK/RplBB1qn/qJXo9YJ\nVL53kn6i/O3UBs8M5x6rR0k4ri+Ijv/XG/UOVA7dwL0u3YU+G+M0Quaf3/Taeh5w\nVMsXe+20eUmkt/cRkydpgdUiTBFIyU4O3MVUriahYQKBgQD/Xbz/WaXPCvRbv3vh\nNHgoNKBcbradRV0NvRLOj9xMj+PJXD6LEtPoMoWbBoaeWznUe1U8UWYe6qkE8A+r\njhEbCbxGnxMTio3OkhMgOPH1tjwrOaAqR+5DIjUXFLRSPJaLDuqELhQN7HcyD1cw\n+azlY/XzBLsXE1LgEo4xorWp4QKBgQD7YV0/FAxnSmkrwVNVETsOyDG2kz/Yswu7\nzuXWTmZx4m1/kTkIwXwMmjoOByYyiUG/fQlWaXSeaARsIABdAiOwj1BtVZqkR9/W\npO+YrPMn7MBGppMh+Q5JKA0vFyaLBgrSe36JEWJWrc+9o0QRPUVhAliccYVsiX+C\nJ3+f3/rlPwKBgQD3Lvg7v74EzFi92nsCAfTxDgfPkQdI8pRhMQxcT9pxbbKS/aw4\nmE/wab7z0XxLGoi+yWc3DJ+p+4EBm5G/gLPEFUdeoKopdytOsgy7WwOy0OQq/wuv\nAZN6/kiff9YP6D/ceOK+cY/N7n9uQHUonfUi0gCHbKPgcT7+UFe9af8oYQKBgQCe\nesqTqusK74GQgUgtGDjYX+Pfi8OztWVPWOfTjQfPAoYv53lCiODQ/SZek6lEMP5P\nX9/UJ5XLDB7FoAM6n8+qTx/QXiipK1r18nPPGDIP2JV7tSaLQ337JxHwvzKgcQW/\nnvWuKlSJ+vg+QUD3cV5dA2Kj9nm8bI8Dmi0+uLFvdwKBgQCN8GJTXmZ+1nWge/TC\nT9Gfxu0yGtJiOPHm/OJID44/5OBKUG+N18ZnI0Eqn4GZW3yXn3L7rXPnQ/0C0ctm\nzfomDGRsZ4ny3RI94OgzxS1IO41YMftVnZ64zx6APNNMdHRjmnYSVUBED+Q7Kc8A\njfJ1WYPzQl9/HnMCb4umgrKhnw==\n-----END PRIVATE KEY-----\n",
    "client_email": "transcription-icc@icc-tag-dom.iam.gserviceaccount.com",
    "client_id": "107074308950613438660",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/transcription-icc%40icc-tag-dom.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

credentials = service_account.Credentials.from_service_account_info(
    credentials_details)
client = speech.SpeechClient(credentials=credentials)

storage_client = storage.Client.from_service_account_info(credentials_details)
bucket_name = 'icc-transcription-bucket'
bucket = storage.Bucket(storage_client, 'icc-transcription-bucket')


@app.get("/api/trial")
def hello():
    print("hello")


@app.post("/api/transcribe")
async def transcribe_file(file: UploadFile = File(...)):
    try:

        # Uploading the file to Google Cloud Storage
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file.file, content_type=file.content_type)

        # Getting the GCS path of the uploaded file
        gcs_path = f"gs://{bucket_name}/{file.filename}"

        # Downloading the audio content from GCS
        mp3_blob = bucket.blob(file.filename)
        audio_content = mp3_blob.download_as_bytes(timeout=12000)

        # Creating the AudioSegment and getting sample rate
        audio = AudioSegment.from_file(BytesIO(audio_content), format="mp3")
        sample_rate = int(audio.frame_rate)

        # Configuring Speech-to-Text
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=sample_rate,
            language_code="sw",  # Update with your desired language code
        )

        # Creating RecognitionAudio object with GCS URI
        audio = speech.RecognitionAudio(uri=gcs_path)

        # Initiating a long-running transcription
        operation = client.long_running_recognize(
            config=config, audio=audio, timeout=7200)

        print("Waiting for operation to complete...")
        response = operation.result()

        # Building transcript
        transcript_builder = []
        for result in response.results:
            transcript_builder.append(f"{result.alternatives[0].transcript}")

        transcript = "".join(transcript_builder)
        print(transcript)

        return {"transcript": transcript_builder}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An error occurred during file transcription."
        )
