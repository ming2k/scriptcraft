#!/bin/bash

# rm -rf ~/.config/nvim.bak && mv ~/.config/nvim ~/.config/nvim.bak
rm -f ~/.config/nvim/lazy-lock.json
rm -rf ~/.local/share/nvim.bak && mv -f ~/.local/share/nvim ~/.local/share/nvim.bak
rm -rf ~/.local/state/nvim.bak && mv -f ~/.local/state/nvim ~/.local/state/nvim.bak
rm -rf ~/.cache/nvim.bak && mv -f ~/.cache/nvim ~/.cache/nvim.bak
