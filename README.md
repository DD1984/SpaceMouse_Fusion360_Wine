**if something does not work - pls, use development wine branch, in staging branch "ntdll-Syscall_Emulation" feature is enabled - and this feature prevent to use direct linux syscalls execution, whitch using by this dll to access to driver unix socket, but dll have workaround solution - int80h api - and it is workable in my tests on wine-9.0-rc2 (Staging)**  

This is new solution to make 3Dconnexion SpaceMouse workable in Fusion 360 in Linux under WINE (other applications may work too)  
New solution based on dll replacment and work together with open source linux driver for space mouse [spacenavd](http://spacenav.sourceforge.net/),  
[old](https://github.com/DD1984/SpaceMouse_Fusion360_Wine/tree/master/AddIns) solution - based on AddIns


#### instalation:
* **spacenavd** must be installed first from you distributive repositories 
* copy **siappdll.dll** to the folder of your program (folder where Fusion360.exe placed)
* setup **_legacy_** SpaceMouse driver in Fusion 360 *Preferences*
* **spnavcfg** could be installed - this is graphical util for fine tune space mouse parameters (this package do not exist in ubuntu repos, but you could download it from spacenavd website)

#### TODO:
* [ ] Buttons
* [ ] CPU load

#### Very Thanks:
* [SpaceNavigatorEmulator](https://github.com/lukenuttall/SpaceNavigatorEmulator)
* [wine-discord-ipc-bridge](https://github.com/0e4ef622/wine-discord-ipc-bridge)
