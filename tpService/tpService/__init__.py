import os
import sys
from pathlib import Path
import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.extend(
    [
        # root_dir,
        os.path.join(root_dir, 'tpRunner')
    ]
)