# dnurt_integration
The python module for updating DNURT database using scopus, wos and gscholar api.
# Installation
1. Extract the archive.
2. Change database config in `dnurt_integration/dnurtdb/dbconfig.json`.
3. Open terminal and type:

    `sudo pip3 install /path/to/extracted/archive` if you want to install package for all users.
    
    `pip3 install /path/to/extracted/archive --user` if you want to install package for current user.
    
    If you have chosen second way, be sure that `$HOME/.local/bin` directory is in your **PATH** system variable.
# Run script
For running script you can simply type:
`authors_update -x` where **x** is one of the folowing parameters:
* `-s` - updates only scopus information.
* `-w` - updates only wos information. 
* `-g` - updates only gscholar information.
* `-a` - updates all.