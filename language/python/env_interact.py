import subprocess
import os

# Define the shell command as a multi-line string
shell_command = """
mkdir -p test_subdir/

cat << EOF > test_subdir/.env
TEST_VAR=123
EOF

cat << EOF > test_subdir/load.py
from dotenv import load_dotenv
load_dotenv()
EOF

# for testing `test_launch_json`
# run dG and add arguments
cat << EOF > ./.env
TEST_VAR=123
EOF
"""

# Execute the shell command
from pathlib import Path
DIRNAME = Path(__file__).absolute().resolve().parent

import fire
class Exp:
    def run(self):
        subprocess.run(shell_command, shell=True, check=True, cwd=DIRNAME)

    def test_env(self):
        """
        It will work under normal python script.

        .. code-block:: python

            python language/python/env_interact.py run && python language/python/env_interact.py test_env


        But it will not work under interactive REPL

        .. code-block:: shell

            cd language/python && python env_interact.py run && python -c "from env_interact import *; Exp().test_env()"

        """
        import sys
        sys.path.insert(0, str(DIRNAME))
        import test_subdir.load
        # NOTE:
        # If you only source the variables
        # - It will fail;
        #
        # You have to use following methods to make it works
        # 1) source the env
        #   if [ -f .env ]; then
        #     # Export each variable in the .env file
        #     export $(grep -v '^#' .env | xargs)
        #   fi
        # 2) use dotenv
        #   dotenv run -- python app.py
        print(os.environ["TEST_VAR"])

    def test_launch_json(self):
        print(os.environ["TEST_VAR"])
        print("end")
        
if __name__ == "__main__":
    fire.Fire(Exp)
