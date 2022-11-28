import click
import subprocess
import os
import colorama

from typing import Optional, Union

__prog_name__ = "env > " # thanks nox for the cool name format suggestion
__version__ = "0.0.1"
__author__ = "Snipy7374"

PREFIX_COMMANDS_VERBOSE = colorama.Fore.LIGHTYELLOW_EX + __prog_name__ + colorama.Style.RESET_ALL

# TODO:
# - add the option --force-install

@click.group()
@click.help_option("-h", "--help")
@click.option("--verbose/--no-verbose", is_flag=True, default=True, show_default=True, help="enable verbosity")
@click.version_option(__version__, "-v", "--version", prog_name=__prog_name__, message="%(prog)s " + f"({__author__})" + " version: %(version)s")
@click.pass_context
def env(ctx, verbose: bool):
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose


@env.command()
@click.argument("repository", required=False, default="https://github.com/DisnakeDev/disnake")
@click.argument("path", required=False, default="./disnake_dev")
@click.help_option("-h", "--help")
@click.option("-b", "--branch", show_default=False, help="the only branch that you want to include")
@click.pass_context
def setup(ctx, repository: str, path: str, branch: str) -> None:
    verbose =  ctx.obj.get("VERBOSE", True)
    msg = clone_repository(repository=repository, path=path, branch=branch, verbose=verbose)
    if msg:
        click.echo(msg, color=True)
        return
    create_env_and_install_deps(path=path, verbose=verbose)
    


def clone_repository(*, repository: str, path: str, branch: Optional[str], verbose: bool) -> Union[str, None]:
    clone_path = path + "/disnake"
    clone_single_branch_cmd = ["git", "clone", "--branch", branch, "--single-branch", repository, clone_path]
    clone_cmd = ["git", "clone", repository, clone_path]
    verbose_msg = {
        "branch_clone": colorama.Fore.BLUE + "Cloning brach '{}' from repository '{}' in '{}'" + colorama.Style.RESET_ALL,
        "repo_clone": colorama.Fore.BLUE + "Cloning repository '{}' in '{}'" + colorama.Style.RESET_ALL,
        "clone_cmd": colorama.Fore.BLUE + "'" + " ".join(clone_cmd) + "'" + colorama.Style.RESET_ALL
    }
    if branch:
        verbose_msg["clone_single_branch_cmd"] = colorama.Fore.BLUE + " ".join(clone_single_branch_cmd) + colorama.Style.RESET_ALL
    if os.path.isdir(path):
        if any(file for file in os.listdir(path)):
            return PREFIX_COMMANDS_VERBOSE + colorama.Fore.RED + "ERROR: Can't use a directory with files! Create a new empty directory or use --force-install" + colorama.Style.RESET_ALL

    if branch:
        if verbose:
            click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["branch_clone"].format(branch, repository, clone_path), color=True)
            click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["clone_single_branch_cmd"], color=True)
        subprocess.run(
            clone_single_branch_cmd,
            shell=True,
        )
        return
    
    if verbose:
        click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["repo_clone"].format(repository, clone_path), color=True)
        click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["clone_cmd"], color=True)
    subprocess.run(
        clone_cmd,
        shell=True,
    )

def create_env_and_install_deps(path: str, verbose: bool) -> None:
    path_env = path + "/env"
    create_env_cmd = ["python", "-m", "venv", path_env]
    path_activate_env = path.replace("/", "\\") + "\\env\\Scripts\\Activate"
    install_deps_cdm = [path_activate_env, "&",
        "python", "-m", "pip", "install", "nox", "taskipy", "&"
        "cd", path + "/disnake", "&",
        "task", "setup_env"]
    verbose_msg = {
        "venv_creation": colorama.Fore.BLUE + "Creating virtual enviroment at '{}'" + colorama.Style.RESET_ALL,
        "deps_install": colorama.Fore.BLUE + "Activating virtaul enviroment '{}', installing dependencies 'nox' and 'taskipy', running 'task setup_env' to install dev dependencies" + colorama.Style.RESET_ALL,
        "successful": colorama.Fore.LIGHTGREEN_EX + "Installed successfully all the dependencies, remember to run '{}' to activate the virtual environment" + colorama.Style.RESET_ALL,
        "create_env_cmd": colorama.Fore.BLUE + "'" + " ".join(create_env_cmd) + "'" + colorama.Style.RESET_ALL,
        "env_created": colorama.Fore.BLUE + "Virtual Environment created successfully at '{}'" + colorama.Style.RESET_ALL,
        "install_deps_cmd": colorama.Fore.BLUE + "'"+ " ".join(install_deps_cdm) + "'" + colorama.Style.RESET_ALL
    }
    if verbose:
        click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["venv_creation"].format(path_env), color=True)
        click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["create_env_cmd"], color=True)
    subprocess.run(
        create_env_cmd,
        shell=True,
    )
    click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["env_created"].format(path_env), color=True)
    if verbose:
        click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["deps_install"].format(path_activate_env), color=True)
        click.echo(PREFIX_COMMANDS_VERBOSE + verbose_msg["install_deps_cmd"], color=True)
    subprocess.run(
        install_deps_cdm,
        shell=True,
    )
    click.echo("\n" + PREFIX_COMMANDS_VERBOSE + verbose_msg["successful"].format(path_activate_env), color=True)


if __name__ == '__main__':
    env(obj={})