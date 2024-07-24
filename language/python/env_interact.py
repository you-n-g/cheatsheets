import subprocess
import os

# Define the shell command as a multi-line string
shell_command = """
cat << EOF > .env
TEST_VAR=123
EOF
"""

# Execute the shell command


import fire
class Exp:
    def run(self):
        subprocess.run(shell_command, shell=True, check=True)

    def test_env(self):
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
        
if __name__ == "__main__":
    fire.Fire(Exp)
