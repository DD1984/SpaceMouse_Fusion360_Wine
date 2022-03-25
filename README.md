This is workaround solution to make 3Dconnexion SpaceMouse workable in Fusion 360 in Linux under WINE
#### how it work:
solution consist from two part: 
* spconvd - daemon that connect to [spacenavd](http://spacenav.sourceforge.net/) (open source linux driver for spacemouse), read mouse events and then send it to Fusion 360 via network through *localhost:11111*
* AddIns (plugin) for Fusion 360, that read mouse events from spconvd and convert it to camera motions using Fusion 360 API
#### instalation:
* **spacenavd** must be installed first from you distributive repositories (this package exist in Ubuntu 21.04 repos)
* **spnavcfg** could be installed - this is graphical util for fine tune space mouse parameters (this package do not exist in ubuntu repos, but you could download it from spacenavd website)
* clone this repo, go to spconvd directory and execute: ```make && make install``` - this will build and install spconvd daemon to ```~/.local/bin/```
* run spconvd **manually**
* copy **SpaceMouse** folder into Fusion 360 AddIns path: ```~/.wine/drive_c/users/<YOU USER NAME>/Application Data/Autodesk/Autodesk Fusion 360/API/AddIns```
* start Fusion 360, go to AddIns menu and **Run** SpaceMouse - that is all
* #### TODO:
* - [ ] move mouse events shaper(it need to decrease cpu load by decrease screen refresh rate) from spconvd to AddIns
* - [ ] rewrite spconvd on python
* - [ ] fine tune coefficients of motions, rotations and zoom 
