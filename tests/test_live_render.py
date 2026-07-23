import ssl
import json
import urllib.request
import io
from PIL import Image

def test_live_render():
    url = "https://hydrogrow-ai-plant-doctor.onrender.com/api/vision/plant-analysis"
    img = Image.new('RGB', (224, 224), (40, 180, 50))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    img_bytes = buf.getvalue()

    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = bytearray()
    body.extend(f'--{boundary}\r\n'.encode('utf-8'))
    body.extend(b'Content-Disposition: form-data; name="file"; filename="leaf.jpg"\r\n')
    body.extend(b'Content-Type: image/jpeg\r\n\r\n')
    body.extend(img_bytes)
    body.extend(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(url, data=bytes(body), headers={
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    })

    print("Sending request to live Render server:", url)
    res = urllib.request.urlopen(req, context=ctx)
    print("Live Render Status Code:", res.getcode())
    data = json.loads(res.read().decode())
    print("Live Render Response JSON:", json.dumps(data, indent=2))

if __name__ == "__main__":
    test_live_render()
