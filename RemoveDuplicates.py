# Copyright 2022 Alan Tseng
#
# This program is free software: you can redistribute it 
# and/or modify it under the terms of the GNU General Public 
# License as published by the Free Software Foundation, 
# either version 3 of the License, or (at your option) any 
# later version.
# 
# This program is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more 
# details.
# 
# You should have received a copy of the GNU General Public 
# License along with this program. If not, see 
# <https://www.gnu.org/licenses/>. 

import sys
import os
from os.path import join
from pathlib import Path

import hashlib

def list_diff(lst1, lst2):
  '''Returns difference of two lists as a list.'''
  return list(set(lst1).difference(set(lst2)))

def try_remove(lst, x):
  try:
    lst.remove(x)
  except:
    pass

def files_in(path, excluded=[]):
  '''Yields the files that are in the path.'''
  for root, dirs, files in os.walk(path):
    #dirs = list_diff(dirs, excluded)
    #files = list_diff(files, excluded)
    for x in excluded:
      try_remove(dirs, x)
      try_remove(files, x)
    for name in files:
      yield join(root, name)

def dict_append(d, key, val):
  if key in d:
    d[key] += [val]
  else:
    d[key] = [val]

def file_hash(filename):
  '''Returns the SHA256 hash of the file.'''
  h = hashlib.new('sha256')
  with open(filename, "rb") as f:
    while True:
      piece = f.read(4096)
      if piece == b'':
        break
      else:
        h.update(piece)
  return h.digest()

def add_index(h, directory, excluded=[]):
  '''Adds the files in the directory 
and its subdirectories to the index.'''
  for f in files_in(directory, excluded):
    try:
      dict_append(h, file_hash(f), f)
    except OSError:
      pass
  return h

def is_symlink(f):
  return Path(f).is_symlink()

def is_low_priority(filename):
  '''Returns True if file is judged to be low priority based on filename.'''
  f = filename.lower()
  for keyw in ['copy', 'backup', 'temp', '~']:
    if keyw in f:
      return True
  return False

def partition(lst, fun):
  '''Splits list into two parts depending on whether predicate is true.'''
  return [x for x in lst if fun(x)], [x for x in lst if not fun(x)]

def sort_files(files):
  '''Put high priority files in front of backups and temporary files.'''
  links, non_links = partition(files, is_symlink)
  low, high = partition(non_links, is_low_priority)
  return sorted(high) + sorted(low) + sorted(links)

def sort_index(ht):
  '''Orders the files for each index.'''
  for k, v in ht.items():
    ht[k] = sort_files(v)

def print_operations(ht):
  '''Prints the operations that will be performed for
  the files with the same hash digest.'''
  for k, v in ht.items():
    if len(v) > 1:
      print("KEEP   {}".format(v[0]))
      for file_copy in v[1:]:
        print("DELETE {}".format(file_copy))

def do_operations(ht):
  '''Removes duplicate files. ht must be sorted first.'''
  for k, v in ht.items():
    for f in v[1:]:
      try:
        os.remove(f)
      except: # couldn't find file or don't have permission
        print("WARNING: Couldn't delete {}".format(f))

# Main entry point for the program
if __name__ == "__main__":
  ht = dict()
  for directory in sys.argv[1:]:
    print("Scanning directory " + directory + "...")
    add_index(ht, directory, excluded=['.git'])
  if len(ht) == 0:
    print("Usage: python RemoveDuplicates.py dir1 [dir2 ...]")
    sys.exit("No actions to perform.")
  sort_index(ht)
  print_operations(ht)
  while True:
    choice = input("Continue? (yes/no) ")
    if choice == 'no':
      sys.exit("Cancelled by user.")
    elif choice == 'yes':
      # Do operations
      do_operations(ht)
      sys.exit(0)
    else:
      print("Sorry, please re-enter.")
