# This file is sourced by all *interactive* bash shells on startup,
# including some apparently interactive shells such as scp and rcp
# that can't tolerate any output.  So make sure this doesn't display
# anything or bad things will happen !

# Test for an interactive shell.  There is no need to set anything
# past this point for scp and rcp, and it's important to refrain from
# outputting anything in those cases.
if [[ $- != *i* ]] ; then
    # Shell is non-interactive.  Be done now!
    return
fi

alias l='ls -l --group-directories-first'
alias ll='ls -l'
alias la='ls -l --all --group-directories-first'

alias o='less'

alias ..='cd ..'
alias ...='cd ../..'

alias md='mkdir'
alias rd='rmdir'

alias gvi='gvim'

PATH="/home/july/bin:${PATH}"

diff-less() {
    source-highlight -s diff --out-format=esc | less
}
alias d-o='diff-less'

if [[ -f ~/.bashrc.local ]]; then
    source ~/.bashrc.local
fi

