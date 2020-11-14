#!/usr/bin/env python

import logging
import pathlib
import platform
import shutil
import shlex
import subprocess
import warnings


def get_script_path() -> pathlib.Path:
  return pathlib.Path.cwd() / __file__


def eval_os_cmd(cmd: str) -> (int, str):
  proc = subprocess.Popen(shlex.split(cmd),
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
  _, stderr = proc.communicate()

  return proc.returncode, f'Evaluation of {cmd} raised the error {stderr}'


def install_brew():
  if platform.system() == 'Darwin':
    if shutil.which('brew') is None:
      eval_os_cmd(
          '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"'
      )
  else:
    raise ValueError(f'{platform.system()} is not supported')


def install_git():
  if platform.system() == 'Darwin':
    if shutil.which('git') is None:
      eval_os_cmd('brew install git')
  elif platform.system() == 'Linux':
    if shutil.which('git') is None:
      eval_os_cmd('sudo apt install -y git')
  else:
    raise ValueError(f'{platform.system()} is not supported')


def copy_tmux_config(dot_folder: pathlib.Path):
  logging.debug('Installing tmux config ...')
  tmux_conf_src = dot_folder / 'tmux.conf'
  tmux_conf_dst = pathlib.Path.home() / '.tmux.conf'

  if tmux_conf_dst.exists():
    if tmux_conf_dst.is_symlink() and tmux_conf_dst.resolve() == tmux_conf_src:
      logging.info(f'{tmux_conf_dst} is alread symlink to the {tmux_conf_src}')
    else:
      raise ValueError(f'{tmux_conf_dst} exists.')
  else:
    tmux_conf_dst.symlink_to(tmux_conf_src)


def copy_neovim_config(dot_folder: pathlib.Path):
  logging.debug('Installing neovim config ...')

  neovim_conf_src = dot_folder / 'nvim'
  neovim_conf_dst = pathlib.Path.home() / '.config/nvim'

  if neovim_conf_dst.exists():
    if neovim_conf_dst.is_symlink() and neovim_conf_dst.resolve(
    ) == neovim_conf_src:
      logging.info(
          f'{neovim_conf_dst} is alread symlink to the {neovim_conf_src}')
    else:
      raise ValueError(f'{neovim_conf_dst} exists.')
  else:
    neovim_conf_dst.symlink_to(neovim_conf_src)


def copy_kitty_config(dot_folder: pathlib.Path):
  logging.debug("Installing kitty config ...")
  if platform.system() == 'Linux':

    kitty_conf_src = dot_folder / 'kitty'
    kitty_conf_dst = pathlib.Path.home() / '.config/kitty'

    if kitty_conf_dst.exists():
      if kitty_conf_dst.is_symlink() and kitty_conf_dst.resolve(
      ) == kitty_conf_src:
        logging.info(
            f'{kitty_conf_dst} is alread symlink to the {kitty_conf_src}')
      else:
        raise ValueError(f'{kitty_conf_dst} exists.')
    else:
      kitty_conf_dst.symlink_to(kitty_conf_src)
  else:
    logging.info(f'Platform {platform.platform()} is not supported')


def copy_zsh_config(dot_folder: pathlib.Path):
  logging.debug("Installing zsh config ...")
  zsh_conf_src = dot_folder / 'zshrc'
  zsh_conf_dst = pathlib.Path.home() / '.zshrc'

  if zsh_conf_dst.exists():
    if zsh_conf_dst.is_symlink() and zsh_conf_dst.resolve() == zsh_conf_src:
      logging.info(f'{zsh_conf_dst} is alread symlink to the {zsh_conf_src}')
    else:
      raise ValueError(f'{zsh_conf_dst} exists.')
  else:
    zsh_conf_dst.symlink_to(zsh_conf_src)


def install_fira_code():
  logging.debug("Installing fira code...")
  if platform.system() == 'Linux':
    rcode, _ = eval_os_cmd("apt list --installed fonts-firacode")
    if not rcode and len(msg.decode('utf8').rstrip().split('\n')) == 1:
      rcode, msg = eval_os_cmd("sudo apt install -y fonts-firacode")
      if rcode:
        logging.critical(msg)
  elif platform.system() == 'Darwin':
    install_brew()
    rcode, _ = eval_os_cmd("brew list --cask font-fira-code")
    if rcode:
      warnings.warn(f"list firacode returns {rcode}")
      eval_os_cmd(
          "brew tap homebrew/cask-fonts && brew cask install font-fira-code")


def install_dircolors():
  logging.debug("Installing dircolors...")
  if platform.system() == 'Darwin':
    rcode, _ = eval_os_cmd("brew list coreutils")
    if rcode:
      rcode, msg = eval_os_cmd("brew install coreutils")
      if rcode:
        logging.critical(msg)
  elif platform.system() == 'Linux':
    logging.info("Linux has dircolors by default")
  else:
    raise ValueError(f'{platform.system()} platform is not supported yet')


def install_zsh():
  logging.debug("Installing zsh...")
  if platform.system() == 'Linux':
    rcode, _ = eval_os_cmd("apt list --installed zsh")
    if not rcode and len(msg.decode('utf8').rstrip().split('\n')) == 1:
      rcode, msg = eval_os_cmd("sudo apt install zsh")
      if rcode:
        logging.critical(msg)
    eval_os_cmd("chsh -s $(which zsh)")
  elif platform.system() == 'Darwin':
    logging.info("MacOS X uses zsh by default")
  else:
    raise ValueError(f'{platform.system()} platform is not supported yet')


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
  if platform.system() == 'Darwin':
    rcode, _ = eval_os_cmd('brew list starship')
    if rcode:
      eval_os_cmd('brew install starship')
  elif platform.system() == 'Linux':
    if shutil.which('starship') is None:
      rcode, msg = eval_os_cmd(
          'curl -fsSL https://starship.rs/install.sh | bash')
      if rcode:
        raise RuntimeError(msg)
  else:
    raise ValueError(f'{platform.system()} platform isnot supported yet')


def install_exa():
  logging.debug('Installing exa ...')
  if platform.system() == 'Darwin':
    install_brew()
    rcode, _ = eval_os_cmd('brew list exa')
    if rcode:
      rcode, msg = eval_os_cmd('brew install exa')
      if rcode:
        logging.warn(msg)
  elif platform.system() == 'Linux':
    rcode, _ = eval_os_cmd("apt list --installed exa")
    if not rcode and len(msg.decode('utf8').rstrip().split('\n')) == 1:
      rcode, msg = eval_os_cmd('sudo apt install exa')
      if rcode:
        logging.critical(msg)


def install_fd():
  logging.debug('Installing fd ...')
  if platform.system() == 'Darwin':
    install_brew()
    rcode, _ = eval_os_cmd('brew list fd')
    if rcode:
      rcode, msg = eval_os_cmd('brew install fd')
      if rcode:
        logging.warn(msg)
  elif platform.system() == 'Linux':
    rcode, _ = eval_os_cmd("apt list --installed fd-find")
    if not rcode and len(msg.decode('utf8').rstrip().split('\n')) == 1:
      rcode, msg = eval_os_cmd("sudo apt install -y fd-find")
      if rcode:
        logging.critical(msg)


def install_bat():
  logging.debug('Installing bat ...')
  if platform.system() == 'Darwin':
    install_brew()
    rcode, _ = eval_os_cmd('brew list bat')
    if rcode:
      rcode, msg = eval_os_cmd('brew install bat')
      if rcode:
        logging.warn(msg)
  elif platform.system() == 'Linux':
    rcode, _ = eval_os_cmd("apt list --installed bat")
    if not rcode and len(msg.decode('utf8').rstrip().split('\n')) == 1:
      rcode, msg = eval_os_cmd('sudo apt install -y bat')
      if rcode:
        logging.critical(msg)


def generate_alaises(dot_folder):
  logging.debug("Generating aliases ...")
  alias_conf_src = dot_folder / 'aliases'
  alias_conf_dst = pathlib.Path.home() / '.aliases'

  with open(alias_conf_src, 'w') as src:
    if platform.system() == 'Darwin':
      dircolors_cmd = 'dircolors=gdircolors'
      cat_cmd = 'cat=bat'
    elif platform.system() == 'Linux':
      dircolors_cmd = 'dircolors=dircolors'
      cat_cmd = 'cat=batcat'
    ls_cmd = 'ls=exa'
    find_cmd = 'find=fd'
    src.write('\n'.join(
        [f'alias {cmd}' for cmd in [ls_cmd, dircolors_cmd, find_cmd]]))

  if alias_conf_dst.exists():
    if alias_conf_dst.is_symlink() and alias_conf_dst.resolve(
    ) == alias_conf_src:
      logging.info(
          f'{alias_conf_dst} is alread symlink to the {alias_conf_src}')
    else:
      raise ValueError(f'{alias_conf_dst} exists.')
  else:
    alias_conf_dst.symlink_to(alias_conf_src)


def main():
  dot_folder = get_script_path().parent

  install_fira_code()
  install_zsh()
  install_zsh_plugins()
  install_starship()
  install_exa()
  install_dircolors()
  install_fd()
  install_bat()

  generate_alaises(dot_folder)

  copy_zsh_config(dot_folder)
  copy_tmux_config(dot_folder)
  copy_neovim_config(dot_folder)

  if platform.system() == 'Linux':
    copy_kitty_config(dot_folder)


if __name__ == "__main__":
  import sys
  logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
  main()
