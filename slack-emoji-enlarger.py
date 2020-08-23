import requests
import argparse
import sys
import subprocess
from pathlib import Path

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n\n" % message)
        print("help text:")
        self.print_help()
        sys.exit(2)
        
parser = MyParser(description="functionality: enlarge an image or gif and split into a grid and upload each grid piece as a slack emoji in order to create the look of an enlarged slack emoji")

parser.add_argument("file_path", help="path to image or gif to enlarge and upload")
parser.add_argument("size_dimension", help="whether to specify enlarged emoji's width or height", choices=["width", "height"])
parser.add_argument("size", type=int, help="number of 128x128 emoji grid pieces either per column (vertical-size) or row (horizontal-size) in final output")
parser.add_argument("emoji_base_name", help="base name of emojis to be uploaded. all emoji names will be of the form :{emoji_base_name}{X}: where X is the index of the emoji within the grid from left to right, top to bottom")
parser.add_argument("slack_subdomain", help="the subdomain of the slack workspace where you want to upload the emojis: {slack-subdomain}.slack.com")
parser.add_argument("slack_user_token", help='a slack user token from the slack-subdomain. usually starts with "xox"')

args = parser.parse_args()

Path(args.emoji_base_name).mkdir(exist_ok=True)

SLACK_EMOJI_DIMENSION_SIZE = 128

resized_path = Path("{directory}/{file_stem}{file_type}".format(directory=args.emoji_base_name, file_stem=args.emoji_base_name, file_type=Path(args.file_path).suffix))

resize_cmd = "convert {file_path} -resize {resized_width}x{resized_height} {resized_path}".format(
        file_path=args.file_path,
        resized_width=args.size*SLACK_EMOJI_DIMENSION_SIZE if args.size_dimension == "width" else "",
        resized_height=args.size*SLACK_EMOJI_DIMENSION_SIZE if args.size_dimension == "height" else "",
        resized_path=str(resized_path)
        ).split()

tile_cmd = "convert {file_path} -crop {slack_emoji_width}x{slack_emoji_height} +repage +adjoin {tile_path}".format(
        file_path=str(resized_path),
        slack_emoji_width=SLACK_EMOJI_DIMENSION_SIZE,
        slack_emoji_height=SLACK_EMOJI_DIMENSION_SIZE,
        tile_path=str(resized_path)
        ).split()

print(" ".join(resize_cmd))
subprocess.run(resize_cmd)
print(" ".join(tile_cmd))
subprocess.run(tile_cmd)

tile_number = 0

while Path("{path_except_suffix}-{tile_number}{file_type}".format(path_except_suffix=resized_path.with_suffix(""), tile_number=tile_number, file_type=resized_path.suffix)).exists():
    tile_path = Path("{path_except_suffix}-{tile_number}{file_type}".format(path_except_suffix=resized_path.with_suffix(""), tile_number=tile_number, file_type=resized_path.suffix))
    print(tile_path)
    
    with open(str(tile_path), "rb") as image_file:
        url = "https://{subdomain}.slack.com/api/emoji.add".format(subdomain=args.slack_subdomain)
        data = {
          "mode": "data",
          "name": "{emoji_base_name}-{tile_number}".format(emoji_base_name=args.emoji_base_name, tile_number=tile_number),
          "token": args.slack_user_token
        }
        files = {"image": image_file}

        print(data)
        #  req = requests.post(url, data=data, files=files, allow_redirects=False)

    tile_number += 1
