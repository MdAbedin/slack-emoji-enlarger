import requests
import argparse
import sys
import subprocess

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n\n' % message)
        print("help text:")
        self.print_help()
        sys.exit(2)
        
parser = MyParser(description="functionality: enlarge an image or gif and split into a grid and upload each grid piece as a slack emoji in order to create the look of an enlarged slack emoji")

parser.add_argument("file_path", help="path to image or gif to enlarge and upload")
parser.add_argument("size_dimension", help="whether to specify enlarged emoji's size vertically or horizontally", choices=["vertical-size", "vs", "horizontal-size", "hs"])
parser.add_argument("size", type=int, help="number of 128x128 emoji grid pieces either per column (vertical-size) or row (horizontal-size) in final output")
parser.add_argument("emoji_base_name", help="base name of emojis to be uploaded. all emoji names will be of the form :{emoji_base_name}{X}: where X is the index of the emoji within the grid from left to right, top to bottom")
parser.add_argument("slack_subdomain", help="the subdomain of the slack workspace where you want to upload the emojis: {slack-subdomain}.slack.com")
parser.add_argument("slack_user_token", help='a slack user token from the slack-subdomain. usually starts with "xox"')

args = parser.parse_args()

"""
print(args.file_path)
print(args.size_dimension)
print(args.size)
print(args.slack_subdomain)
print(args.slack_user_token)
"""

resize_cmd ="convert {file_path} -resize {resized_width}x{resized_height} {resized_path}"
tile_cmd = "convert {file_path} -crop {slack_emoji_width}x{slack_emoji_height} +repage +adjoin {tile_path_base}"
print(' '.join(resize_cmd))
subprocess.run(resize_cmd)
print(' '.join(tile_cmd))
subprocess.run(tile_cmd)
quit()

with open(args.file_path, 'rb') as image_file:
    url = "https://{subdomain}.slack.com/api/emoji.add".format(subdomain=args.slack_subdomain)
    data = {
      "mode": "data",
      "name": args.emoji_base_name,
      "token": args.slack_user_token
    }
    files = {'image': image_file}
    
    res = requests.post(url, data=data, files=files, allow_redirects=False)
    print(res.text)
