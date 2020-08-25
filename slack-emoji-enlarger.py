import requests
import argparse
import sys
import subprocess
from pathlib import Path
from math import ceil
from time import sleep

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n\n" % message)
        print("help text:")
        self.print_help()
        sys.exit(2)
        
parser = MyParser(description="functionality: enlarge an image or gif and split into a grid and upload each grid piece as a slack emoji in order to create the look of an enlarged slack emoji")

parser.add_argument("file_path", help="path to image or gif to enlarge and upload")
parser.add_argument("size_dimension", help="which dimension the enlarged size will be given in, either 'width' or 'height'", choices=["width", "height"])
parser.add_argument("size", type=int, help="number of 128x128 emoji grid pieces either per column (height) or row (width-size) in final output")
parser.add_argument("emoji_base_name", help="base name of emojis to be uploaded. all emoji names will be of the form :{emoji_base_name}-{X}: where X is the index of the emoji within the grid from left to right, top to bottom, with leading zeros so that all corresponding emoji names are the same width")
parser.add_argument("slack_subdomain", help="the subdomain of the slack workspace where you want to upload the emojis: {slack-subdomain}.slack.com")
parser.add_argument("slack_user_token", help="a slack user token from the slack-subdomain. usually starts with 'xox'")
parser.add_argument("-d", "--dry_run", help="enlarge and create tiles but don't upload", action="store_true")

args = parser.parse_args()

if Path(args.file_path).suffix in [".jpg", ".jpeg"]:
    new_file_path = "{path_except_suffix}.png".format(path_except_suffix=Path(args.file_path).with_suffix(""))
    convert_to_png_cmd = "convert {file_path} {new_file_path}".format(file_path=args.file_path, new_file_path=new_file_path).split()
    print(" ".join(convert_to_png_cmd))
    subprocess.run(convert_to_png_cmd)
    args.file_path = new_file_path
    
Path(args.emoji_base_name).mkdir(exist_ok=True)

resized_path = Path("{directory}/{file_stem}{file_type}".format(directory=args.emoji_base_name, file_stem=args.emoji_base_name, file_type=Path(args.file_path).suffix))
file_type = resized_path.suffix

resize_cmd_str = "convert {file_path} -resize {resized_width}x{resized_height} {resized_path}"
if file_type == ".gif": resize_cmd_str = "gifsicle --colors 256 --resize {resized_width}x{resized_height} -o {resized_path} {file_path}"
empty_size_char = ""
if file_type == ".gif": empty_size_char = "_"

SLACK_EMOJI_DIMENSION_SIZE = 128

resize_cmd = resize_cmd_str.format(
        file_path=args.file_path,
        resized_width=args.size*SLACK_EMOJI_DIMENSION_SIZE if args.size_dimension == "width" else empty_size_char,
        resized_height=args.size*SLACK_EMOJI_DIMENSION_SIZE if args.size_dimension == "height" else empty_size_char,
        resized_path=str(resized_path)
        ).split()

print(" ".join(resize_cmd))
subprocess.run(resize_cmd)

get_sizes_cmd = "identify -format %wx%h {resized_path}".format(resized_path=resized_path).split()
if file_type == ".gif": get_sizes_cmd = "gifsicle --sinfo {resized_path}".format(resized_path=resized_path).split()

sizes = subprocess.run(get_sizes_cmd, capture_output=True).stdout.decode("utf-8")
if file_type == ".gif": sizes = sizes.split("\n")[1].split()[-1]

width, height = (int(size) for size in sizes.split("x"))

num_rows = ceil(height/SLACK_EMOJI_DIMENSION_SIZE)
num_cols = ceil(width/SLACK_EMOJI_DIMENSION_SIZE)
tile_number_width = len(str(num_rows*num_cols-1))

paste_rows = []

for row in range(num_rows):
    paste_row = []
    
    for col in range(num_cols):
        tile_number = row*num_cols + col
        
        tile_path = Path("{path_except_suffix}-{tile_number:0{tile_number_width}}{file_type}".format(
            path_except_suffix=resized_path.with_suffix(""),
            tile_number=tile_number,
            tile_number_width=tile_number_width,
            file_type=file_type)
            )

        tile_crop_cmd = "convert {resized_path} -crop {slack_emoji_width}x{slack_emoji_height}+{X}+{Y} -background none -gravity northwest -extent 128x128 {tile_path}".format(
                resized_path=resized_path,
                slack_emoji_width=SLACK_EMOJI_DIMENSION_SIZE,
                slack_emoji_height=SLACK_EMOJI_DIMENSION_SIZE,
                X=col*SLACK_EMOJI_DIMENSION_SIZE,
                Y=row*SLACK_EMOJI_DIMENSION_SIZE,
                tile_path=tile_path
                ).split()
        
        if file_type == ".gif":
            tile_crop_cmd = "gifsicle -O3 --lossy=20 --crop {X},{Y}+{slack_emoji_width}x{slack_emoji_height} -o {tile_path} {resized_path}".format(
                    X=col*SLACK_EMOJI_DIMENSION_SIZE,
                    Y=row*SLACK_EMOJI_DIMENSION_SIZE,
                    slack_emoji_width=SLACK_EMOJI_DIMENSION_SIZE,
                    slack_emoji_height=SLACK_EMOJI_DIMENSION_SIZE,
                    tile_path=tile_path,
                    resized_path=resized_path
                    ).split()

        print(" ".join(tile_crop_cmd))
        subprocess.run(tile_crop_cmd)
        
        emoji_name = "{emoji_base_name}-{tile_number:0{tile_number_width}}".format(
                emoji_base_name=args.emoji_base_name,
                tile_number=tile_number,
                tile_number_width=tile_number_width
                )
        
        paste_row.append(":{emoji_name}:".format(emoji_name=emoji_name))
        
        if not args.dry_run:
            sleep(2)
            
            with open(str(tile_path), "rb") as image_file:
                url = "https://{subdomain}.slack.com/api/emoji.add".format(subdomain=args.slack_subdomain)
                
                data = {
                  "mode": "data",
                  "name": emoji_name,
                  "token": args.slack_user_token
                }
                files = {"image": image_file}

                res = requests.post(url, data=data, files=files, allow_redirects=False)
                print(res.text)

    paste_rows.append("".join(paste_row))

user_paste_string = "\n".join(paste_rows)
slackbot_paste_string = "\\n".join(paste_rows)

print("USER PASTE STRING:")
print(user_paste_string)
print()
print("SLACKBOT PASTE STRING:")
print(slackbot_paste_string)
