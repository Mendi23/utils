#!/bin/bash

pocasts_loc="/run/user/1000/gvfs/mtp:host=SAMSUNG_SAMSUNG_Android_RF8M8399FMF/Phone/Android/data/au.com.shiftyjelly.pocketcasts/files/PocketCasts/podcasts"
walkman_loc="/media/user/AC-Y10"

get-meta-tag() {
    echo `ffprobe 2> /dev/null -show_format "$2" | grep -oP "TAG:$1=\K.+"`
}

sanitize-str() {
    echo "$1" | sed 's/[^a-zA-Z0-9 ./-]//g'
    # echo "$1" | sed "s/[^[:alnum:]-]//g"
}

rm -r "$walkman_loc"/*
for file in "$pocasts_loc"/*; do
    album=`get-meta-tag album "$file"`
    if [[ "$album" == 'History Extra podcast' || "$album" == "Dan Carlin's Hardcore History: Addendum" ]]; then
        title=`sanitize-str "2x-$album-$(get-meta-tag title "$file").mp3"`
        name="$walkman_loc/$title"
        if [ ! -f "$name" ]; then
            ffmpeg -i "$file" -filter:a "atempo=2.1,volume=2.5" -vn "$name"
        fi
    fi
done
