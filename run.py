#!/usr/bin/env python

from __future__ import annotations

import logging
import pathlib
import platform
import shutil
import shlex
import subprocess
import warnings


def get_script_path() -> pathlib.Path:
    return pathlib.Path.cwd() / __file__


def eval_os_cmd(cmd: str) -> tuple[int, str]:
    logging.debug(shlex.split(cmd))
    proc = subprocess.Popen(shlex.split(cmd),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    if proc.returncode:
        return proc.returncode, f"Evaluation of {cmd} raised the error {stderr}"
    else:
        return proc.returncode, stdout.decode("utf8")


def install_brew():
    if platform.system() == "Darwin":
        if shutil.which("brew") is None:
            eval_os_cmd(
                "/bin/bash -c '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)'"
            )
    else:
        raise ValueError(f"{platform.system()} is not supported")


def install_git():
    if platform.system() == "Darwin":
        if shutil.which("git") is None:
            eval_os_cmd("brew install git")
    elif platform.system() == "Linux":
        if shutil.which("git") is None:
            eval_os_cmd("sudo apt install -y git")
    else:
        raise ValueError(f"{platform.system()} is not supported")


def install_curl():
    if platform.system() == "Darwin":
        if shutil.which("curl") is None:
            eval_os_cmd("brew install curl")
    elif platform.system() == "Linux":
        if shutil.which("curl") is None:
            eval_os_cmd("sudo apt install -y curl")
    else:
        raise ValueError(f"{platform.system()} is not supported")


def copy_tmux_config(dot_folder: pathlib.Path):
    logging.debug("Installing tmux config ...")
    tmux_conf_src = dot_folder / "tmux.conf"
    tmux_conf_dst = pathlib.Path.home() / ".tmux.conf"

    if tmux_conf_dst.exists():
        if tmux_conf_dst.is_symlink() and tmux_conf_dst.resolve(
        ) == tmux_conf_src:
            logging.info(
                f"{tmux_conf_dst} is alread symlink to the {tmux_conf_src}")
        else:
            raise ValueError(f"{tmux_conf_dst} exists.")
    else:
        tmux_conf_dst.symlink_to(tmux_conf_src)


def copy_neovim_config(dot_folder: pathlib.Path):
    logging.debug("Installing neovim config ...")

    neovim_conf_src = dot_folder / "nvim"
    neovim_conf_dst = pathlib.Path.home() / ".config/nvim"

    if neovim_conf_dst.exists():
        if neovim_conf_dst.is_symlink() and neovim_conf_dst.resolve(
        ) == neovim_conf_src:
            logging.info(
                f"{neovim_conf_dst} is alread symlink to the {neovim_conf_src}"
            )
        else:
            raise ValueError(f"{neovim_conf_dst} exists.")
    else:
        neovim_conf_dst.symlink_to(neovim_conf_src)


def copy_git_message(dot_folder: pathlib.Path):
    logging.debug("Installing git message...")

    gitmessage_src = dot_folder / "gitmessage"
    gitmessage_dst = pathlib.Path.home() / ".gitmessage"

    if gitmessage_dst.exists():
        if gitmessage_dst.is_symlink() and gitmessage_dst.resolve(
        ) == gitmessage_src:
            logging.info(
                f"{gitmessage_dst} is alread symlink to the {gitmessage_src}")
        else:
            raise ValueError(f"{gitmessage_dst} exists.")
    else:
        gitmessage_dst.symlink_to(gitmessage_src)
    eval_os_cmd("git config --global commit.template ~/.gitmessage")


def copy_kitty_config(dot_folder: pathlib.Path):
    logging.debug("Installing kitty config ...")
    if platform.system() == "Linux":

        kitty_conf_src = dot_folder / "kitty"
        kitty_conf_dst = pathlib.Path.home() / ".config/kitty"

        if kitty_conf_dst.exists():
            if kitty_conf_dst.is_symlink() and kitty_conf_dst.resolve(
            ) == kitty_conf_src:
                logging.info(
                    f"{kitty_conf_dst} is alread symlink to the {kitty_conf_src}"
                )
            else:
                raise ValueError(f"{kitty_conf_dst} exists.")
        else:
            kitty_conf_dst.symlink_to(kitty_conf_src)
    else:
        logging.info(f"Platform {platform.platform()} is not supported")


def copy_zsh_config(dot_folder: pathlib.Path):
    logging.debug("Installing zsh config ...")
    zsh_conf_src = dot_folder / "zshrc"
    zsh_conf_dst = pathlib.Path.home() / ".zshrc"

    if zsh_conf_dst.exists():
        if zsh_conf_dst.is_symlink() and zsh_conf_dst.resolve(
        ) == zsh_conf_src:
            logging.info(
                f"{zsh_conf_dst} is alread symlink to the {zsh_conf_src}")
        else:
            raise ValueError(f"{zsh_conf_dst} exists.")
    else:
        zsh_conf_dst.symlink_to(zsh_conf_src)


def install_fira_code():
    logging.debug("Installing fira code...")
    if platform.system() == "Linux":
        rcode, msg = eval_os_cmd("apt list --installed fonts-firacode")
        if not rcode and len(msg.rstrip().split("\n")) == 1:
            rcode, msg = eval_os_cmd("sudo apt install -y fonts-firacode")
            if rcode:
                logging.critical(msg)
    elif platform.system() == "Darwin":
        install_brew()
        rcode, _ = eval_os_cmd("brew list --cask font-fira-code")
        if rcode:
            warnings.warn(f"list firacode returns {rcode}")
            eval_os_cmd(
                "brew tap homebrew/cask-fonts && brew cask install font-fira-code"
            )


def install_dircolors():
    logging.debug("Installing dircolors...")
    if platform.system() == "Darwin":
        rcode, _ = eval_os_cmd("brew list coreutils")
        if rcode:
            rcode, msg = eval_os_cmd("brew install coreutils")
            if rcode:
                logging.critical(msg)
    elif platform.system() == "Linux":
        logging.info("Linux has dircolors by default")
    else:
        raise ValueError(f"{platform.system()} platform is not supported yet")


def install_zsh():
    logging.debug("Installing zsh...")
    if platform.system() == "Linux":
        rcode, msg = eval_os_cmd("apt list --installed zsh")
        if not rcode and len(msg.rstrip().split("\n")) == 1:
            rcode, msg = eval_os_cmd("sudo apt install -y zsh")
            if rcode:
                logging.critical(msg)
        rcode, msg = eval_os_cmd("chsh -s $(which zsh) dbihbka")
        if rcode:
            logging.critical(msg)
    elif platform.system() == "Darwin":
        logging.info("MacOS X uses zsh by default")
    else:
        raise ValueError(f"{platform.system()} platform is not supported yet")


def install_kitty():
    logging.debug("Installing kitty...")
    if platform.system() == "Linux":
        rcode, msg = eval_os_cmd("apt list --installed kitty")
        if not rcode and len(msg.rstrip().split("\n")) == 1:
            rcode, msg = eval_os_cmd("sudo apt install -y kitty")
            if rcode:
                logging.critical(msg)
    elif platform.system() == "Darwin":
        logging.info("with use iTerm2 in MacOS X usually")
    else:
        raise ValueError(f"{platform.system()} platform is not supported yet")


def install_vim_plug():
    logging.info("Install vim plug...")
    config_folder = pathlib.Path.home() / ".local/share"
    logging.critical(
        f"curl -fLo {config_folder}/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
    )


def install_node():
    # list of useful nvm commands: https://github.com/nvm-sh/nvm#usage
    logging.info("Installing node via NVM...")
    if shutil.which("node") is None:
        rcode, msg = eval_os_cmd(
            "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && nvm use stable"
        )
        if rcode:
            logging.critical(msg)


def install_neovim():
    if platform.system() == "Darwin":
        if shutil.which("nvim") is None:
            eval_os_cmd("brew install --fetch-HEAD tree-sitter luajit neovim")
    elif platform.system() == "Linux":
        if shutil.which("nvim") is None:
            eval_os_cmd("sudo apt install -y neovim")
    else:
        raise ValueError(f"{platform.system()} is not supported")


def install_tmux():
    if platform.system() == "Darwin":
        if shutil.which("tmux") is None:
            eval_os_cmd("brew install tmux")
    elif platform.system() == "Linux":
        if shutil.which("tmux") is None:
            eval_os_cmd("sudo apt install -y tmux")
    else:
        raise ValueError(f"{platform.system()} is not supported")


def install_diff():
    if platform.system() == "Darwin":
        if shutil.which("diff-so-fancy") is None:
            eval_os_cmd("brew install diff-so-fancy")
    elif platform.system() == "Linux":
        if shutil.which("diff-so-fancy") is None:
            eval_os_cmd("sudo apt install -y diff-so-fancy")
    else:
        raise ValueError(f"{platform.system()} is not supported")
    # postinstall usage
    # https://github.com/so-fancy/diff-so-fancy#usage
    commands = [
        'git config --global core.pager "diff-so-fancy | less --tabs=4 -RFX"',
        'git config --global interactive.diffFilter "diff-so-fancy --patch"',
        'git config --global color.ui true',
        'git config --global color.diff-highlight.oldNormal    "red bold"',
        'git config --global color.diff-highlight.oldHighlight "red bold 52"',
        'git config --global color.diff-highlight.newNormal    "green bold"',
        'git config --global color.diff-highlight.newHighlight "green bold 22"',
        'git config --global color.diff.meta       "11"',
        'git config --global color.diff.frag       "magenta bold"',
        'git config --global color.diff.func       "146 bold"',
        'git config --global color.diff.commit     "yellow bold"',
        'git config --global color.diff.old        "red bold"',
        'git config --global color.diff.new        "green bold"',
        'git config --global color.diff.whitespace "red reverse"',
    ]
    for cmd in commands:
        eval_os_cmd(cmd)


def install_df():
    if platform.system() == "Darwin":
        if shutil.which("duf") is None:
            eval_os_cmd("brew install duf")
    elif platform.system() == "Linux":
        if shutil.which("duf") is None:
            eval_os_cmd("sudo apt install -y duf")
    else:
        raise ValueError(f"{platform.system()} is not supported")


def install_fx():
    if platform.system() == "Darwin":
        if shutil.which("fx") is None:
            eval_os_cmd("npm install -g fx")
    elif platform.system() == "Linux":
        if shutil.which("fx") is None:
            eval_os_cmd("sudo npm install -g fx")
    else:
        raise ValueError(f"{platform.system()} is not supported")

def install_tldr():
    if platform.system() == "Darwin":
        if shutil.which("tldr") is None:
            eval_os_cmd("npm install -g tldr")
    elif platform.system() == "Linux":
        if shutil.which("tldr") is None:
            eval_os_cmd("sudo npm install -g tldr")
    else:
        raise ValueError(f"{platform.system()} is not supported")



def install_zsh_plugins():
    install_git()
    zsh_folder = pathlib.Path.home() / ".zsh"
    if not zsh_folder.exists():
        zsh_folder.mkdir()
    rcode, msg = eval_os_cmd(
        f"git clone https://github.com/zsh-users/zsh-autosuggestions {zsh_folder}/zsh-autosuggestions"
    )
    if rcode:
        warnings.warn(msg)

    rcode, msg = eval_os_cmd(
        f"git clone --recursive https://github.com/joel-porquet/zsh-dircolors-solarized {zsh_folder}/zsh-dircolors-solarized"
    )
    if rcode:
        logging.critical(msg)


def install_starship():
    logging.debug("Installing starship...")
    if platform.system() == "Darwin":
        rcode, _ = eval_os_cmd("brew list starship")
        if rcode:
            eval_os_cmd("brew install starship")
    elif platform.system() == "Linux":
        if shutil.which("starship") is None:
            rcode, msg = eval_os_cmd(
                "curl -fsSL https://starship.rs/install.sh | bash")
            if rcode:
                raise RuntimeError(msg)
    else:
        raise ValueError(f"{platform.system()} platform isnot supported yet")


def install_exa():
    logging.debug("Installing exa ...")
    if platform.system() == "Darwin":
        install_brew()
        rcode, _ = eval_os_cmd("brew list exa")
        if rcode:
            rcode, msg = eval_os_cmd("brew install exa")
            if rcode:
                logging.warn(msg)
    elif platform.system() == "Linux":
        rcode, msg = eval_os_cmd("apt list --installed exa")
        if not rcode and len(msg.rstrip().split("\n")) == 1:
            rcode, msg = eval_os_cmd("sudo apt install -y exa")
            if rcode:
                logging.critical(msg)


def install_fd():
    logging.debug("Installing fd ...")
    if platform.system() == "Darwin":
        install_brew()
        rcode, _ = eval_os_cmd("brew list fd")
        if rcode:
            rcode, msg = eval_os_cmd("brew install fd")
            if rcode:
                logging.warn(msg)
    elif platform.system() == "Linux":
        rcode, msg = eval_os_cmd("apt list --installed fd-find")
        if not rcode and len(msg.rstrip().split("\n")) == 1:
            rcode, msg = eval_os_cmd("sudo apt install -y fd-find")
            if rcode:
                logging.critical(msg)


def install_rg():
    logging.debug("Installing rg (ripgrep) ...")
    if platform.system() == "Darwin":
        install_brew()
        rcode, _ = eval_os_cmd("brew list ripgrep")
        if rcode:
            rcode, msg = eval_os_cmd("brew install ripgrep")
            if rcode:
                logging.warn(msg)
    elif platform.system() == "Linux":
        rcode, msg = eval_os_cmd("apt list --installed ripgrep")
        if not rcode and len(msg.rstrip().split("\n")) == 1:
            rcode, msg = eval_os_cmd("sudo apt install -y ripgrep")
            if rcode:
                logging.critical(msg)


def install_bat():
    logging.debug("Installing bat ...")
    if platform.system() == "Darwin":
        install_brew()
        rcode, _ = eval_os_cmd("brew list bat")
        if rcode:
            rcode, msg = eval_os_cmd("brew install bat")
            if rcode:
                logging.warn(msg)
    elif platform.system() == "Linux":
        rcode, msg = eval_os_cmd("apt list --installed bat")
        if not rcode and len(msg.rstrip().split("\n")) == 1:
            rcode, msg = eval_os_cmd("sudo apt install -y bat")
            if rcode:
                logging.critical(msg)


def generate_alaises(dot_folder, aliases):
    logging.debug("Generating aliases ...")
    alias_conf_src = dot_folder / "aliases"
    alias_conf_dst = pathlib.Path.home() / ".aliases"

    with open(alias_conf_src, "w") as src:
        grep_cmd = "grep=rg"
        dircolors_cmd = "dircolors=dircolors"
        cat_cmd = "cat=cat"
        find_cmd = "find=find"
        df_cmd = "df=duf"
        if platform.system() == "Darwin":
            dircolors_cmd = "dircolors=gdircolors"
            cat_cmd = "cat=bat"
            find_cmd = "find=fd"
        elif platform.system() == "Linux":
            dircolors_cmd = "dircolors=dircolors"
            cat_cmd = "cat=batcat"
            find_cmd = "find=fdfind"

        ls_cmd = "ls=exa"
        src.write("\n".join([
            f"alias {cmd}" for cmd in aliases +
            [ls_cmd, dircolors_cmd, find_cmd, cat_cmd, grep_cmd, df_cmd]
        ]))

    if alias_conf_dst.exists():
        if alias_conf_dst.is_symlink() and alias_conf_dst.resolve(
        ) == alias_conf_src:
            logging.info(
                f"{alias_conf_dst} is alread symlink to the {alias_conf_src}")
        else:
            raise ValueError(f"{alias_conf_dst} exists.")
    else:
        alias_conf_dst.symlink_to(alias_conf_src)


def install_bazel_compilation_database(dot_folder):
    """Install the tool to generate compile_command.json
    for bazel projects.
    https://github.com/grailbio/bazel-compilation-database
    """

    bin_folder = dot_folder / "bin"
    if not bin_folder.exists():
        bin_folder.mkdir()

    install_dir = str(bin_folder)
    version = "0.4.5"
    cmd = f"/bin/bash -c '$(curl -L https://github.com/grailbio/bazel-compilation-database/archive/{version}.tar.gz | tar --directory {install_dir} -xz)'"

    logging.debug(cmd)

    rcode, msg = eval_os_cmd(cmd)

    if rcode:
        logging.critical(msg)
        return None
    else:
        msg = f"bazel compilation database version {version} installed to {install_dir}"
        logging.debug(msg)

    return f"bazel-compdb={install_dir}/bazel-compilation-database-{version}/generate.sh"


def main():
    dot_folder = get_script_path().parent

    install_git()
    install_curl()
    install_fira_code()
    install_zsh()
    install_zsh_plugins()
    install_starship()
    install_exa()
    install_dircolors()
    install_fd()
    install_rg()
    install_bat()
    install_kitty()
    install_node()
    install_vim_plug()
    install_neovim()
    install_tmux()
    install_diff()
    install_df()
    install_fx()
    install_tldr()

    bcdalias = install_bazel_compilation_database(dot_folder)
    generate_alaises(dot_folder, [bcdalias])

    copy_zsh_config(dot_folder)
    copy_tmux_config(dot_folder)
    copy_neovim_config(dot_folder)
    copy_git_message(dot_folder)

    if platform.system() == "Linux":
        copy_kitty_config(dot_folder)


if __name__ == "__main__":
    try:
        from rich.logging import RichHandler
    except ImportError:
        RichHandler = logging.StreamHandler

    FORMAT = "%(message)s"
    logging.basicConfig(level="NOTSET",
                        format=FORMAT,
                        datefmt="[%X]",
                        handlers=[RichHandler()])
    main()
