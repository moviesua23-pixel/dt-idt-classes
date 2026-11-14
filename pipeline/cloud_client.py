import os
import sys
import json
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

DEFAULT_SA_PATH = os.path.join(PROJECT_ROOT, 'config', 'service_account.json')
ALT_SA_PATH = r'C:\Users\HP\OneDrive\Desktop\VISHNU\Auto Posting to Insta\instagram-auto-poster-503210-e850cd7ca998.json'

DRIVE_ROOT_ID = os.getenv('DRIVE_ROOT_ID', '1riykckqyQGHi89TuZsMn97bAUq3iQg8i')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', '14O9I8ZAjnIp8i4SFtM0xZX-y62f5BNtdh25ibSC7ChE')

SHEET_HEADERS = [
    "Subject",
    "Chapter No",
    "Question No",
    "Question",
    "Answer",
    "Provisions",
    "Provision Summary",
    "Malayalam Narration & Timings"
]

class CloudClient:
    def __init__(self, key_path=None):
        if not key_path:
            key_path = DEFAULT_SA_PATH if os.path.exists(DEFAULT_SA_PATH) else ALT_SA_PATH
            
        sa_json_env = os.getenv('GCP_SA_KEY')
        if sa_json_env:
            try:
                info = json.loads(sa_json_env)
                self.creds = service_account.Credentials.from_service_account_info(
                    info,
                    scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
                )
            except Exception:
                self.creds = service_account.Credentials.from_service_account_file(
                    key_path,
                    scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
                )
        else:
            self.creds = service_account.Credentials.from_service_account_file(
                key_path,
                scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
            )

        self.drive = build('drive', 'v3', credentials=self.creds)
        self.sheets = build('sheets', 'v4', credentials=self.creds)
        self._folder_cache = {}

    def get_or_create_folder(self, folder_name, parent_id=None):
        parent_id = parent_id or DRIVE_ROOT_ID
        cache_key = f"{parent_id}_{folder_name}"
        if cache_key in self._folder_cache:
            return self._folder_cache[cache_key]

        query = f"'{parent_id}' in parents and name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        results = self.drive.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])

        if files:
            folder_id = files[0]['id']
        else:
            metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }
            folder = self.drive.files().create(body=metadata, fields='id').execute()
            folder_id = folder.get('id')

        self._folder_cache[cache_key] = folder_id
        return folder_id

    def upload_pdf(self, file_path_or_bytes, filename, subject="DT"):
        target_folder = subject.upper()
        folder_id = self.get_or_create_folder(target_folder, DRIVE_ROOT_ID)

        if isinstance(file_path_or_bytes, (bytes, bytearray)):
            media = MediaIoBaseUpload(io.BytesIO(file_path_or_bytes), mimetype='application/pdf', resumable=True)
        else:
            media = MediaFileUpload(file_path_or_bytes, mimetype='application/pdf', resumable=True)

        # Check existing file
        query = f"'{folder_id}' in parents and name = '{filename}' and trashed = false"
        res = self.drive.files().list(q=query, fields='files(id)').execute().get('files', [])

        file_metadata = {'name': filename, 'parents': [folder_id]}
        if res:
            file_id = res[0]['id']
            updated = self.drive.files().update(fileId=file_id, media_body=media, fields='id, webViewLink').execute()
            return updated['id'], updated.get('webViewLink')
        else:
            created = self.drive.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
            return created['id'], created.get('webViewLink')

    def upload_voice_clip(self, q_num, clip_name, file_path_or_bytes):
        voice_root_id = self.get_or_create_folder("Voice", DRIVE_ROOT_ID)
        q_folder_name = f"Q{q_num}" if not str(q_num).upper().startswith("Q") else str(q_num).upper()
        q_folder_id = self.get_or_create_folder(q_folder_name, voice_root_id)

        if isinstance(file_path_or_bytes, (bytes, bytearray)):
            media = MediaIoBaseUpload(io.BytesIO(file_path_or_bytes), mimetype='audio/mpeg', resumable=True)
        else:
            media = MediaFileUpload(file_path_or_bytes, mimetype='audio/mpeg', resumable=True)

        query = f"'{q_folder_id}' in parents and name = '{clip_name}' and trashed = false"
        res = self.drive.files().list(q=query, fields='files(id)').execute().get('files', [])

        file_metadata = {'name': clip_name, 'parents': [q_folder_id]}
        if res:
            file_id = res[0]['id']
            f = self.drive.files().update(fileId=file_id, media_body=media, fields='id, webContentLink').execute()
        else:
            f = self.drive.files().create(body=file_metadata, media_body=media, fields='id, webContentLink').execute()
            file_id = f['id']

        # Ensure public read permissions for direct browser audio streaming
        try:
            self.drive.permissions().create(
                fileId=file_id,
                body={'type': 'anyone', 'role': 'reader'}
            ).execute()
        except Exception:
            pass

        stream_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        return file_id, stream_url

    def init_google_sheet(self, tab_name="Sheet1"):
        # Check current headers
        result = self.sheets.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{tab_name}!A1:H1"
        ).execute()
        rows = result.get('values', [])
        if not rows or rows[0] != SHEET_HEADERS:
            self.sheets.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=f"{tab_name}!A1:H1",
                valueInputOption='RAW',
                body={'values': [SHEET_HEADERS]}
            ).execute()
            print(f"Initialized Google Sheet with headers: {SHEET_HEADERS}")

    def append_or_update_question_row(self, row_data, tab_name="Sheet1"):
        self.init_google_sheet(tab_name)
        
        # Read all rows to find if question already exists
        result = self.sheets.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{tab_name}!A:H"
        ).execute()
        rows = result.get('values', [])

        subject = row_data.get("Subject", "DT")
        ch_no = str(row_data.get("Chapter No", ""))
        q_no = str(row_data.get("Question No", ""))

        target_row_idx = None
        for idx, r in enumerate(rows[1:], start=2): # 1-indexed, starting after header
            if len(r) >= 3 and r[0] == subject and str(r[1]) == ch_no and str(r[2]) == q_no:
                target_row_idx = idx
                break

        row_values = [
            row_data.get("Subject", "DT"),
            row_data.get("Chapter No", ""),
            row_data.get("Question No", ""),
            row_data.get("Question", ""),
            row_data.get("Answer", ""),
            row_data.get("Provisions", ""),
            row_data.get("Provision Summary", ""),
            row_data.get("Malayalam Narration & Timings", "")
        ]

        if target_row_idx:
            # Update existing row
            range_to_update = f"{tab_name}!A{target_row_idx}:H{target_row_idx}"
            self.sheets.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_to_update,
                valueInputOption='USER_ENTERED',
                body={'values': [row_values]}
            ).execute()
            print(f"Updated {subject} {q_no} at row {target_row_idx}")
        else:
            # Append new row
            self.sheets.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=f"{tab_name}!A:H",
                valueInputOption='USER_ENTERED',
                body={'values': [row_values]}
            ).execute()
            print(f"Appended new question {subject} {q_no}")

    def get_all_sheet_rows(self, tab_name="Sheet1"):
        result = self.sheets.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{tab_name}!A:H"
        ).execute()
        rows = result.get('values', [])
        if not rows:
            return []
        headers = rows[0]
        data = []
        for r in rows[1:]:
            item = {}
            for col_i, h in enumerate(headers):
                item[h] = r[col_i] if col_i < len(r) else ""
            data.append(item)
        return data

cloud_client = CloudClient()
