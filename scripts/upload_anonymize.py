import os, sys, httpx

ORTHANC_URL = "http://localhost/dicom-web"

def process_dicom(input_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(('.dcm', '.ima')):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    res = httpx.post(f"{ORTHANC_URL}/studies",
                                     content=f.read(),
                                     headers={"Content-Type": "application/dicom"})
                    if res.status_code == 200:
                        print(f"Uploaded: {file}")
                    else:
                        print(f"Failed: {file} - {res.status_code}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python upload_anonymize.py <input_dir>")
        sys.exit(1)
    process_dicom(sys.argv[1])
