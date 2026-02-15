import sys
import os

# get the directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory of the test
parent_dir = os.path.dirname(current_dir)

# add parent directory to sys.path
sys.path.insert(0, parent_dir)
