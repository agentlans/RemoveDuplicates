# RemoveDuplicates
Finds and deletes duplicate files from one or more directories.

It's a single-file Python 3 script.

Usage:
`python RemoveDuplicates.py directory1 directory2 ...`

where `directory1`, `directory2`, ... are directories that contain duplicate files.

Example session:
```
$ python RemoveDuplicates.py ~/Python

Scanning directory /home/user/Python...
KEEP   /home/user/Python/Markov/Dracula.txt
DELETE /home/user/Python/Markov/Mystery/Dracula.txt
KEEP   /home/user/Python/Bioinfo/Matrices/Nucleotides.csv
DELETE /home/user/Python/Bioinfo/Others/Nucleotides.csv
KEEP   /home/user/Python/Bioinfo/GeneticCode/Translation.csv
DELETE /home/user/Python/Bioinfo/Others/Translation.txt
KEEP   /home/user/Python/Dates/Schedule.py
DELETE /home/user/Python/Dates/date_helper/build/lib/date_helper/Schedule.py
DELETE /home/user/Python/Dates/date_helper/src/date_helper/Schedule.py
Continue? (yes/no) yes
WARNING: Couldn't delete /home/user/Python/Dates/date_helper/build/lib/date_helper/Schedule.py
```

# Author, License
Copyright :copyright: 2022 Alan Tseng

GNU General Public License v3
