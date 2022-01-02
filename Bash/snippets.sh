grep -Eoi pattern file # get strings matching patterns (-E: --extended-regexp, -o: --only-matching, -i: --ignore-case)
$(cmd) # cmd result as variable
for var in "$@" # iterate arguments. can also use: for i;
bs=8; for ((i=0; i<=$#; i+=bs)); do echo "${@:i:bs}"; done # iterating over batches of the arguments. for array, replace `$#`` with `${#s[@]}` and `@` with `s[@]`
read -a s <<< "$@" # arguments into array
grep -Eoi '<A [^>]+>' file | grep -Eoi 'HREF="[^\"]+"' |  grep -Eo '(http|https)://[^"]+') # get links from html file
rsync -avh <source> <dst> # merge folders 
man -K <keyword> # search in man pages for keyword
pip uninstall -y -r <(pip freeze) # reset all pip packages
find -name <regex-like>
pkill -f <my_pattern> # kill proccess with partial name
ffmpeg -i '<input>' -filter:a "atempo=2.0" -vn 'output' # change audio speed. limited to using values between 0.5 and 2.0, for more: "atempo=2.0,atempo=2.0"
if compgen -G <pattern> > /dev/null; then ... done; # check file existence with wildcards!
command1 > everything.txt 2>&1 # redirect both stdout and stderr
sudo ss -tulpn | grep LISTEN # check open ports
tac # cat with reverse lines
dpkg -r $(dpkg -f <file>.deb Package) # remove package from .deb file
wc -l <file> # number of lines
grep -o -i <word> <file> | wc -l # number of word in file
ls -l --block-size=M # show size in Mb
ex 2>&1 | tee output.log # output to file and stdout
screen [-r | -ls] # preform long task in the background. ctrl+a,d to detach
find <path> -type f | wc -l # number of files in path
du -sh <path> # size of directory
kill -9 $(lsof -t -i:8000) # kill process running on port 8000
find . -maxdepth 2 -mindepth 2 -name "*" | xargs -I% basename % | sort -u # find all unique ././*/...
rsync -arzh /backup/../ this/folder # resumable copy (among other)
IFS=','; arrIN=($IN); unset IFS; # arrIN=IN.split(',')
echo "${FILE##*/}" # echo just basename
echo "$1" | tr '[:upper:]' '[:lower:]' # to lower case
echo "$1" | sed "s/[^a-zA-Zא-ת0-9 ./-]//g" # remove chars
echo "$1" | sed 's/[^[:alnum:]]//g' # only keep alphanumeric
[[ ! -z "$name" ]] && filename="$name" || filename="default" # trinary operator
[[ ! -z "$info" ]] && mv "$file" "$file.epub" # if; then...
mv -n # move wothout overwrite
# CTRL+ALT+E -  expand alias

# --github
find . -size +100M | cat >> .git/info/exclude # don't commit files > 100Mb
git reset --[soft|hard] HEAD~[n] # revert last n local commits with(/out) changing local files 

# --docker
docker build -t <image_name> . # build image in current dir (containing Dockerfile)
docker run --name <container_name> -p <container_port>:<host_port> <image_name>
docker ps [-a] # list all [running] containers 
docker rm -f $(docker ps -a -q) # remove all containers
docker rmi -f $(docker images -a -q) # remove all images
docker exec -it <container_name> /bin/bash # get shell in container
