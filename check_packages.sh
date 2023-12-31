sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get purge python3 -y --auto-remove
sudo apt-get install python3.11 -y

# git disable advice.detachedHead
git config --global advice.detachedHead false

python3.11 -m pip install --upgrade pip
python3.11 check_packages.py
