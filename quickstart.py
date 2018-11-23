from __future__ import print_function
from googleapiclient.discovery import build, MediaFileUpload
from googleapiclient.http import    MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
import io

SCOPES = 'https://www.googleapis.com/auth/drive'

def auth():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service

def list_folder(folder_id):
    service = auth()

    results = service.files().list(q="'" + folder_id + "' in parents and trashed=false").execute()

    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            print("{0}\tID: {1}".format(item['name'], item['id']))

def create_folder(folder_name, parent_id=None):
    service = auth()

    folder = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    if parent_id:
        folder['parents'] = [parent_id]

    file = service.files().create(body=folder, fields='id').execute()

    print('Folder ID: %s' % file.get('id'))

def move(file_id, folder_id):
    service = auth()
    # Retrieve the existing parents to remove
    file = service.files().get(fileId=file_id, fields='parents').execute()

    previous_parents = ",".join(file.get('parents'))

    # Move the file to the new folder
    file = service.files().update(fileId=file_id, addParents=folder_id, removeParents=previous_parents, fields='id, parents').execute()


def copy(file_id, folder_id):
    service = auth()

    # Copy the file to the new folder
    file = service.files().update(fileId=file_id, addParents=folder_id, fields='id, parents').execute()


def trash(file_id):
    service = auth()

    file_metadata = {
        'trashed': 'true'
    }

    # Copy the file to the new folder
    file = service.files().update(body=file_metadata, fileId=file_id).execute()


def upload(file_path, file_name, folder_id):
    service = auth()

    file_metadata = {
        'name': file_name,
        'parents' : [folder_id]
    }

    media = MediaFileUpload(file_path)

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()


def download(file_id, filename):
    service = auth()

    request = service.files().get_media(fileId=file_id)

    fh = io.FileIO(filename, 'wb')

    downloader = MediaIoBaseDownload(fh, request)

    done = False

    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


if __name__ == '__main__':

    #upload('anime.py', 'anime.py', '1d_RGV3PC5748ZB00RMgBkEIBgqRW40n6')

    download('1Y9fNp_b16MOen65B4mNmB4LcGH9OKBCf', 'pintos.pdf')

    list_folder('root')
