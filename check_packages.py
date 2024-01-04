
import os
import json
import tomllib

has_error = False

# Iterate all packages inside "pkgs" folder
for pkg in os.listdir("pkgs"):
    print("\n=========================================\n")
    # Get package name
    pkg_name = pkg.split(".")[0]
    # Open package file
    with open("pkgs/" + pkg, "r") as pkg_file:
        # Load package data
        pkg_data = json.load(pkg_file)
        
        download_url = pkg_data["download_url"]

        print("CHECKING " + pkg_name + "...")
        try:
            print(" DOWNLOAD: ...", end=' ')
            # clone the package into ".temp" folder
            os.system("git clone " + download_url + " .temp --quiet --depth 1")
            print("OK")

            # See if the package has a "sn.toml" file
            print(" PACKAGE CONFIG: ...", end=' ')
            if os.path.isfile(".temp/sn.toml"):
                # If it does, then it's a valid package
                print("OK")

                # Load the "sn.toml" file
                with open(".temp/sn.toml", "r") as sn_toml_file:
                    # Load the "sn.toml" file
                    sn_toml_data = tomllib.loads(sn_toml_file.read())

                    print(" ENTRY EXISTENCE: ...", end=' ')
                    # See if the package has an entry
                    if "main" in sn_toml_data["package"]:
                        entry = sn_toml_data["package"]["main"]
                        with open(f".temp/{entry}", "r") as entry_file:
                            print("OK")
                    else:
                        # If it doesn't, then it's an invalid package
                        print("INVALID")
                        has_error = True
            else:
                # If it doesn't, then it's an invalid package
                print("INVALID")
                has_error = True
            
        except Exception as e:
            print("ERROR")
            print(e)
            has_error = True

        # Delete the ".temp" folder
        os.system("rm -rf .temp")

if has_error:
    exit(1)
