# Photography Script

This tool generates the static page for photos.daemo.nz

## Flags
### --verbose, -v
Prints data on what the script is doing

### --version
Prints version number of script. The index.html page also states the version in the footer.

# index.css
This is the formatting for the index page of the site.

# photos.css
Similar format to index.css, but includes a tool to prevent right-click->Download.

# prepare.sh
This script is in the early stages and requires more fleshing out. However, it's basic idea is to move files off the SD card and into a Pictures directory with the date from which the script is run. For example, if I ran the script on March 7th, 2021, it creates the directory 2021-03-07. 
