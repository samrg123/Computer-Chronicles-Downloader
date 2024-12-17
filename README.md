# Welcome to the Computer Chronicles Downloader Repo!

**Table of contents:**
---
> 1. [About **C**omputer **C**hronicles **Downloader**](#about)  
> 2. [Getting Started](#gettingStarted)
> 3. [Things To Note](#notes)
---


<a name="about"></a>
## About **C**omputer **C**hronicles **Downloader**
**C**omputer **C**hronicles **Downloader** (CCDownloader) is a lightweight python utility used to bulk download episodes of [*The Computer Chronicles*](https://en.wikipedia.org/wiki/Computer_Chronicles) or any other files conforming to the the `files.xml` download format. 

As configured out of the box CCDownloader will download 448 unique episodes of *The Computer Chronicles* from Seasons 1 - 19. CCDownloader can also optionally output linux `ln` commands to additionally hark link 151 re-aired episodes from Seasons 1-20 to their original episode files. 

<a name="gettingStarted"></a>
## Getting Started
To use CCDownloader first clone the repo and install the required python packages:
```bash
git clone https://github.com/samrg123/Computer-Chronicles-Downloader.git
cd ./Computer-Chronicles-Downloader
pip install -r ./requirements.txt
```

Then execute the program according to your needs:
```bash
py ./CCDownloader.py --help
usage: CCDownloader.py [-h] [--dir str] [--file str] [--listAll] [--listDir] [--listDownload] [--listFile] [--listLinks] [--listRepeat] [--threads int] [--verbose int]

A lightweight python utility for downloading recorded computer chronicle episodes

options:
  -h, --help      show this help message and exit
  --dir str       Specifies the directory to download to. Default [str] = './Computer Chronicles'
  --file str      Specifies the download xml file to parse. Default [str] = './files.xml'
  --listAll       Lists all information and exits. Default = 'False'
  --listDir       Lists the files in `--dir` and exits. Default = 'False'
  --listDownload  Lists the non existing `--file` files in `--dir` that will be downloaded and exits. Default = 'False'
  --listFile      Lists the files in `--file` and exits. Default = 'False'
  --listLinks     Lists the 'REPEAT' files in `--file` as linux `ln` commands to original files and exits. Default = 'False'
  --listRepeat    Lists the 'REPEAT' files in `--file` that will be ignored and exits. Default = 'False'
  --threads int   Specifies the number of threads to use while downloading. Default [int] = '32'
  --verbose int   Specifies the verbose log level. Larger values enable more verbose output. Log Levels: {'Error': 0, 'Default': 1, 'Verbose': 2} Default [int] = '1'

```

<a name="notes"></a>
## Things to Note
- By default CCDownloader is configured to download all the files in `files.xml` who's names don't match `' REPEAT [.*].EXT'` and don't already existing in `--dir`.
- `REPEAT` files represent reruns of previously aired episodes and can be hard linked to their original aired episodes by executing the commands output from `py CCDownloader.py --listLinks`
    > Note: Season 20 only consists of reruns and doesn't contain any unique files. As a result the 'Season 20' folder isn't created by default and should be manually created in the `--dir` folder before running the link commands.
- There are currently 100 mssing (33 unique) episodes that can be found in `missing.xml`. Feel free to reach out to me with a download link to any of the missing episodes and so I can add them to `files.xml`  
- Currently all of the episodes in `files.xml` are in english* and cherry picked between versions for best quality. A list of episodes with mulitple versions can be found in `multiversion.txt`.
    > *Season 12 Episode 20 is in English, but has hardcoded arabic subtitles. A strictly english version is also tracked in `missing.xml`.  
    > *Season 15 Episode 02 has partial missing audio. A better copy of the episode is also tracked in `missing.xml`.  
    > *Season 19 Episode 20 has English audio on a second track and the video is partially corrupt. A better copy of the episode is also tracked in `missing.xml`.  
    > *I admittedly haven't watched all 400+ episodes, so if you stumble across an episode that isn't in english or of 'good' quality let me know and I'll update `missing.xml` to include it.
- All download links are sourced from various [Internet Archive](https://archive.org/) uploads. If you enjoy using CCDownloader consider making a donation to them [here](https://archive.org/donate?origin=iawww-TopNavDonateButton)  