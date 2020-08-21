import requests
import argparse

parser = argparse.ArgumentParser(description="enlarge an image or gif and split into a grid and upload each grid piece as a slack emoji in order to create the look of an enlarged slack emoji")
parser.add_argument("filename", help="the image or gif to enlarge and upload")
args = parser.parse_args()
print(args.filename)
    
quit()

url = 'https://{subdomain}.slack.com/api/emoji.add'

data = {
  'mode': 'data',
  'name': "test",
  'token': ""
}

with open("stonks.jpeg", 'rb') as f:
    files = {'image': f}
    x = requests.post(url, data=data, files=files, allow_redirects=False)
    print(x.text)
