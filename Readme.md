# Video Shazam
## Description
This script will parse a folder of videos and retrieve the songs that are played in the videos, for example extracting a series soundtrack.

## Usage
1. Create a [pro shazam account](https://rapidapi.com/diyorbekkanal/api/shazam-api6) (10$ a month)
1. Follow the [guide to create a spotify developer account](https://www.youtube.com/watch?v=kaBVN8uP358&ab_channel=DanArwady)
1. Add a `.env` file at the root folder with your RapidApi key
    ```
    RAPID_API_KEY=YOUR_KEY
    SPOTIFY_CLIENT_ID=YOUR_ID
    SPOTIFY_CLIENT_SECRET=YOUR_SECRETE
    SPOTIFY_REDIRECT_URI=YOUR_REDIRECT_URI
    ```
1. Install dependencies ```pip3 install .``` from root of the project

### For video parsing
1. Run command ```python3 ./src/main.py -i PATH_TO_VIDEO```

### For Playlist resolusion and creation
1. Run command ```python3 ./src/main.py -n PATH_TO_SONGS_JSON```
Json example - title and artists are the only required fields
```
{
    "Letterkenny.S01E04.DVDRip.x264-TAXES6i7tpvzj_splittdhpxx2e": [
        {
            "title": "That's It, That's All",
            "artist": "We Are the City",
            "original_file": "Letterkenny.S01E04.DVDRip.x264-TAXES6i7tpvzj_splittdhpxx2e",
            "time": "00:20:40",
            "accuracy": 0.01
        },
        {
            "title": "Tries",
            "artist": "Kaboom Atomic & Aalo Guha",
            "original_file": "Letterkenny.S01E04.DVDRip.x264-TAXES6i7tpvzj_splittdhpxx2e",
            "time": "00:05:15",
            "accuracy": 0.01
        },
        {
            "title": "Haunted House",
            "artist": "Dead Ghosts",
            "original_file": "Letterkenny.S01E04.DVDRip.x264-TAXES6i7tpvzj_splittdhpxx2e",
            "time": "00:08:40",
            "accuracy": 0.01
        }
    ],
    "Letterkenny.S01E01.DVDRip.x264-TAXESbfivbs83_splitc16u04p7": [
        {
            "title": "Everyone Looks Like Everyone",
            "artist": "The Pack a.d.",
            "original_file": "Letterkenny.S01E01.DVDRip.x264-TAXESbfivbs83_splitc16u04p7",
            "time": "00:20:40",
            "accuracy": 0.01
        },
        {
            "title": "Wolf Pack",
            "artist": "Pigeon Hole",
            "original_file": "Letterkenny.S01E01.DVDRip.x264-TAXESbfivbs83_splitc16u04p7",
            "time": "00:22:45",
            "accuracy": 0.01
        },
        {
            "title": "Save Me (feat. Katy B)",
            "artist": "Keys N Krates",
            "original_file": "Letterkenny.S01E01.DVDRip.x264-TAXESbfivbs83_splitc16u04p7",
            "time": "00:09:50",
            "accuracy": 0.01
        },
        {
            "title": "Sucker for a Man With a Boody",
            "artist": "Zabrina",
            "original_file": "Letterkenny.S01E01.DVDRip.x264-TAXESbfivbs83_splitc16u04p7",
            "time": "00:15:40",
            "accuracy": 0.01
        },
        {
            "title": "Big League Chew",
            "artist": "day hike",
            "original_file": "Letterkenny.S01E01.DVDRip.x264-TAXESbfivbs83_splitc16u04p7",
            "time": "00:01:05",
            "accuracy": 0.01
        }
    ]
}
```

### For webcrawling tunefind
1. Install Playright dependencies ```sudo playwright install-deps```
1. Run command ```playright install```
1. Run command ```python3 ./src/main.py -t TUNEFIND_SERIES_URL```