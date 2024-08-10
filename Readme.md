# Video Shazam
## Description
This script will parse a folder of videos and retrieve the songs that are played in the videos, for example extracting a series soundtrack.

## Usage
1. Create a [pro shazam account](https://rapidapi.com/diyorbekkanal/api/shazam-api6) (10$ a month)
1. Add a `.env` file at the root folder with your RapidApi key ```RAPID_API_KEY=YOUR_KEY```
1. Install dependencies ```pip3 install .``` from root of the project
1. Run command ```python3 ./src/main.py -i PATH_TO_VIDEO