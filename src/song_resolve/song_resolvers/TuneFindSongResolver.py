from urllib import request
from playwright.sync_api import sync_playwright, Page, Locator, Browser
from progressbar import ProgressBar

from song_resolve.song_resolvers.SongData import SongData


class TuneFindSongResolver:
    def __init__(self, series_url: str, all_songs: list[SongData]) -> None:
        self._series_url = series_url
        self._all_songs = all_songs
        self._browser: Browser = None

    def get_songs(self) -> list[SongData]:
        with sync_playwright() as s_playwright:
            self._playwright_context = s_playwright
            page = self._playwright_init(s_playwright)
            seasons = self._get_seasons(page)

            bar = ProgressBar(max_value=len(seasons)).start()
            for season in seasons:
                page = self._playwright_init(s_playwright)
                while True:
                    try:
                        self._get_season_songs(page, season)
                        break
                    except Exception as e:
                        print(f"Error getting songs for season {season}: {e}")
                        page = self._playwright_init(s_playwright)

                bar.increment()

            bar.finish()

        return self._all_songs

    def _playwright_init(self, s_playwright: sync_playwright) -> Page:
        if self._browser and self._browser.is_connected():
            self._browser.close()

        self._browser = s_playwright.chromium.launch(headless=False)
        context = self._browser.new_context()
        page = context.new_page()

        page.goto(self._series_url, wait_until="domcontentloaded")

        return page

    def _get_seasons(self, page):
        print("Getting seasons")
        # this wait for is needed because the page is not fully loaded
        page.locator(".DropdownSelect___StyledDiv-sc-r6nflk-0.lgzsqo > select > option").first.wait_for(state="attached")

        all_seasons = page.locator(".DropdownSelect___StyledDiv-sc-r6nflk-0.lgzsqo > select > option").all_inner_texts()

        return [season for season in all_seasons if season and season != "-"]

    def _get_season_songs(self, page: Page, season: str):
        print(f"Getting songs for season {season}")
        # select season
        season_selector = ".DropdownSelect___StyledDiv-sc-r6nflk-0.lgzsqo > select"
        page.locator(season_selector).select_option(season)

        # get episodes
        episode_selector = ".styles__StyledCardBorder-sc-1njjh38-3.sc-cDsqlO.ikwQk.bVwFkC"
        page.locator(episode_selector).first.wait_for(state="attached")

        episodes = page.locator(episode_selector).all()
        for episode in episodes:
            episode_title = self._get_episode_title(episode)
            print(f"Getting songs for episode {episode_title}")
            episode.click()

            # get all songs
            song_locator = ".ant-row.ant-row-no-wrap.ant-row-start.sc-gRtvSG.gVuIuB"
            page.locator(song_locator).first.wait_for()

            episode_songs_elements = page.locator(song_locator).all()
            episode_songs = self._get_episode_songs(episode_title, episode_songs_elements)

            self._all_songs.extend(episode_songs)

            page.go_back(wait_until="domcontentloaded")

    def _get_episode_songs(self, episode_title: str, episode_songs_elements: list[Locator]) -> list[SongData]:
        episode_songs = []

        for song_element in episode_songs_elements:
            song_block = song_element.locator(".ant-col").all()
            song_name, song_artists = self._get_song_details(song_block[0].inner_text())

            inner_text_2 = song_block[2].inner_text()
            timestamp = self._get_timestamp(inner_text_2)
            description = self._get_description(inner_text_2)

            spotify_track_id = self._get_spotify_track_id(song_block[3])

            episode_songs.append(
                SongData(
                    original_file=episode_title,
                    title=song_name,
                    artist=song_artists,
                    time=timestamp,
                    description=description,
                    track_id=spotify_track_id,
                )
            )

        return episode_songs

    def _get_episode_title(self, episode) -> str:
        episode_inner_texts = episode.all_inner_texts()
        if not episode_inner_texts:
            return ""
        return episode_inner_texts[0].split("\n")[0]

    def _get_song_details(self, song_text: str):
        song_name, song_artists = song_text.split("\n", 1)
        return song_name.strip(), song_artists.strip().replace("\n", " ")

    def _get_timestamp(self, song_text: str):
        return song_text[song_text.find("(") + 1 : song_text.find(")")]

    def _get_description(self, song_text: str):
        return song_text[song_text.find(")") + 2 :].strip()

    def _get_spotify_track_id(self, links_block: Locator) -> str:
        spotify_link = ""
        audio_links = links_block.locator("a").all()
        for link in audio_links:
            link_icon_alt_text = link.locator("img").first.get_attribute("alt")
            if "spotify" in link_icon_alt_text:
                spotify_link = link.get_attribute("href")
                break

        if not spotify_link:
            return ""

        with request.urlopen(spotify_link) as contents:
            return contents.url.split("/")[-1]
