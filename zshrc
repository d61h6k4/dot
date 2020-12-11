HISTSIZE=500000
SAVEHIST=500000
setopt appendhistory
setopt INC_APPEND_HISTORY  
setopt SHARE_HISTORY

source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source ~/.zsh/zsh-dircolors-solarized/zsh-dircolors-solarized.zsh

source ~/.aliases
eval "$(starship init zsh)"

source ~/.profile
