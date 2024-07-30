import requests
import base64

### initial settings
# image_path = '../95079.jpg'    # need to be changed
try:
    api_key = open('api_key','r').read()
except FileNotFoundError:
    api_key = ""
    
### function definition
def detect_text(image_path, api_key):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()

    json_request = {
        "requests": [
            {
                "image": {
                    "content": base64_image
                },
                "features": [
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }
        ]
    }
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    
    response = requests.post(url, json=json_request)
    result = response.json()
    if response.status_code == 200:
        return result['responses'][0]['textAnnotations'][0]['description']
    else:
        return result.get("error", {})
    
### calling function
# text = detect_text(image_path, api_key)