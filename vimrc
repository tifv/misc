set tabstop=8
set shiftwidth=4
set softtabstop=-1
set expandtab
set smarttab
set autoindent

set backspace=indent,eol,start

syntax on
autocmd FileType plaintex set filetype=tex
set modeline

set hlsearch
set incsearch
set showmatch
set gdefault

set showcmd
set ruler

set switchbuf=useopen,split
set hidden

set history=1000
set wildmode=list:longest

set exrc

set swapsync=

"function LaTeX()
"  let l:fname = bufname("")
"  let l:len = strlen(l:fname)
"  if (match(l:fname, "/") != -1) || (strpart(l:fname, l:len-3, l:len) == "sty")
"    return
"  endif
"  let l:swap = &makeprg
"  set makeprg=latex\ -file-line-error\ -halt-on-error
"  execute "make %"
"  execute "set makeprg=" . l:swap
"  execute "!dvipdf %:r.dvi"
"endfunction
"
"command LaTeX call LaTeX()
"autocmd FileType tex nmap <F11> :wa<CR>:LaTeX<CR>
"autocmd FileType tex imap <F11> <C-O>:wa<CR><C-O>:LaTeX<CR>

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

nmap <F8> :call Comment()<CR><Down>
imap <F8> <C-O>:call Comment()<CR><Down>
vmap <F8> :call Comment()<CR>

nmap <F9> :call UnComment()<CR><Down>
imap <F9> <C-O>:call UnComment()<CR><Down>
vmap <F9> :call UnComment()<CR>

imap <F7> <C-O>:vertical resize 80<CR>
nmap <F7> :vertical resize 80<CR>

autocmd FileType vim let b:comment_sign = '"'
autocmd FileType make,python,yaml,conf,sh let b:comment_sign = '#'
autocmd FileType tex,plaintex,mp,mf let b:comment_sign = "%"
autocmd FileType haskell let b:comment_sign = "--"
autocmd FileType pure,asy let b:comment_sign = "//"

autocmd FileType yaml setlocal shiftwidth=2

set mouse=a

set fencs=utf-8,cp1251

let python_highlight_all=1

set viminfo='300,<50,s10,h,r/media

autocmd BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

set langmap=
    \ЙЦУКЕНГШЩЗ;QWERTYUIOP,
    \йцукенгшщз;qwertyuiop,
    \ФЫВАПРОЛД;ASDFGHJKL,
    \фывапролд;asdfghjkl,
    \ЯЧСМИТЬ;ZXCVBNM,
    \ячсмить;zxcvbnm,
    \ХЪЖЭБЮ;{}:\"<>,хъжэю;[];'.,ё`,Ё~

let s:latexspaceerror = "" .
    \'-\@4<!\<\(' .
        \'[Аа]\|[Ии]\|[Вв]\|[Кк]\|[Сс]\|[Уу]\|[Оо]\|' .
        \'[Ии]з\|[Оо][тб]\|[ДдПпСсВвт]о\|[Зз]а\|[Нн][аеоиу]\|[Кк]о\|' .
    \'\)\zs\( \|\n\)\ze' .
\'\|' .
    \'\zs\( \|\n\)\ze---' .
\'\|' .
    \'\zs\( \|\n\)\ze\(ли\|же\|бы\)\>'

function HighlighLaTeXSpaceErrors()
    highlight latexspaceerror ctermbg=lightmagenta guibg=lightmagenta
    execute "match latexspaceerror /" . s:latexspaceerror . "/"
endfunction

function SubstituteLaTeXSpaceErrors() range
    execute (a:firstline) . "," . (a:lastline) .
        \"substitute/" . s:latexspaceerror . '/\~/ce'
endfunction

" This is going to .gvimrc
"set guifont=Monospace\ 11
"set vb t_vb=
"set guioptions-=m
"set guioptions-=T
"set guioptions+=c

