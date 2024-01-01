#!/bin/bash

set -eux
set -o pipefail

while getopts "h:g:c" opt; do
  case $opt in
    h) echo "Usage: $0 [-g GIT_SERVICE_URL] [-s]"; exit 0;;
    g) GIT_SERVICE_URL=$OPTARG;;
    c) USE_CHINA_SOURCE=true;;
    *) echo "Usage: $0 [-g GIT_SERVICE_URL] [-s]"; exit 1;;
  esac
done

if [ -z "$GIT_SERVICE_URL" ]; then
  GIT_SERVICE_URL="https://github.com"
fi

if [ "$USE_CHINA_SOURCE" = true ]; then
  echo "" > /etc/pacman.d/mirrorlist
  sudo sed -i 's/^#Server/Server/g' /etc/pacman.d/mirrorlist
  sudo sed -i '1i Server = http://mirrors.163.com/archlinux/$repo/os/$arch' /etc/pacman.d/mirrorlist
  sudo sed -i '2i Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch' /etc/pacman.d/mirrorlist
  sudo pacman -Syyu
fi

pacman -S --noconfirm \
    base-devel git curl wget vim tmux zsh cronie wireguard-tools chezmoi \
    exa ripgrep fzf htop bat duf fd jq procs tree starship \
    nodejs npm python python-pip go \
    docker docker-compose

git clone "${GIT_SERVICE_URL}/ohmyzsh/ohmyzsh.git" ~/.oh-my-zsh

git clone "${GIT_SERVICE_URL}/zsh-users/zsh-autosuggestions.git" ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

git clone "${GIT_SERVICE_URL}/zsh-users/zsh-syntax-highlighting.git" ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

chezmoi init --apply "${GIT_SERVICE_URL}/Mylodie/dotfiles.git"

chsh -s "$(which zsh)"