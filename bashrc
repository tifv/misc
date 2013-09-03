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

alias l='ls -alF'
alias la='ls -la'
alias ll='ls -l'

alias o='less'

alias ..='cd ..'
alias ...='cd ../..'

alias md='mkdir'
alias rd='rmdir'

alias gvi='gvim'
PATH="${PATH}:/home/july/bin"

alias init='sudo /sbin/init'

alias gnome-wm-lock='dbus-send --type=method_call --dest=org.gnome.ScreenSaver /org/gnome/ScreenSaver org.gnome.ScreenSaver.Lock'
alias kde-wm-lock='qdbus org.freedesktop.ScreenSaver /ScreenSaver Lock'
alias wm-lock='kde-wm-lock'
alias pm-suspend='sudo /usr/sbin/pm-suspend'

etail() {
    echo -en '\033]2;etail\007'
    sudo /usr/bin/tail -f /var/log/emerge.log
}

etail-fetch() {
    echo -en '\033]2;etail-fetch\007'
    sudo /usr/bin/tail -f /var/log/emerge-fetch.log
}

make-o-matic() {
    while true
    do
        make
        inotifywait --event modify --event move_self "$@" || return
    done
}

diff-less() {
    source-highlight -s diff --out-format=esc | less
}
alias d-o='diff-less'

