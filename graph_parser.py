import re

from functools import cached_property
from typing import NamedTuple

# expression to capture a Bible reference that corresponds to a range of verses
RANGE_REGEX: re.Pattern = re.compile("^(.*?)(?:-([^-]*))?$")


class BibleVerse(NamedTuple):
    """This class stores the information corresponding to a Bible verse (book, chapter, verse)
    and provides a utility method, `from_osis`, that allows parsing from OSIS format.

    """

    book: str
    chapter: int
    verse: str

    @classmethod
    def _parse_ref(cls, ref: str) -> "BibleVerse":
        components: list[str] = ref.split(".")
        if len(components) == 3:
            book, raw_chapter, raw_verse = components
            return BibleVerse(book, int(raw_chapter), int(raw_verse))
        raise ValueError(f"Malformed input: {ref}")

    @classmethod
    def _populate_range(
        cls, start_verse: "BibleVerse", end_verse: "BibleVerse"
    ) -> list["BibleVerse"]:
        assert (
            start_verse.book == end_verse.book
        ), f"verses in a range must be in the same book: {start_verse} - {end_verse}"
        assert (
            start_verse.chapter == end_verse.chapter
        ), f"verse ranges that span chapters are currently not supported: {start_verse} - {end_verse}"
        book, chapter, _ = start_verse
        verses = []
        for verse_num in range(start_verse.verse, end_verse.verse):
            verses.append(BibleVerse(book, chapter, verse_num))
        verses.append(end_verse)
        return verses

    @classmethod
    def from_raw(cls, raw: str) -> list["BibleVerse"]:
        if match := RANGE_REGEX.match(raw):
            first_parsed = cls._parse_ref(match[1])
            if second := match[2]:
                second_parsed = cls._parse_ref(second)
                return cls._populate_range(first_parsed, second_parsed)
            return [first_parsed]
        raise ValueError(f"Invalid input to convert from raw: {raw}")

    @cached_property
    def osis(self):
        """Retrieve the OSIS ID of this verse."""
        return f"{self.book}.{self.chapter}.{self.verse}"


VersePair = frozenset[BibleVerse]


class BibleGraph:
    """Numerically stores bible verses as nodes and references as edges."""
    def __init__(self):
        self._lowest_unused_index = 0
        self.verses_to_index: dict[BibleVerse, int] = {}
        self.index_to_verses: list[BibleVerse] = []
        self.references = []

    @classmethod 
    def from_weights(cls, weights: dict[VersePair, int]):
        bibleGraph = cls()
        for versePair in weights.keys():
            verses = list(versePair)
            if len(verses) != 2:
                print("WARNING: Found weights key with len != 2: ", verses)
                continue
            bibleGraph.add_edge(verses[0], verses[1])
        return bibleGraph
    
    def add_edge(self, from_verse, to_verse):
        self.references.append((self._verse_to_index(from_verse), self._verse_to_index(to_verse)))
    
    def _verse_to_index(self, verse):
        index = self.verses_to_index.get(verse)
        if index is None:
            index = self._lowest_unused_index 
            self._lowest_unused_index += 1
            self.verses_to_index[verse] = index 
            self.index_to_verses.append(verse)
        return index


def load_source_file(location: str) -> dict[VersePair, int]:
    """Load the dataset and return a dictionary that maps a pair of Bible verses to an integer
    corresponding to the edge weight. Note that verse pairs should be frozensets because edges
    are undirected.

    """
    with open(location) as file:
        header = next(file)
        whitespace = re.compile(r"\s")
        weights: dict[VersePair, int] = {}
        for line in map(str.strip, file):
            components = whitespace.split(line)
            if len(components) == 3:
                raw_from, raw_tos, raw_weight = components

                # attempt to parse data
                try:
                    from_verses, to_verses = map(
                        BibleVerse.from_raw, [raw_from, raw_tos]
                    )
                except AssertionError as ae:
                    continue
                weight = int(raw_weight)

                # create edges
                for from_verse in from_verses:
                    for to_verse in to_verses:
                        weights[frozenset((from_verse, to_verse))] = weight
        return weights


if __name__ == "__main__":
    weights = load_source_file("cross_references.txt")
    bibleGraph = BibleGraph.from_weights(weights)

    print("Number of unique verses in biblegraph: ", bibleGraph._lowest_unused_index)
    print("Edge samples: ", bibleGraph.references[:10])
    print("Node dict: ", list(bibleGraph.verses)[:10])