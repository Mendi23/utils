#!/bin/bash

get-epub-meta() {
    if [ $# -lt 2 ]
    then
       echo
       echo "Usage: minfo <meta-type> <epub-file>"
       echo
    else
       fileloc=`unzip -l "$2" | grep -Po '\b[^\s-]*\.opf\b'`
       metafound=`zipgrep '<dc:'$1'.*>(.*)</dc:'$1'>' -m1 "$2" $fileloc`
       echo `expr "$metafound" : '.*<dc:'$1'.*>\(.*\)</dc:'$1'>.*'`
    fi
}

split-str() {
    IFS=',' read -ra arr <<< "$@"
    for i in "${arr[@]}"; do
        echo "${i%;}" | xargs -0
    done
}

get-file-title() {
    title=$(get-epub-meta title "$1")
    creator=`split-str $(get-epub-meta creator "$1") | tac`
    [[ ! -z "$creator" ]] && [[ ! -z "$title" ]] && echo $creator - $title || echo ""
}

for file in "$1"/*.epub; do
    info="$(get-file-title "$file" | sed 's/\///g')"
    [[ ! -z "$info" ]] && mv -n "$file" "$1/$info.epub"
done;
