## Table of Contents
1. [Project Introduction](#afk-timer)
2. [Purpose](#purpose)
3. [Key Features](#key-features)
4. [Installation and Execution](#installation-and-execution)
5. [Usage](#usage)
6. [Data Storage](#data-storage)
7. [Uninstallation](#uninstallation)
8. [Troubleshooting](#troubleshooting)
9. [License](#license)

# AFK Timer

![AFK Timer Image](https://private-user-images.githubusercontent.com/192361273/397818950-53c9889a-ee03-4700-b084-c04b83cbfc59.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ3MTYzOTIsIm5iZiI6MTczNDcxNjA5MiwicGF0aCI6Ii8xOTIzNjEyNzMvMzk3ODE4OTUwLTUzYzk4ODlhLWVlMDMtNDcwMC1iMDg0LWMwNGI4M2NiZmM1OS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQxMjIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MTIyMFQxNzM0NTJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01NDNjZDFlN2VjNThjZGRhMTQzZTQ1MzViNzNkN2NmMTU3YTJjMDYyZjhkOTc2Yjc1MzIzM2Y5MTBlMmIyOGJjJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.J1xmX1xhV8hPjzrKWilZm2WmnllEkXv8RTj2UjxK7pc)

AFK Timer is a simple and intuitive timer program designed for Windows environments to track AFK (Away From Keyboard) time.

The code was written and tested within approximately 4 hours, with an initial draft quickly set up using Claude 3.5 Sonnet, followed by feature additions and modifications.

---

## Purpose

Many productivity management apps exist, but I wanted an app that focuses solely on tracking AFK time to help reduce psychological procrastination. Since no such app existed, I decided to create one.

Have you ever thought, **"I should shower, but I just don’t want to..."**, and ended up wasting hours on your phone instead of getting up?

Or said to yourself, **"I’ll start my task right after this YouTube video,"** but then got sucked into autoplay and spent hours watching instead?

This program is designed to **hold yourself accountable** and help you make better use of your time.

Unlike commercial software, this app focuses solely on this purpose. It helps you track wasted time in front of your computer and reflect on it for a more efficient day.

For other activities like exercising, walking, watching sports, or reading, you can simply press the **Pause** button and resume tracking when you return to your computer!

---

## Key Features
- **AFK Time Tracking**: Detects inactivity for over 3 minutes based on mouse and keyboard activity and logs the AFK time.
- **Pause/Resume**: Pause or resume AFK tracking as needed.
- **Data Logging**: Logs daily AFK data and visualizes the last 7 days in a graph.
- **Auto Start**: Register the program to start automatically with your system.
- **Midnight Reset**: Automatically resets the timer at midnight and saves the data.

---

## Installation and Execution

### 1. System Requirements
- Windows 10 or later
- Python 3.7 or later (if using source code)
- Required Libraries:
  - `tkinter`
  - `matplotlib`
  - `pynput`
  - `win32api`, `win32con`, `win32gui`, `winreg`

### 2. Installation Methods
#### A. Using the Executable File (Recommended)
1. Download the executable file from the GitHub Release section.
2. Double-click the executable file to run the program.

#### B. Running from Source Code
1. Clone this repository:
   ```bash
   git clone https://github.com/username/afk-timer.git
   cd afk-timer
   ```
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program:
   ```bash
   python idletimer.py
   ```

---

## Usage

1. **Launch the program**, and a small widget will appear, displaying live AFK time.
2. **Pause/Resume Button**: Pause or resume AFK tracking.
3. **Exit Button**: Save the current data and close the program. Upon relaunch, the widget will appear at its last position.
4. **Graph**: Displays the last 7 days of AFK data visually.

---

## Data Storage

AFK data and configuration files are saved in the following locations:
- `Documents/AFKTimer/afk_history.json`
- `Documents/AFKTimer/widget_config.ini`

---

## Uninstallation

1. Run the `deletereg.exe` file to remove the program from startup settings. (If it fails, you can try administrator mode)
2. Delete the program's executable file and related data (e.g., `Documents/AFKTimer`).

---

## Troubleshooting

I anticipate there may be bugs that I missed due to the short development time. 

Feel free to open a discussion or issue, and I will address them as soon as possible.

### Bug Reporting Template

#### 1. Bug Summary
- Briefly describe the issue.
  - Example: "Pause button does not stop the AFK timer."

#### 2. Steps to Reproduce
1. **First Step**: Example: Run the program.
2. **Second Step**: Example: Click the Pause button.
3. **Third Step**: Example: Stop using the mouse and keyboard.
4. **Fourth Step**: Example: The AFK timer continues to increase.

#### 3. Expected Behavior
- Describe how the program should behave.
  - Example: "The AFK timer should stop when the Pause button is clicked."

#### 4. Actual Behavior
- Describe what actually happens.
  - Example: "The AFK timer keeps running despite clicking Pause."

#### 5. Screenshot or Logs (Optional)
- Provide screenshots or logs that show the issue. 

#### 6. Environment
- Specify the environment where the issue occurred:
  - **Operating System**: Example: Windows 10 / Windows 11
  - **Python Version** (if using source code): Example: Python 3.9
  - **AFK Timer Version**: Example: v1.0.1
  - **Multi-Monitor Setup**: Example: Yes / No

---

## Q&A

#### Q: The program does not automatically start with the system.
1. The program generates an `autostart_afktimer.reg` file.
2. Run this file to register the program as a startup application.

#### Q: The graph does not display correctly.
1. Ensure that `matplotlib` is installed correctly:
   ```bash
   pip install matplotlib
   ```

---

## License

This project is licensed under the **MIT License**.

You are free to **use, modify, distribute, and commercially exploit** this software!
Just make sure to attribute the original author and note that the software is provided "as is" without any warranty.
