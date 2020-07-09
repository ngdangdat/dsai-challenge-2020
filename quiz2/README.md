# Requirement
- Implement a minimal 'ls' command with support of argument '-R'

# Prerequisites
- Python 3.6.3

# Usage
```sh
python ls.py [-R] <file/folder path> ...
```

# Example
- With `-R`
```sh
python3 ls.py -R ../ ls.py 
ls.py

../:
README.md       quiz1   quiz2

..//quiz1:
README.md       file1.txt       file1.txt_file2.txt_1594223407.output.txt
file1.txt_file2.txt_1594223448.output.txt       file2.txt       write_not_duplicate.py

..//quiz2:
README.md       ls.py
```

- Without -R
```sh
python3 ls.py  ../ ls.py
ls.py

../:
README.md       quiz1   quiz2
```
