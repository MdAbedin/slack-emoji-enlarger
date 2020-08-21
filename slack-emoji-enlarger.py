import requests
import argparse

parser = argparse.ArgumentParser(description="enlarge an image or gif and split into a grid and upload each grid piece as a slack emoji in order to create the look of an enlarged slack emoji")

parser.add_argument("filename", help="the image or gif to enlarge and upload")

parser.add_argument("size_dimension", help="specify size vertically or horizontally", choices=["vertical-size", "vs", "horizontal-size", "hs"])

parser.add_argument("size", type=int, help="number of 128x128 emoji grid pieces either per column (vertical-size) or row (horizontal-size) in final output")

parser.add_argument("slack_subdomain", help="the subdomain of the slack workspace where you want to upload the emojis: {slack-subdomain}.slack.com")

parser.add_argument("slack_user_token", help='a slack user token from the slack-subdomain. usually starts with "xox"')

args = parser.parse_args()

print(args.filename)
print(args.size_dimension)
print(args.size)
print(args.slack_subdomain)
print(args.slack_user_token)
    
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
