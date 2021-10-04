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

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/dbihbka/Downloads/google-cloud-sdk/path.zsh.inc' ]; then . '/Users/dbihbka/Downloads/google-cloud-sdk/path.zsh.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/Users/dbihbka/Downloads/google-cloud-sdk/completion.zsh.inc' ]; then . '/Users/dbihbka/Downloads/google-cloud-sdk/completion.zsh.inc'; fi

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
