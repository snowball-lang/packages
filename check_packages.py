
import os
import json
import tomllib

has_error = False

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Iterate all packages inside "pkgs" folder
for pkg in os.listdir("pkgs"):
    print("\n=========================================\n")
    # Get package name
    pkg_name = pkg.split(".")[0]
    # Open package file
    with open("pkgs/" + pkg, "r") as pkg_file:
        # Load package data
        pkg_data = json.load(pkg_file)

        print("CHECKING " + pkg_name + "...")
        if "versions" not in pkg_data:
            print(RED + "INVALID (no verion tree)" + RESET)
            has_error = True
            continue

        versions = pkg_data["versions"]
        for version in versions:
            download_url = pkg_data["download_url"]
            print(" VERSION " + GREEN + version + RESET + ":")
            try:
                print("    DOWNLOAD: ...", end=' ')
                # clone the package into ".temp" folder
                os.system("git clone " + download_url + " .temp --quiet --depth 1 --branch " + version)
                print(GREEN + "OK" + RESET)

                # See if the package has a "sn.toml" file
                print("    PACKAGE CONFIG: ...", end=' ')
                if os.path.isfile(".temp/sn.toml"):
                    # If it does, then it's a valid package
                    print(GREEN + "OK" + RESET)

                    # Load the "sn.toml" file
                    with open(".temp/sn.toml", "r") as sn_toml_file:
                        # Load the "sn.toml" file
                        sn_toml_data = tomllib.loads(sn_toml_file.read())

                        print("    ENTRY EXISTENCE: ...", end=' ')
                        # See if the package has an entry
                        if "main" in sn_toml_data["package"]:
                            entry = sn_toml_data["package"]["main"]
                            with open(f".temp/{entry}", "r") as entry_file:
                                print(GREEN + "OK" + RESET)
                        else:
                            # If it doesn't, then it's an invalid package
                            print(RED + "INVALID" + RESET)
                            has_error = True

                        print("    DEPENDENCIES EXISTENCE: ...", end=' ')
                        # See if the package has dependencies
                        if "dependencies" in sn_toml_data:
                            dependencies = sn_toml_data["dependencies"]
                            for dependency in dependencies:
                                # only check if the dependency exists in the pkgs folder
                                if os.path.isfile(f"pkgs/{dependency}.json"):
                                    print(GREEN + "OK" + RESET)
                                else:
                                    print(RED + "INVALID" + RESET)
                                    has_error = True
                        else: print(GREEN + "OK" + RESET)
                else:
                    # If it doesn't, then it's an invalid package
                    print(RESET + "INVALID" + RESET)
                    has_error = True
                
            except Exception as e:
                print(RED + "ERROR" + RESET)
                print(e)
                has_error = True

            # Delete the ".temp" folder
            os.system("rm -rf .temp")

if has_error:
    exit(1)
