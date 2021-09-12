# Label Checker
<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>

  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Label checker is a python project to create the data set used in a solution by playing a video with the name of the word in which it is said and saving the word in which the video is said in a file with the suffix .csv by the user. 
This data can be used to train the **lipreading model**

<!-- GETTING STARTED -->
## Getting Started

Just copy and paste this codes to install dependencies and run the project

### Prerequisites

create an environment with `python 3.7`
  ```sh
  conda create -n "ENVIRONMENT_NAME" python=3.7
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/LabelChecker.git
   ```
2. Install `PyQt` on your system
   ```sh
   sudo apt-get install python3-pyqt5
   ```
      
3. Install Python libraries
   ```sh
   pip install PyQt5
   pip install pandas
   pip install numpy
   ```

<!-- USAGE EXAMPLES -->
## Usage

make sure all the directories in such a structure:
    ...

    videos
      word 1
         sample 1.mp4
         sample 2.mp4
         sample 3.mp4
      word 2
         sample 1.mp4
      word 3
         sample 1.mp4
      ...

and then in project directory run main.py file
   ```sh
   python main.py
   ```

## Result
The result in the results folder is stored in a folder called the name you entered at the beginning of the last session, which indicates the number of times you tried.



