# Szurubooru-Grabber Script

----------


## Description
A script to automate uploading images, along with their data, to a szurubooru imageboard as they are saved using [Grabber](https://github.com/Bionus/imgbrd-grabber).

## Requirements

* Python 3 (>=3.6)
* [Grabber](https://github.com/Bionus/imgbrd-grabber)
  
## Usage
1. **Download** the [szurubooru.py](https://github.com/Tkompuras/Szurubooru-Grabber-Script/archive/main.zip) file and place it in the root directory of your Grabber installation
2. **Open and edit** the lines 8-10 according to your info, **username** (Go to account tab), **token** ("Login tokens" tab in your account tab), **api_url** (Should be 'http://localhost:8080/api' if you did a default installation)
3. Open **Grabber**, go to **Tools**, go to **Options (Ctrl-P)**, then **Commands** and in the image field enter: <br /> ```python szurubooru.py "%all:includenamespace,unsafe,underscores%" "%rating%" "%source:unsafe%" "%path%"```
4. Just save an image anywhere and it should automatically be uploaded to your szurubooru server.

## Warnings
* The script doesn't automatically delete the images after they are saved so keep that in mind.

## License
[MIT](https://choosealicense.com/licenses/mit/)

