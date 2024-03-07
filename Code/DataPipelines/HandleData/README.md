# DataBase Preparation

Description of your project, what it does, and any other relevant information about what your project accomplishes or its intended use.

## C++ Part
## Requirements

- **C++ Compiler**: A modern C++ compiler capable of C++17 (e.g., GCC 7+, Clang 5+, MSVC 19.14+).
- **CMake**: Version 3.5 or higher.
- **LLVM & Clang**: This project depends on LLVM and Clang libraries. Ensure you have them installed on your system. The project has been tested with LLVM version 14.x.x and 12.x.x (specify the version you tested with).

## Installation

### Step 1: Install LLVM and Clang

You need to have LLVM and Clang installed on your system. Here are the general steps to install LLVM and Clang:

#### On Ubuntu/Debian-based systems:

sudo apt-get update
sudo apt-get install llvm clang


#### On MacOS:
you can use Homebrew:

... Note: Ensure that the LLVM binaries are in your system's PATH. You might need to add them manually if you're using Homebrew on macOS.
brew install llvm


#### On Windows:
Windows users can download pre-built binaries from the [LLVM Download Page](https://releases.llvm.org/download.html).


#### Building the project :

mkdir build && cd build
cmake ..
make 
cd ../src/
g++ (or clang++ or whatever) -o main main.cpp

#### Usage : 

After building the project, you can run your executable (e.g., ASTConsumer) as follows:

./ASTConsumer <input-file>

Or if you want over all files you can just ./main but you should modify it and provide it with all directories that you want to loop on.

## Getting database Part (Python)
## Requirements

- Python 3.6 or higher
- `datasets` library from Hugging Face
- `requests` library for HTTP requests
- Access to the internet to fetch datasets and interact with the GitHub API

## Installation

### Step 1: Clone the Repository

First, clone this repository to your local machine:

### Step 2: Install Dependencies

Install the required Python libraries using pip:
pip install datasets requests

### Step 3: Obtain a GitHub API Token

To use the GitHub API for downloading C files, you need a GitHub API token:

1. Go to your GitHub settings.
2. Navigate to Developer settings > Personal access tokens.
3. Generate a new token with the necessary permissions (e.g., `repo` for full control of private repositories).
4. Copy your new token.

Update the `headers` dictionary in `get_code.py` with your token:

```python
headers = {
    'Authorization': 'token YOUR_GITHUB_TOKEN',
    'Accept': 'application/vnd.github.v3+json'
}
```

### Usage

#### Extracting Embedded Systems Code
Run get_code.py to start the extraction process:
```
python get_code.py
```

This script will automatically identify C code snippets related to embedded systems from the specified dataset and save them to a designated directory.

#### Downloading C Files from GitHub Repositories
Specify the desired repositories or topics related to embedded systems in get_code.py and run the script. It will download the C files, applying the same embedded systems filter, and organize them into your local directory structure.