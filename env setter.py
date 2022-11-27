import click
import subprocess
import os
import colorama

from typing import Optional, Union

__prog_name__ = ">> env setter"
__version__ = "0.0.1"
__author__ = "Snipy7374"

PREFIX_COMMANDS_VERBOSE = colorama.Fore.GREEN + __prog_name__ + colorama.Style.RESET_ALL

# TODO:
# - add the option --force-install

@click.command()
@click.argument("repository", required=False, default="https://github.com/DisnakeDev/disnake")
@click.argument("path", required=False, default="./disnake_dev")
@click.help_option("-h", "--help")
@click.option("--verbose/--no-verbose", is_flag=True, default=True, show_default=True, help="enable verbosity for the current command")
@click.version_option(__version__, "-v", "--version", prog_name=__prog_name__, message="%(prog)s " + f"({__author__})" + " version: %(version)s")
@click.option("-b", "--branch", show_default=False, help="the only branch that you want to include")
def setup_dev_env(repository: str, path: str, branch: str, verbose: bool) -> None:
    msg = clone_repository(repository=repository, path=path, branch=branch, verbose=verbose)
    if msg:
        click.echo(msg, color=True)
        return
    create_env_and_install_deps(path=path, verbose=verbose)
    


def clone_repository(*, repository: str, path: str, branch: Optional[str], verbose: bool) -> Union[str, None]:
    verbose_msg = {
        "branch_clone": colorama.Fore.BLUE + " Cloning brach '{}' from repository '{}' in '{}'" + colorama.Style.RESET_ALL,
        "repo_clone": colorama.Fore.BLUE + " Cloning repository '{}' in '{}'" + colorama.Style.RESET_ALL
    }
    clone_path = path + "/disnake"
    if os.path.isdir(path):
        if any(file for file in os.listdir(path)):
            return PREFIX_COMMANDS_VERBOSE + colorama.Fore.RED + " ERROR: Can't use a directory with files! Create a new empty directory or use --force-install" + colorama.Style.RESET_ALL

    if branch:
        if verbose:
            click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["branch_clone"].format(branch, repository, clone_path), color=True)
        subprocess.run(
            ["git", "clone", "--branch", branch, "--single-branch", repository, clone_path],
            shell=True
        )
        return
    
    if verbose:
        click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["repo_clone"].format(repository, clone_path), color=True)
    subprocess.run(
        ["git", "clone", repository, clone_path],
        shell=True
    )

def create_env_and_install_deps(path: str, verbose: bool) -> None:
    verbose_msg = {
        "venv_creation": colorama.Fore.BLUE + " Creating virtual enviroment at '{}'" + colorama.Style.RESET_ALL,
        "deps_install": colorama.Fore.BLUE + " Activating virtaul enviroment '{}', installing dependencies 'nox' and 'taskipy', running 'task setup_env' to install dev dependencies" + colorama.Style.RESET_ALL,
        "successful": colorama.Fore.BLUE + " Installed successfully all the dependencies, remember to run '{}' to activate the virtual environment" + colorama.Style.RESET_ALL
    }
    path_env = path + "/env"
    if verbose:
        click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["venv_creation"].format(path_env), color=True)
    subprocess.run(
        ["python", "-m", "venv", path_env],
        shell=True
    )
    path_activate_env = path.replace("/", "\\") + "\\env\\Scripts\\Activate"
    if verbose:
        click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["deps_install"].format(path_activate_env), color=True)
    subprocess.run(
        [path_activate_env, "&",
        "python", "-m", "pip", "install", "nox", "taskipy", "&"
        "cd", path + "/disnake", "&",
        "task", "setup_env"],
        shell=True
    )
    click.echo("\n\n" + PREFIX_COMMANDS_VERBOSE + verbose_msg["successful"].format(path_activate_env))


if __name__ == '__main__':
    setup_dev_env()