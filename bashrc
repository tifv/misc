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

alias init='sudo /sbin/init'

alias kde-lock='qdbus org.freedesktop.ScreenSaver /ScreenSaver Lock'
alias kde-unlock='qdbus $(qdbus | grep kscreenlocker_greet) /MainApplication quit'
alias kde-suspend='qdbus org.freedesktop.PowerManagement /org/kde/Solid/PowerManagement/Actions/SuspendSession suspendToRam'

etail() {
    echo -en '\033]2;etail\007'
    sudo /usr/bin/tail -f /var/log/emerge.log
} # etail

etail-fetch() {
    echo -en '\033]2;etail-fetch\007'
    sudo /usr/bin/tail -f /var/log/emerge-fetch.log
} # etail-fetch

make-o-matic() {
    while true
    do
        sleep 0.2
        make
        inotifywait --event modify --event move_self "$@" || return
    done
} # make-o-matic

diff-less() {
    source-highlight -s diff --out-format=esc | less
} # diff-less
alias d-o='diff-less'

if [[ -f ~/.bashrc.local ]]; then
    source ~/.bashrc.local
fi
