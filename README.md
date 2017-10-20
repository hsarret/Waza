# Waza
SublimeText 3 Simple Perforce plugin

## Requirements:
* p4 console tool must be available in the system's PATH

Download it here https://www.perforce.com/downloads/helix-visual-client-p4v

## What does it do:
* **CheckOut** current file
* **Mark for add** current file
* Display **Default changelist stats**

## Integration in SublimeText

### To add a section in SublimeText menu

* Use Command Palette to browse packages
* Enter *"User"* folder
* Add following content to file *"Main.sublime-menu"*
```
	{
	    "id" : "P4",
	    "caption" : "P4",
		"children":
		[
		{
			"caption" : "CheckOut",
			"command" : "p4_checkout"
		},
		{
			"caption" : "Add",
			"command" : "p4_add"
		},
		{
			"caption" : "Defaut changelist stats",
			"command" : "p4_default_changelist_stats"
		}
		]
	}
```

### To add shortcuts to commands
* Open *"Key Bindings"* from *"Preferences"* menu
* Add following content to user file
```
	{ "keys": ["ctrl+4"], "command": "p4_checkout" },
	{ "keys": ["ctrl+5"], "command": "p4_add" },
	{ "keys": ["ctrl+6"], "command": "p4_default_changelist_stats" },
```
