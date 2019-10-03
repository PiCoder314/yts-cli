# yts-cli
> Free movies for everyone.

An unofficial CLI client for yts.am torrents.

Made by PiCoder314.

## Coming Soon
+ New Movies
+ Popular Movies
+ Filter
+ Trakt TV Authorization

## Prerequisites
+ Non Windows Environment(Windows not supported and probably never will be.)
+ Python3 or above. [Get Python](https://www.python.org/downloads/)
+ pip package manager for python. Tip you may already have it installed if you got python from above link.

## Installation
### git

```sh
sh -c "git clone https://github.com/PiCoder314/yts-cli.git"
```

### wget

```shell
sh -c "wget https://github.com/PiCoder314/yts-cli/archive/master.zip && unzip master.zip && rm master.zip"
```

### curl

```shell
sh -c "curl -fsSL https://github.com/PiCoder314/yts-cli/archive/master.zip -o master.zip && unzip master.zip && rm master.zip"
```
## Usage

```shell

chmod u+x yts.py

./yts.py --query=<search-term> <options>

-q, --query= : movie to search for.

-p, --use-proxy : use anonymous proxy.

-c, --use-cli : use aria2c to download torrent in command line.Install aria2c by <package manager> <install command> aria2.

```


## Contributing
Feel free to download the source code, open issues and open pull requests.

Recommended to use PEP8 rules for pull requests.

## Disclaimer
I am not the owner of any content, all content is provided by YTS.AM(formerly YIFY torrents).
