# Login-moodle-script
This python script allows one to enter the username and password and the script will login to there moodle and check there grade for a given course ID
## How it works
this simple script copys the table where the grades are kept and stores that in a text file. The next time it is run it looks for change and if any is detected it alearts the user via slack. This script is ment to be run periodictly. (for example I have it running every 30 minutes)
