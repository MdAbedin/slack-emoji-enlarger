# slack-emoji-enlarger

A command-line tool to split an image or gif into tiles and upload each as a slack emoji to create the illusion of an enlarged slack emoji

![example of enlarged slack emoji image](https://user-images.githubusercontent.com/18149939/91142815-77996c80-e67f-11ea-87ec-08996111848a.png)

![enlarged emoji image wtih spacing between individual emojis](https://user-images.githubusercontent.com/18149939/91142862-8f70f080-e67f-11ea-9fcd-7a24ee56aa3d.png)

![exmaple of enlarged slack emoji gif](https://user-images.githubusercontent.com/18149939/91186739-640cf680-e6bd-11ea-8b67-1414417bdc85.gif)

## Dependencies

- [Python3](https://www.python.org/downloads/)
- If you're using images, [ImageMagick](https://imagemagick.org/script/download.php). If you install from source, you might have to install many other things to handle file formats, so it's best to install with a package manager
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
- `-h` or `--help`: show help message and exit
- `-d` or `--dry_run`: enlarge and create tiles but don't upload

## Usage Examples

- Enlarge an image `stonks.jpg` to have a height of 3 emojis where each emoji's name is `:stonks-big-00:`, `:stonks-big-01:`, etc. to the Slack workspace `coinbase.slack.com` using your Slack user token `xoxs-123456789`:
  - `python3 slack-emoji-enlarger.py stonks.jpg height 3 stonks-big coinbase xoxs-123456789`

## Notes
- You might have to soft refresh (`Ctrl + R` or `Cmd + R`) Slack in order for gif tiles to sync
- Large or rapid usages might run into rate limiting from Slack. You can re-run your command after waiting for a bit in order to retry all uploads
- Large gif enlargements may cause lag or crashes in Slack
- Some gifs may be too large in file size even after the lossy compression from this tool. You can try increasing GIF_COMPRESSION and re-running your command to retry all uploads with increased compression

## Planned Features
- Auto-retry uploads that fail due to rate limiting
- Provide a GUI alongside the CLI for easier use and to easily preview the results before uploading
- Option to use email and password instead of Slack token
- Option to show details and ask for confirmation before starting the process
- Option to delete exisiting emojis with the same name before uploading
- Option to delete all emoji tiles from a previous upload
