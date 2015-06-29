# Commandline tools for ROOT files inspection and automated plotting

These are several ROOT commandline tools which have the goal to inspect
and to act on root file contents directly from a unix terminal.

At this time, there are:

    o rools:    Print the content of a root file or subdirectory (like ls)
                -l option exists (like with ls) and give access to class,
                datime, name and title of an object

    o roocp:    Copy an object from a root file to another

    o roorm:    Remove an object from a root file
                -f option exists to force the removing

    o roomv:    Move an object from a root file to another

    o roomkdir: Create a directory in a root file

    o rooprint: Put histograms and graphs in pdf file
		-o option exists and allows to put all the histograms
		and graphs in the same pdf file

Let's be pragmatic, here are some examples:

About rools:

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

Which is really usefull with these commandlines is that they accept regular expressions:

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

About roocp:

> roocp file2.root:graph1 file.root
> rools *.root
/dir/dir/dir/file.root :
dir1   dir2   graph1 hist1  hist2

/dir/dir/dir/file2.root :
graph1 graph2


About roorm:

> roorm file.root:hist1
Are you sure to remove 'hist1' from '/dir/dir/dir/file.root' ? (y/n) : y
> rools file.root
dir1  dir2  hist2

or:

> roorm	-f file.root:graph1
> rools	file.root
dir1  dir2  hist2

About roomv:

> roomv file2.root:graph1 file.root
> rools *.root
/dir/dir/dir/file.root :
dir1   dir2   graph1 hist1  hist2

/dir/dir/dir/file2.root :
graph2

About roomkdir:

> roomkdir file.root:new_dir
> rools file.root
dir1    dir2    hist1   hist2   new_dir
