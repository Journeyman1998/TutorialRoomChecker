# Tutorial Room Checker
This application checks the availability of tutorial rooms.

## Usage
First, install the dependencies. I am using conda, but pip will do just fine. The program uses several built-in modules, such as json, request, os and datetime. Only BeautifulSoup needs to be installed.
```cmd
conda install bs4
```
Next, just run the main program.
```cmd
cd TutorialRoomChecker
python main.py
```
The program will take a few seconds to download and initialize the lookup dictionary. Subsequent runs will be instantaneous.

## To do
- [ ] Organize the locations into different regions, so that only the nearest ones are provided as valid results. We don't want students to walk for 1km just for a tutorial room (Priority: High)
- [ ] Incorporate a UI, possibly using Electron or web-based, e.g. Django (Priority: Medium)
- [ ] Several indices have remarks, which are ignored when checking for tutorial rooms. For example, some tutorials are only held at specific weeks. (Priority: Low)

