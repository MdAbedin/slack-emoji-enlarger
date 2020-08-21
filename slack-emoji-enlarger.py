import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="the image to enlarge and upload")
args = parser.parse_args()
print(args.echo)
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
