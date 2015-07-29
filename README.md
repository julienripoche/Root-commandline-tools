# Commandline tools for ROOT files inspection and automated plotting

These are several ROOT commandline tools which have the goal to inspect
and to act on root file contents directly from a unix terminal.

## Short description

    o rools:      Print the content of a root file or subdirectory (like ls)
                  -l option exists (like with ls) and give access to class,
                  datime, name and title of an object

    o roocp:      Copy objects from ROOT files into an other

    o roorm:      Remove objects from ROOT files
                  -f option exists to force the removing

    o roomv:      Move objects from ROOT files to an other

    o roomkdir:   Add directories in a ROOT files

    o rooprint:   Print ROOT files contents on ps,pdf or png,gif.. files

    o rooeventselector : Copy subsets of trees from source ROOT files
                         to new trees on a destination ROOT file

    o roobrowse : Open a ROOT file on a TBrowser

## Some examples

### rools

> rools file.root

dir1  dir2  hist1 hist2

> rools file.root -l

TDirectoryFile  Jun 26 11:23  dir1   "a directory"  
TDirectoryFile  Jun 26 11:23  dir2   "another directory"  
TH1F            Jun 26 11:23  hist1  "This is the px distribution"  
TH2F            Jun 26 11:23  hist2  "py vs px"

> rools -h

usage: rools [-h] [-l] pattern_list [pattern_list ...]

list ROOT file contents

positional arguments:  
  pattern_list  file path and object path in the ROOT file with the syntax :  
                [file_path/]file.root:[object_path/]object

optional arguments:  
  -h, --help    show this help message and exit  
  -l            use a long listing format

> rools file.root:hist1

hist1

> rools file.root:dir1

hist3 hist4

Which is really usefull with these commandlines is that they accept regular expressions.

> rools file.root:hist*

hist1 hist2

> rools file.root:dir*

dir1 :  
hist3 hist4

dir2 :  
hist5 hist6

> rools *.root

/dir/dir/dir/file.root :  
dir1  dir2  hist1 hist2

/dir/dir/dir/file2.root :  
graph1 graph2

> rools \*.root:\*

/dir/dir/dir/file.root :  
hist1 hist2

dir1 :  
hist3 hist4

dir2 :  
hist5 hist6

/dir/dir/dir/file2.root :  
graph1 graph2

### roocp

> roocp file2.root:graph1 file.root  
> rools *.root

/dir/dir/dir/file.root :  
dir1   dir2   graph1 hist1  hist2

/dir/dir/dir/file2.root :  
graph1 graph2


### roorm

> roorm file.root:hist1

Are you sure to remove 'hist1' from '/dir/dir/dir/file.root' ? (y/n) : y
> rools file.root

dir1  dir2  hist2

or:

> roorm	-f file.root:graph1  
> rools	file.root

dir1  dir2  hist2

### roomv

> roomv file2.root:graph1 file.root  
> rools *.root

/dir/dir/dir/file.root :  
dir1   dir2   graph1 hist1  hist2

/dir/dir/dir/file2.root :  
graph2

### roomkdir

> roomkdir file.root:new_dir  
> rools file.root

dir1    dir2    hist1   hist2   new_dir
