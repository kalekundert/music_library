#!/usr/bin/env python3

"""\
Rename songs such that their paths contain only alphanumeric characters and 
underscores.

Usage:
    rename_songs.py <dir>... [-d]

Options:
    -d --dry-run
        Show how any files would be renamed, but don't actually do anything.
"""

from add_to_library import *

def rename_song(src_path, dry_run=False):
    artist, title = names_from_song(src_path)
    dest_path = src_path.parent / (title + src_path.suffix)

    if not dry_run:
        src_path.rename(dest_path)
    else:
        #print(src_path)
        print('  →', dest_path)


def main():
    args = docopt.docopt(__doc__)
    paths = []
    num_songs_added = 0

    for dir in args['<dir>']:
        for path in find_mp3_files(dir):
            rename_song(path, args['--dry-run'])

if __name__ == '__main__':
    main()

