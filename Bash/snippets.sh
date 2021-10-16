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
docker rm -f $(docker ps -a -q) # remove all containers
docker rmi -f $(docker images -a -q) # remove all images
tac # cat with reverse lines
dpkg -r $(dpkg -f <file>.deb Package) # remove package from .deb file
wc -l <file> # number of lines
grep -o -i <word> <file> | wc -l # number of word in file
# CTRL+ALT+E -  expand alias
