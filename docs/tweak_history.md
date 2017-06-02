Tweak history of Elementary OS
1. I want to use Super+s to raise `slack` window. Use gsettings to reset the `Super+s` of windows overview [link](https://elementaryos.stackexchange.com/questions/184/how-can-i-reset-keyboard-shortcuts)
```
 $  gsettings list-recursively  | grep -i 'show-desktop'
 $  set org.gnome.desktop.wm.keybindings show-desktop ["''"]

 ```
PS: when using gsettings to set key bindings it need extra quotes and in array. eg. ["'<Alt>F8'"] 

2. add slack to custom key binding in system settings
``` wmctrl -a slack || slack```

3. Setting rotate terminator to super+t in keyboard settings:

```/home/johnnyniu/dev/projects/windows-manager/rotate.py terminator >> /home/johnnyniu/debug.txt```