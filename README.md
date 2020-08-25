# slack-emoji-enlarger

A command-line tool to split an image or gif into tiles and upload each as a slack emoji to create the illusion of an enlarged slack emoji

![example of enlarged slack emojis](https://user-images.githubusercontent.com/18149939/91142815-77996c80-e67f-11ea-87ec-08996111848a.png)

![enlarged emoji wtih spacing between individual emojis](https://user-images.githubusercontent.com/18149939/91142862-8f70f080-e67f-11ea-9fcd-7a24ee56aa3d.png)

## Dependencies

- [Python3](https://www.python.org/downloads/)
- If you're using images, [ImageMagick](https://imagemagick.org/script/download.php)
- If you're using gifs, [gifsicle](https://www.lcdf.org/gifsicle/)

## Usage
`python3 slack-emoji-enlarger.py file_path size_dimension size emoji_base_name slack_subdomain slack_user_token`

Required arguments:
- `file_path`: path to image or gif to enlarge and upload
- `size_dimension`: which dimension the enlarged size will be given in, either `width` or `height`
- `size`: number of 128x128 emoji tiles either per column (height) or row (width) in final output
- `emoji_base_name`: base name of emojis to be uploaded. all emoji names will be of the form `:{emoji_base_name}-{X}:` where `X` is the index of the emoji within the grid from left to right, top to bottom, with leading zeros so that all corresponding emoji names are the same width
- `slack_subdomain`: the subdomain of the slack workspace where you want to upload the emojis: {`slack-subdomain`}.slack.com
- `slack_user_token`:  a slack user token from the slack-subdomain. usually starts with "xox"

Optional arguments:
- `-h, --help`: show help message and exit

## Notes
