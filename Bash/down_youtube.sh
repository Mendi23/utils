#!/bin/bash

# sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl
# sudo chmod a+rx /usr/local/bin/youtube-dl
# --write-description
down-yt() {
    # usage: down-yt single|playlist|channel audio|video|subs|sub-vid [OPTIONS] URL [URL...]
    # use youtube-dl --help to see more OPTIONS

    params=("-i" "--restrict-filenames")
    if [[ "$1" == 'single' ]]; then
      params+=("--no-playlist" "-o" "'%(title)s.%(ext)s'")
    elif [[ "$1" == 'playlist' ]]; then
      params+=("--yes-playlist", "-o" "'%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'")
    elif [[ "$1" == 'channel' ]]; then
      params+=("-o" "'%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'")
    else
      echo "ERROR: unknown target"
      return
    fi

    if [[ "$2" == 'audio' ]]; then
      params+=("-x" "--audio-format" "mp3" "--audio-quality" "0" "--embed-thumbnail")
    elif [[ "$2" == 'video' ]]; then
      params+=("--add-metadata" "-f bestvideo+bestaudio/best")
    elif [[ "$2" == 'subs' ]]; then
      params+=("--write-auto-sub" "--sub-lang" "en,iw" "--skip-download" "--convert-subs" "srt")
    elif [[ "$2" == 'sub-vid' ]]; then
      params+=("--add-metadata" "--write-auto-sub" "--sub-lang" "en,iw" "--embed-subs")
    else
      echo "ERROR: unknown type"
      return
    fi
    params+=("${@:3}")
    youtube-dl "${params[@]}"
}
down-yt single video https://www.youtube.com/watch?v=I3ty8X9ozX4
# down-yt channel video --write-description --playlist-items 137,186,270-332 -f 'bestvideo[height>=720]+bestaudio/best' https://www.youtube.com/c/KingsandGenerals 
# --ffmpeg-location LOC
  # Playlist Selection:
    # --playlist-start NUMBER          Playlist video to start at (default is 1)
    # --playlist-end NUMBER            Playlist video to end at (default is last)
    # --playlist-items ITEM_SPEC       Playlist video items to download. Specify indices of the videos in the playlist separated
    #                                  by commas like: "--playlist-items 1,2,5,8" if you want to download videos indexed 1, 2, 5,
    #                                  8 in the playlist. You can specify range: "--playlist-items 1-3,7,10-13", it will download
    #                                  the videos at index 1, 2, 3, 7, 10, 11, 12 and 13.
    # --match-title REGEX              Download only matching titles (regex or caseless sub-string)
    # --reject-title REGEX             Skip download for matching titles (regex or caseless sub-string)

  # Filesystem Options:
    # -a, --batch-file FILE            File containing URLs to download ('-' for stdin), one URL per line. Lines starting with
    #                                  '#', ';' or ']' are considered as comments and ignored.
    # --autonumber-start NUMBER        Specify the start value for %(autonumber)s (default is 1)
    # -w, --no-overwrites              Do not overwrite files
    # --write-description              Write video description to a .description file
    # --write-info-json                Write video metadata to a .info.json file
    # --write-annotations              Write video annotations to a .annotations.xml file
    # --load-info-json FILE            JSON file containing the video information (created with the "--write-info-json" option)

  # Thumbnail images:
  #   --write-thumbnail                Write thumbnail image to disk
  #   --write-all-thumbnails           Write all thumbnail image formats to disk
  #   --list-thumbnails                Simulate and list all available thumbnail formats

  # Verbosity / Simulation Options:
  #   -q, --quiet                      Activate quiet mode
  #   --no-warnings                    Ignore warnings
  #   -v, --verbose                    Print various debugging information
  #   --no-call-home                   Do NOT contact the youtube-dl server for debugging
  #   -s, --simulate                   Do not download the video and do not write anything to disk
  #   --skip-download                  Do not download the video

  # Workarounds:
  #   --sleep-interval SECONDS         Number of seconds to sleep before each download when used alone or a lower bound of a
  #                                    range for randomized sleep before each download (minimum possible number of seconds to
  #                                    sleep) when used along with --max-sleep-interval.
  #   --max-sleep-interval SECONDS     Upper bound of a range for randomized sleep before each download (maximum possible number
  #                                    of seconds to sleep). Must only be used along with --min-sleep-interval.

  # Subtitle Options:
  #   --write-sub                      Write subtitle file
  #   --write-auto-sub                 Write automatically generated subtitle file (YouTube only)
  #   --all-subs                       Download all the available subtitles of the video
  #   --list-subs                      List all available subtitles for the video
  #   --sub-format FORMAT              Subtitle format, accepts formats preference, for example: "srt" or "ass/srt/best"
  #   --sub-lang LANGS                 Languages of the subtitles to download (optional) separated by commas, use --list-subs for
  #                                    available language tags

  # Authentication Options:
  #   -u, --username USERNAME          Login with this account ID
  #   -p, --password PASSWORD          Account password. If this option is left out, youtube-dl will ask interactively.
  #   --video-password PASSWORD        Video password (vimeo, smotri, youku)


  # Post-processing Options:
  #   --embed-subs                     Embed subtitles in the video (only for mp4, webm and mkv videos)
  #   --add-metadata                   Write metadata to the video file
  #   --metadata-from-title FORMAT     Parse additional metadata like song title / artist from the video title. The format syntax
  #                                    is the same as --output. Regular expression with named capture groups may also be used.
  #                                    The parsed parameters replace existing values. Example: --metadata-from-title "%(artist)s
  #                                    - %(title)s" matches a title like "Coldplay - Paradise". Example (regex): --metadata-from-
  #                                    title "(?P<artist>.+?) - (?P<title>.+)"
  #   --ffmpeg-location PATH           Location of the ffmpeg/avconv binary; either the path to the binary or its containing
  #                                    directory.
  #   --exec CMD                       Execute a command on the file after downloading and post-processing, similar to find's
  #                                    -exec syntax. Example: --exec 'adb push {} /sdcard/Music/ && rm {}'
  #   --convert-subs FORMAT            Convert the subtitles to other format (currently supported: srt|ass|vtt|lrc)
