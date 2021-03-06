" vim: foldmethod=marker :

if exists('g:july_vimrc')
    finish
endif
let g:july_vimrc = 1

" Options {{{

" Vi compatibility
set cpoptions=

" Initialization and syntax
set fencs=utf-8,cp1251
syntax on
autocmd FileType plaintex set filetype=tex
set modeline

" Editing
set autoindent
set scrolloff=2
set virtualedit=block
set backspace=indent,eol,start
set nojoinspaces
set nrformats-=octal

set langmap=
    \ЙЦУКЕНГШЩЗ;QWERTYUIOP,
    \йцукенгшщз;qwertyuiop,
    \ФЫВАПРОЛД;ASDFGHJKL,
    \фывапролд;asdfghjkl,
    \ЯЧСМИТЬ;ZXCVBNM,
    \ячсмить;zxcvbnm,
    \ХЪЖЭБЮ;{}:\"<>,хъжэю;[];'.,ё`,Ё~

" Tabulation
set tabstop=8
set shiftwidth=4
set softtabstop=0
set expandtab
set smarttab

" Search and replace
set hlsearch
set incsearch
set showmatch
set gdefault

" Windows and commands
set hidden
set showcmd
set ruler
set history=1000
set wildmode=list:longest

" Local .vimrc
set exrc secure

" Swap and viminfo
set swapsync=
set viminfo='300,<50,s10,h,r/home/july/run

" Miscellaneous
set mouse=a

let python_highlight_all=1

" }}}

" Functions {{{

function NextDiff()
    setlocal nodiff noscrollbind
    2next
    setlocal diff scrollbind
    wincmd w
    setlocal nodiff noscrollbind
    2next
    setlocal diff scrollbind
    wincmd w
endfunction

function PrevDiff()
    setlocal nodiff noscrollbind
    2prev
    setlocal diff scrollbind
    wincmd w
    setlocal nodiff noscrollbind
    2prev
    setlocal diff scrollbind
    wincmd w
endfunction

function Comment()
    if exists("b:comment_sign")
      call setline(".", b:comment_sign . getline("."))
    endif
endfunction

function UnComment()
  if exists("b:comment_sign")
    let l:line = getline(".")
    let l:len = strlen(b:comment_sign)
    if strpart(l:line, 0, l:len) == b:comment_sign
      call setline(".", strpart(l:line, l:len, strlen(l:line)))
    endif
  endif
endfunction

let s:latexspaceerror = "" .
    \'-\@4<!\<\(' .
        \'[АаИиВвКкСсУу]\|' .
        \'[Ии]з\|[Оо][тб]\?\|[ДдПпСсВвКк]о\|[Зз]а\|[Нн][аеи]\|' .
    \'\)\zs\( \|\n\)\ze' .
\'\|' .
    \'\zs\( \|\n\)\ze\(---\|\%u2014\)' .
\'\|' .
    \'\zs\( \|\n\)\ze\(ли\|же\|бы\)\>' .
\'\|' .
    \'\zs\<[Тт]о\zs\( \|\n\)\zeесть\>' .
\'\|' .
    \'\%xA0'

function HighlighLaTeXSpaceErrors()
    highlight latexspaceerror ctermbg=lightmagenta guibg=lightmagenta
    execute "match latexspaceerror /" . s:latexspaceerror . "/"
endfunction

function SubstituteLaTeXSpaceErrors(r) range
    execute (a:firstline) . "," . (a:lastline) .
        \"substitute/" . s:latexspaceerror . '/' . a:r . '/ce'
endfunction

" }}}

" Mappings and autocommands {{{

nmap <F8> :call Comment()<CR><Down>
imap <F8> <C-O>:call Comment()<CR><Down>
vmap <F8> :call Comment()<CR>

nmap <F9> :call UnComment()<CR><Down>
imap <F9> <C-O>:call UnComment()<CR><Down>
vmap <F9> :call UnComment()<CR>

imap <F7> <C-O>:vertical resize 80<CR>
nmap <F7> :vertical resize 80<CR>

autocmd FileType vim let b:comment_sign = '"'
autocmd FileType make,python,sh let b:comment_sign = '#'
autocmd FileType yaml,conf,gitconfig let b:comment_sign = '#'
autocmd FileType gentoo-package-use let b:comment_sign = '#'
autocmd FileType gentoo-package-keywords let b:comment_sign = '#'
autocmd FileType tex,plaintex,mp,mf let b:comment_sign = "%"
autocmd FileType haskell let b:comment_sign = "--"
autocmd FileType javascript,pure,asy,go let b:comment_sign = "//"

autocmd FileType yaml setlocal shiftwidth=2
autocmd FileType tex,plaintex setlocal textwidth=79

" }}}

" Parts {{{

" [gvimrc]
"set guifont=Monospace\ 11
"set vb t_vb=
"set guioptions-=m
"set guioptions-=T
"set guioptions+=c

" }}}

