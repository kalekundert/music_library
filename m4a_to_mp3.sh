#!/usr/bin/env zsh

if [ $# -eq 0 ]; then
    echo "Usage: $0 <m4a ...>"
    exit 1
fi

wav=`mktemp --suffix='.wav'`
info=`mktemp --suffix='.txt'`

trap 'rm $wav $info; exit 2' SIGINT

for m4a in $*; do
    mp3="${m4a%.*}.mp3"

    # Extract track metadata from the m4a file.

    faad -i $m4a 2> $info

    # Sometimes the "title" field is spelled "tille".  What the fuck?
    title=` cat -v $info | grep -i '^ti[tl]le *: ' | sed -e 's/[Tt]i[tl]le *: //'`
    artist=`cat -v $info | grep -i '^artist *: '   | sed -e 's/[Aa]rtist *: //'`
    album=` cat -v $info | grep -i '^album *: '    | sed -e 's/[Aa]lbum *: //'`
    track=` cat -v $info | grep -i '^track *: '    | sed -e 's/[Tt]rack *: //'`
    year=`  cat -v $info | grep -i '^date *: '     | sed -e 's/[Dd]ate *: //'`

    # Convert the m4a file into an mp3 file, via a wav intermediate.

    faad -o "$wav" "$m4a"
    lame --tt "$title"      \
         --ta "$artist"     \
         --tl "$album"      \
         --tn "$track"      \
         --ty "$year"       \
         "$wav" "$mp3"

done

rm $wav $info
exit 0
