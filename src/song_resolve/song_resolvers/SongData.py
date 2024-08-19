from dataclasses import dataclass
from typing import Optional


@dataclass
class SongData:
    title: str
    artist: str
    time: str
    original_file: str
    accuracy: Optional[float] = None
    description: Optional[str] = ""
    track_id: Optional[str] = ""

    def __eq__(self, other):
        return self.title == other.title and self.artist == other.artist

    def __hash__(self):
        return hash((self.title, self.artist))
