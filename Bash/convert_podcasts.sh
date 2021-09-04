#!/bin/bash

pocasts_loc="/run/user/1000/gvfs/mtp:host=SAMSUNG_SAMSUNG_Android_RF8M8399FMF/Phone/Android/data/au.com.shiftyjelly.pocketcasts/files/PocketCasts/podcasts"
walkman_loc="/media/user/AC-Y10"

get-meta-tag() {
    echo `ffprobe 2> /dev/null -show_format "$2" | grep -oP "TAG:$1=\K.+"`
}

sanitize-str() {
    echo "$1" | sed 's/[^a-zA-Z0-9 ./-]//g'
}

rm -r "$walkman_loc"/*
for file in "$pocasts_loc"/*; do
    album=`get-meta-tag album "$file"`
    if [[ "$album" == 'History Extra podcast' ]]; then
        title=`sanitize-str "$(get-meta-tag title "$file")"`
        name="$walkman_loc/2x-$album-${title}.mp3"
        if [ ! -f "$name" ]; then
            ffmpeg -i "$file" -filter:a "atempo=1.8,volume=2.5" -vn "$name"
        fi
    fi
done
