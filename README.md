# CLI-env-setter

A simple CLI to set up a development environment for disnake

# Demo

https://user-images.githubusercontent.com/100313469/204569124-c3d8e5b3-a047-463a-8f72-38238d5058fd.mp4

# Requirements
if runned as script:
```
click
```

if runned as `.exe` none (the .exe file is located under the `dist` directory)

# How to run the command?
Clone this repository with:
```
git clone https://github.com/Snipy7374/CLI-dev-env-setter
```
You have two different ways to run the command:
- run the command with Python as script
- execute the .exe file

#Running as script
Go in the directory where you have cloned the repository and execute the following command
```
python -m pip install click
```
to install the required dependencies, then run
```
python env_setter.py
```
this command will display all the subcommands and it's options

to setup an environment for disnake run
```
python env_setter.py setup
```
checks `python env_setter.py setup -h` for more informations about the setup subcommand

# Running as .exe
Go in the directory where you have cloned the repository and execute the following command
```
cd dist
```
then run
```
.\env_setter
```
this command will display all the subcommands and it's options

to setup an environment for disnake run
```
.\env_setter setup
```
check `.\env_setter setup -h` for more informations about the setup subcommand
