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

# For testing 2 files.
cat << EOF > ./.new.env
TEST_VAR_2=123
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

    def test_env_raw(self):

        """
        .. code-block:: python

            python language/python/env_interact.py run
            dotenv run -- python language/python/env_interact.py test_env_raw
            TEST_VAR=321 dotenv run --no-override -- python language/python/env_interact.py test_env_raw

        """
        print(os.environ["TEST_VAR"])

    def test_2_env_file(self):
        """

        .. code-block:: python

            python language/python/env_interact.py run
            dotenv -f language/python/.env run -- python language/python/env_interact.py test_2_env_file
            dotenv -f language/python/.env -f language/python/.new.env run -- python language/python/env_interact.py test_2_env_file

        conclusion: dotenv can't support multiple files.
        """
        print(os.environ.get("TEST_VAR"))
        print(os.environ.get("TEST_VAR_2"))


if __name__ == "__main__":
    fire.Fire(Exp)
