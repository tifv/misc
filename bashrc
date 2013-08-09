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
alias pm-suspend='sudo /usr/sbin/pm-suspend'

nau() {
    if [ $# -eq 0 ]
    then
        nautilus . &> /dev/null &
    else
        nautilus "$@" &> /dev/null &
    fi
}

mysetxkbmap() {
    setxkbmap -layout 'us,ru'
    setxkbmap -option ''
    setxkbmap -option 'altwin:meta_win,grp:caps_toggle,grp_led:caps'
}

etail() {
    echo -en '\033]2;etail\007'
    sudo /usr/bin/tail -f /var/log/emerge.log
}

make-o-matic() {
    while true
    do
        make
        inotifywait --event modify --event move_self "$@" || return
    done
}

# Return 0 if we are running inside guake
guake-status() {
    guakepid=$(pgrep -f guake)
    mytty=$(tty | sed 's|/dev/||')

    if [ -z "$guakepid" ]
    then
        echo "Guake does not seem to be running" 1>&2
        return 1
    fi

    if [ -z "$mytty" ]
    then
        echo "We are not on a tty" 1>&2
        return 1
    fi

    if [ $(echo "$guakepid" | wc -l) -gt 1 ]
    then
        echo "Failed to identify single guake process" 1>&2
        return 1
    fi

    if [ -z "$(ps -Af | grep "$guakepid" | grep "$mytty" | grep "bash")" ]
    then
        echo "We are not in guake" 1>&2
        return 1
    fi

    echo "We are in guake" 1>&2
    return 0
}

alias cdj='cd ~/olm/jeolm'

alias jeolm='python3.3 -m jeolm'
alias jtimer='python3.3 -m jtimer'

_jeolm_completion() {
    COMPREPLY=( $(python3.3 -m jeolm.completion "$COMP_CWORD" "${COMP_WORDS[@]}") )
    completioncode=$?

    # This exit code is deliberately defined to mean that directory
    # completion is requested.
    case $completioncode in
        100)
            COMPREPLY=( $(compgen -o filenames -A file "${COMP_WORDS[COMP_CWORD]}") )
            return 0
            ;;
        101)
            COMPREPLY=( $(compgen -o dirnames -A directory "${COMP_WORDS[COMP_CWORD]}") )
            return 0
            ;;
        *)
        ;;
    esac

    return 0
}
complete -o nospace -F _jeolm_completion jeolm

