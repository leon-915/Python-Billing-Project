#!"e:\work\task\tmp\new folder\billing_coding_challenge\env\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'coverage==4.5.3','console_scripts','coverage-3.8'
__requires__ = 'coverage==4.5.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('coverage==4.5.3', 'console_scripts', 'coverage-3.8')()
    )
