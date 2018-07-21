#!/usr/bin/env python3

"""\
Add new music files to my library.

Usage:
    add_to_library.py <dir>... [-f | -b]

Options:
    -f --force
        Overwrite existing files.

    -b --backref
        If a song already exists in the library, replace it with a hard-link to 
        the version in the library.
"""

# TODO:
# 1. Automatically convert any m4a files I find.

import os, re, logging, docopt, nonstdlib
from mutagen.id3 import ID3
from pathlib import Path
from nonstdlib import plural, name_from_title

LIBRARY = Path(__file__).parent / 'library'
KNOWN_ARTISTS = {
        'dolly_parton',
        'gary_jules',
        'benny_goodman',
        'libera',
        'macklemore',
        'willie_nelson',
        'joe_strummer',
}

def find_mp3_files(dir):
    dir = Path(dir)
    for path in dir.glob('**/*.mp3'):
        yield path

def clean_artist(artist):

    artist = name_from_title(artist)
    
    # Next make an effort to remove "featured" artists, since they mess up the 
    # intended organization.  First, consult a list of known artists and 
    # shorten anything that matches.  Second, look for "_feat_" or "_with_" 
    # and, if found, remove anything after it.

    for known_artist in KNOWN_ARTISTS:
        if artist.startswith(known_artist):
            artist = known_artist
            break

    feat = re.match(r'(.*)_(feat|with)_(.*)', artist)
    if feat:
        artist = feat.group(1)

    return artist

def clean_title(title):
    return name_from_title(title)

def names_from_song(path):
    try:
        audio = ID3(path)
        artist = audio['TPE1'].text[0]
        title = audio['TIT2'].text[0]
    except:
        raise ValueError

    return clean_artist(artist), clean_title(title)

def add_song_to_library(src_path, lib_dir, force=False, backref=False):
    try:
        artist, title = names_from_song(src_path)
    except:
        print(f"Failed to read tags from '{src_path}'")
        return 0

    dest_path = LIBRARY / artist / (title + src_path.suffix)

    if dest_path.exists():
        if force:
            dest_path.unlink()
        elif backref:
            src_path.unlink()
            os.link(dest_path, src_path)
            return 0
        else:
            return 0

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    os.link(src_path, dest_path)
    return 1

def main():
    args = docopt.docopt(__doc__)
    paths = []
    num_songs_added = 0

    for dir in args['<dir>']:
        paths.extend(find_mp3_files(dir))

    for i, path in enumerate(paths, 1):
        nonstdlib.progress(i, len(paths))
        num_songs_added += add_song_to_library(
                path, LIBRARY, args['--force'], args['--backref'])

    print(f"\rAdded {plural(num_songs_added):? song/s}.")

if __name__ == '__main__':
    main()
