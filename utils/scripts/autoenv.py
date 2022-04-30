from pathlib import Path

import secrets


BASE_DIR = Path(__file__).resolve().parent.parent.parent

BLUE = "\033[94m"
GREEN = "\033[92m"
END = "\033[0m"


class AutoGenEnv:
    help = "Create a .env file for storing environment variables"

    def generate(self, *args, **options):
        env_path: str = BASE_DIR / ".env"
        secret_key = secrets.token_urlsafe(16)
        lines: str = """# SECURITY WARNING: don't run with the debug turned on in production!
DEBUG={}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY={}
"""

        if not env_path.exists():
            env_path.touch()
            print(f"{BLUE}Created .env file...{END}")
            is_debug = input("Is this a local-development environment? [y/N] ")
            if is_debug == "y" or is_debug == "Y":
                is_debug = "True"
            else:
                is_debug = "False"
            lines = lines.format(is_debug, secret_key)
            with open(env_path, "w") as f:
                f.write(lines)
        else:
            if env_path.is_file():
                print(f"{BLUE}.env file already exists...{END}")
                print("Do you want to overwrite it? (y/n)")
                choice = input()
                if choice == "y" or choice == "Y":
                    env_path.unlink()
                    env_path.touch()
                    is_debug = input("Is this a local-development environment? [y/N] ")
                    if is_debug == "y" or is_debug == "Y":
                        is_debug = "True"
                    else:
                        is_debug = "False"
                    lines = lines.format(is_debug, secret_key)
                    with open(env_path, "w") as f:
                        f.write(lines)
                    print("Overwritten .env file")
                else:
                    print("Aborted...")
                    return

        print(
            "{0}Successfully created .env file with \nSECRET_KEY={1} and DEBUG={2}{3}".format(
                GREEN, secret_key, is_debug, END
            )
        )


if __name__ == "__main__":
    AutoGenEnv().generate()
