# dnurt_integration
The python module for updating DNURT database using scopus, wos and gscholar api.
# Installation

`sudo pip3 install /path/to/archive` if you want to install package for all users.

`pip3 install /path/to/archive --user` if you want to install package for current user.

If you have chosen second way, be sure that `$HOME/.local/bin` directory is in your **PATH** system variable.
# Run script
For running script you can simply type:
`authors_update`

If u need to do some configuration run:

`authors_update` -x where **x** is one of the folowing parameters:
* `-cb` - change database configuration.
* `-cw` - change browser binary path. 
* `-cs` - change scopus apikey.
