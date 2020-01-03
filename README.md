epp - easy python packaging  
I wrote it mostly because I got tired of creating  
a git repo, a .gitignore file, a setup.py file and all that shit  
every time.  
And that should explain what this code does..  

installation:  
`pip install .`  
then  
`epp --help`  
to see your options  


```
$ epp --help

usage: epp [-h] {new,go,requ} ...

positional arguments:
  {new,go,requ}
    new          Initialize a new project in the current directory
    go           Open a shell in the project's virtual environment
    requ         Update the package's requirements in the setup.py script

optional arguments:
  -h, --help     show this help message and exit
```

This should support both python 2 and 3. currently the script uses the 'virtualenv' version that's in the path.
