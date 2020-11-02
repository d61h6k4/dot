#!/usr/bin/env python

import logging
import pathlib
import platform


def get_script_path() -> pathlib.Path:
    return pathlib.Path.cwd() / __file__


def copy_tmux_config(dot_folder: pathlib.Path):

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

    neovim_conf_src = dot_folder / 'nvim'
    neovim_conf_dst = pathlib.Path.home() / '.config/nvim'

    if neovim_conf_dst.exists():
        if neovim_conf_dst.is_symlink() and neovim_conf_dst.resolve() == neovim_conf_src:
            logging.info(f'{neovim_conf_dst} is alread symlink to the {neovim_conf_src}')
        else:
            raise ValueError(f'{neovim_conf_dst} exists.')
    else:
        neovim_conf_dst.symlink_to(neovim_conf_src)


def copy_kitty_config(dot_folder: pathlib.Path):
    if platform.system() == 'Linux':

        kitty_conf_src = dot_folder / 'kitty'
        kitty_conf_dst = pathlib.Path.home() / '.config/kitty'

        if kitty_conf_dst.exists():
            if kitty_conf_dst.is_symlink() and kitty_conf_dst.resolve() == kitty_conf_src:
                logging.info(f'{kitty_conf_dst} is alread symlink to the {kitty_conf_src}')
            else:
                raise ValueError(f'{kitty_conf_dst} exists.')
        else:
            kitty_conf_dst.symlink_to(kitty_conf_src)
    else:
        logging.info(f'Platform {platform.platform()} is not supported')


def main():
    dot_folder = get_script_path().parent

    copy_tmux_config(dot_folder)
    copy_neovim_config(dot_folder)
    copy_kitty_config(dot_folder)


if __name__ == "__main__":
    logging.basicConfig(filename='/dev/stderr', level=logging.DEBUG)
    main()
