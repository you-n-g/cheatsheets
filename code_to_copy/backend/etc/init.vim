call plug#begin('~/.vim/plugged')

Plug 'scrooloose/nerdtree'
Plug 'majutsushi/tagbar'
Plug 'fatih/vim-go'
Plug 'tomtom/tcomment_vim'
" Plug 'ycm-core/YouCompleteMe', { 'do': './install.py' }
" Plug 'rdnetto/YCM-Generator'
Plug 'nvie/vim-flake8'
Plug 'jpalardy/vim-slime'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'heavenshell/vim-pydocstring'
Plug 'tell-k/vim-autopep8'
Plug 'python-mode/python-mode', {'branch': 'develop'}
Plug 'tpope/vim-surround'
Plug 'dhruvasagar/vim-table-mode'
Plug 'mileszs/ack.vim'
Plug 'morhetz/gruvbox'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'nathanaelkane/vim-indent-guides'

" 这里需要依赖 https://github.com/ryanoasis/nerd-fonts, 需要在本地安装字体
Plug 'ryanoasis/vim-devicons'
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
Plug 'mhinz/vim-startify'
Plug 'vim-ctrlspace/vim-ctrlspace'
Plug 'liuchengxu/vim-which-key'

" Plug 'wellle/tmux-complete.vim'  #
" 好是好，但是我tmux窗口太多了，会引起性能问题

call plug#end()


" settings -------------------------

set ai "auto indent
set expandtab
set tabstop=4
set shiftwidth=4
autocmd FileType c,cpp setlocal shiftwidth=2 tabstop=2
set number
set relativenumber
set scrolloff=10 " always keep 10 lines visible.
set ignorecase
set smartcase

" to automatically load the `.nvimrc`
set exrc
set secure
" examples to ignore
" ignore a directory on top level
" let g:NERDTreeIgnore += ['^models$']
" let g:ctrlp_custom_ignore = {
"   \ 'dir':  '\vmodels$',
"   \ }
" list.source.grep.excludePatterns 实在是不会用,  所以workaround方法如下
" 就是把那些大文件放到别的地方再Link过来，默认coclist grep不会follow link



" Go to the last cursor location when a file is opened, unless this is a
" git commit (in which case it's annoying)
au BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") && &filetype != "gitcommit" |
        \ execute("normal `\"") |
    \ endif
" https://stackoverflow.com/a/774599
" 如果不行一般是因为权限问题: sudo chown user: ~/.viminfo


" highlight current line
set cursorline


" Buffer related
" :bd XXX 可以关闭buffer, 关闭buffer，
" c+^ 是可以在最近的两个buffer之间切换的
nnoremap gb :ls<CR>:b<Space>



let g:gruvbox_contrast_dark="hard"
" let g:gruvbox_contrast_dark="soft"
set background=dark
colorscheme gruvbox

map <F9>p :call CompilePython()<cr>
func! CompilePython()
    exec "w"
    exec "!echo -e '\033[1;34m-----------here\ is\ the\ ans\ of\ %----------\033[0m';python \"%\""
endfunc

map <F9>s :call RunShell()<cr>
func! RunShell()
    exec "w"
    exec "!echo -e '\033[1;34m-----------here\ is\ the\ ans\ of\ %----------\033[0m';bash \"%\""
endfunc

map <F9>c :call CompileRunCpp()<CR>
func! CompileRunCpp()
    exec "w"
    exec "!echo -e '\033[1;32mcompiling.....\033[0m';g++ -std=c++11 \"%\" -o \"%:r.exe\";echo -e '\033[1;34m-----------here_is_the_ans_of_%----------\033[0m';./\"%:r.exe\";echo -e '\033[1;33mend...\033[0m';rm \"%:r.exe\""
    "exec "!./%:r.exe"
endfunc

map <F9>j :call CompileRunJava()<CR>
func! CompileRunJava()
    exec "w"
    exec "!echo -e '\033[1;32mcompiling.....\033[0m';javac %;echo -e '\033[1;34m-----------here_is_the_ans_of_%----------\033[0m';java %:r;echo -e '\033[1;33mend...\033[0m';rm %:r.class"
endfunc

map <F9>g :call CompileRunGo()<CR>
func! CompileRunGo()
    exec "w"
    exec "!go run %"
endfunc

nnoremap <F11> :set spell!<CR>




"
" The plugins I always need -------------------------
" https://github.com/neovim/neovim/wiki/Related-projects#plugins
"


"
" ctrlp.vim
" https://github.com/kien/ctrlp.vim
let g:ctrlp_working_path_mode = 'wa'



"
" vimwiki http://www.vim.org/scripts/script.php?script_id=2226
"
" map tb :VimwikiTable
map t<space> <Plug>VimwikiToggleListItem
let g:vimwiki_hl_headers = 1
" let g:vimwiki_conceallevel = 0


"
" Nerdtree http://www.vim.org/scripts/script.php?script_id=1658
"
nnoremap <silent> <F7> :NERDTreeToggle<CR>
let NERDTreeIgnore=['\.pyc$', '\.orig$', '\.pyo$']


"
" Tagbar http://www.vim.org/scripts/script.php?script_id=3465
"
" nnoremap <silent> <F8> :TlistToggle<CR>
nnoremap <silent> <F8> :TagbarToggle<CR>
let g:tagbar_sort = 0


"
" vim-flake8 , PyFlakes to find static programming errors and  PEP8 ...
"   git clone https://github.com/nvie/vim-flake8 ~/.vim/bundle/
"   sudo apt-get install python-flake8
let g:no_flake8_maps=1
" autocmd BufWritePost *.py call Flake8() " XXX 这个功能需要安装插件
autocmd FileType python map <buffer> <F12> :call Flake8()<CR>


"
" matchit http://www.vim.org/scripts/script.php?script_id=39
"



"
" vim-go
" https://github.com/fatih/vim-go
" 集成了绝大部分go的开发环境
" 依赖 GOPATH, GOROOT
" 查文档时不会在项目里查，因为不知道项目在哪里呀！
" 所以回去系统默认的函数库中(依赖GOROOT??) 和 GOPATH/src下查询，所以设置好gopath非常重要呀
"
" 有用的命令
" :GoImports 自动import缺失工具
" :GoCallers
" 这个可能有很多可能性，只会列出一种情况(TODO:想想原理是啥，以后别被这个坑才好)
" :GoImplements 找到interface的实现， 和 GoCallers 那几个命令都是依赖于
" oracle的， 但是还不知道怎么用 g:go_oracle_scope 这个参数, 用 下面这个成功过
" let g:go_oracle_scope = 'github.com/GoogleCloudPlatform/kubernetes/cmd/kubectl XXXX'
" 但是非常的慢
au FileType go nmap <Leader>gd <Plug>(go-doc)



"
" TComment
" https://github.com/tomtom/tcomment_vim
" gc 确定一切


"
" vim-slime
" https://github.com/jpalardy/vim-slime
" NOTICE: slime代表着一种边写脚本边搞bash的习惯！一种新的思维方式
" ":i.j" means the ith window, jth pane
" C-c, C-c  --- the same as slime
" C-c, v    --- mnemonic: "variables"
let g:slime_target = "tmux"
" 这个一定要和ipython一起用，否则可能出现换行出问题
let g:slime_python_ipython = 1



"
" vim-airline-themes
let g:airline_theme='dark'


"
" heavenshell/vim-pydocstring
nmap <silent> <C-N> <Plug>(pydocstring)



"
" python-mode
" 这个插件遇到过保存失败,导致运行脚本跑的不是最新代码！！！！
" help PymodeDoc
" this plugin will auto folder all the code, please use `:help zo` to find the code
let g:pymode_lint_ignore = ["E0100", "E501", "E402"]
" E402 module level import not at top of file
let g:pymode_doc=0  " This will conflict with coc
let g:pymode_rope=0  " disable refracting because I don't use it
let g:pymode_folding=0  " auto folding really makes python coding really slow.
" lint还是挺有用的，改完代码马上就能检查出一些语法错误，不必等到运行时发现
let g:pymode_lint_unmodified = 1  " Check code on every save (every)
" Set this to make wrap works
let g:pymode_options = 0





"
" vim-surround
" https://github.com/tpope/vim-surround
"




"
" bash-support
" https://www.tecmint.com/use-vim-as-bash-ide-using-bash-support-in-linux/
"

"
" mileszs/ack.vim
let g:ackprg = 'ag --vimgrep'
nnoremap <Leader>a :Ack




" BEGIN for coc ----------------------------------------------------------
" if hidden is not set, TextEdit might fail.
set hidden

" Some servers have issues with backup files, see #649
set nobackup
set nowritebackup

" Better display for messages
set cmdheight=2

" You will have bad experience for diagnostic messages when it's default 4000.
set updatetime=300

" don't give |ins-completion-menu| messages.
set shortmess+=c

" always show signcolumns
set signcolumn=yes

" disable python2 provider
let g:loaded_python_provider=0

" Use tab for trigger completion with characters ahead and navigate.
" Use command ':verbose imap <tab>' to make sure tab is not mapped by other plugin.
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

" Use <c-space> to trigger completion.
inoremap <silent><expr> <c-space> coc#refresh()

" Use <cr> to confirm completion, `<C-g>u` means break undo chain at current position.
" Coc only does snippet and additional edit on confirm.
inoremap <expr> <cr> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"

" Use `[c` and `]c` to navigate diagnostics
nmap <silent> [c <Plug>(coc-diagnostic-prev)
nmap <silent> ]c <Plug>(coc-diagnostic-next)

" Remap keys for gotos
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" Use K to show documentation in preview window
nnoremap <silent> K :call <SID>show_documentation()<CR>

function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  else
    call CocAction('doHover')
  endif
endfunction

" Highlight symbol under cursor on CursorHold
autocmd CursorHold * silent call CocActionAsync('highlight')

" Remap for rename current word
nmap <leader>rn <Plug>(coc-rename)

" Remap for format selected region
xmap <leader>f  <Plug>(coc-format-selected)
nmap <leader>f  <Plug>(coc-format-selected)

augroup mygroup
  autocmd!
  " Setup formatexpr specified filetype(s).
  autocmd FileType typescript,json setl formatexpr=CocAction('formatSelected')
  " Update signature help on jump placeholder
  autocmd User CocJumpPlaceholder call CocActionAsync('showSignatureHelp')
augroup end

" Remap for do codeAction of selected region, ex: `<leader>aap` for current paragraph
xmap <leader>a  <Plug>(coc-codeaction-selected)
nmap <leader>a  <Plug>(coc-codeaction-selected)

" Remap for do codeAction of current line
nmap <leader>ac  <Plug>(coc-codeaction)
" Fix autofix problem of current line
nmap <leader>qf  <Plug>(coc-fix-current)

" Use <tab> for select selections ranges, needs server support, like: coc-tsserver, coc-python
nmap <silent> <TAB> <Plug>(coc-range-select)
xmap <silent> <TAB> <Plug>(coc-range-select)
xmap <silent> <S-TAB> <Plug>(coc-range-select-backword)

" Use `:Format` to format current buffer
command! -nargs=0 Format :call CocAction('format')

" Use `:Fold` to fold current buffer
command! -nargs=? Fold :call     CocAction('fold', <f-args>)

" use `:OR` for organize import of current buffer
command! -nargs=0 OR   :call     CocAction('runCommand', 'editor.action.organizeImport')

" Add status line support, for integration with other plugin, checkout `:h coc-status`
set statusline^=%{coc#status()}%{get(b:,'coc_current_function','')}

" Using CocList
" Show all diagnostics
nnoremap <silent> <space>a  :<C-u>CocList diagnostics<cr>
" Manage extensions
nnoremap <silent> <space>e  :<C-u>CocList extensions<cr>
" Show commands
nnoremap <silent> <space>c  :<C-u>CocList commands<cr>

" ctags的默认参数是这个
" config/coc/extensions/node_modules/coc-python/resources/ctagOptions
" --extras参数出问题要么改参数成 extra，要么装能兼容版本的ctags deploy_apps/install_ctags.sh
" 如果太慢了，可以用 --verbose debug看看慢在哪里，可以在ctagOptions里面加上exclude
" 但是必须用恰好是文件夹名字，不然无法跳过,  --exclude=mlruns --exclude=models
" Find symbol of current document
nnoremap <silent> <space>o  :<C-u>CocList outline<cr>
" Search workspace symbols
nnoremap <silent> <space>s  :<C-u>CocList -I symbols<cr>

" Do default action for next item.
nnoremap <silent> <space>j  :<C-u>CocNext<CR>
" Do default action for previous item.
nnoremap <silent> <space>k  :<C-u>CocPrev<CR>
" Resume latest coc list
nnoremap <silent> <space>p  :<C-u>CocListResume<CR>

nnoremap <silent> <Leader>gc :exe 'CocList -I --input='.expand('<cword>').' grep'<CR>
nnoremap <silent> <Leader>gr :exe 'CocList -I grep'<CR>

let g:coc_global_extensions = [
 \ "coc-python",
 \ "coc-highlight",
 \ "coc-lists",
 \ "coc-json",
 \ ]

" 个人经验 <space>c  setLinter ，把pylama 设置成错误提示的工具方便

" DEBUG相关
" 当出现下面情况都先确认环境有没有弄错
" - 解析pylama解析包失败时(找不到包, 比如import时提示无法解析)
" - 做代码跳转时，提示版本太老
" <space>c -> python.setInterpreter 
" 如果上述命令出错了，很可能是python插件没有加载:  <space>e 来加载插件
" 会频繁出现上面问题的原因是它会因为新项目不知道default interpreter是什么
" - https://github.com/neoclide/coc-python/issues/55
"
" 如果出现运行特别慢的情况，那么可能是因为数据和代码存在一起了,
" 数据小文件特别多，建议把数据单独放到外面。不然得一个一个插件单独地配置XXX_ignore

" 各种配置通过这里来设置 
" 直接编辑 ~/.config/nvim/coc-settings.json 或者  CocConfig


" 好用的地方:  grep, gr; 看上面的定义，IDE常用的地方上面都有

" other cheetsheet
" deploy_apps/install_neovim.sh


" END   for coc ----------------------------------------------------------



" BEGIN for vim-indent-guides ----------------------------------------------------------
let g:indent_guides_enable_on_vim_startup = 1
let g:indent_guides_guide_size = 1
let g:indent_guides_start_level = 2
" END   for vim-indent-guides ----------------------------------------------------------


" 'vim-ctrlspace/vim-ctrlspace'
set nocompatible
set hidden
set encoding=utf-8
hi link CtrlSpaceNormal   PMenu
hi link CtrlSpaceSelected PMenuSel
hi link CtrlSpaceSearch   Search
hi link CtrlSpaceStatus   StatusLine
" visual mode is not useful for me at all
nnoremap <silent>Q :CtrlSpace<CR>
set showtabline=0
" 好用的:  l可以快速列出所有的list


" Plug 'liuchengxu/vim-which-key'
" nnoremap <silent> <leader> :WhichKey '<Space>'<CR>
set timeoutlen=500 " By default timeoutlen is 1000 ms
let g:mapleader = "\<Space>"
let g:maplocalleader = ','
nnoremap <silent> <leader>      :<c-u>WhichKey '<Space>'<CR>
nnoremap <silent> <localleader> :<c-u>WhichKey  ','<CR>



" BEGIN for mhinz/vim-startify ----------------------------------------------------------
let g:ascii_yang = [
      \'____  ________________________  _____________   __________',
      \'__  |/ /___  _/__    |_  __ \ \/ /__    |__  | / /_  ____/',
      \'__    / __  / __  /| |  / / /_  /__  /| |_   |/ /_  / __  ',
      \'_    | __/ /  _  ___ / /_/ /_  / _  ___ |  /|  / / /_/ /  ',
      \'/_/|_| /___/  /_/  |_\____/ /_/  /_/  |_/_/ |_/  \____/   ',
      \]

 let g:ascii_art = [
       \'                           O                                         ',
       \'                                 O           O O                     ',
       \'                                       O     |_|                     ',
       \'                                           <(+ +)>                   ',
       \'                                            ( u )                    ',
       \'                                               \\                    ',
       \'                                                \\                   ',
       \'                                                 \\               )  ',
       \'                                                  \\             /   ',
       \'                                                   \\___________/    ',
       \'                                                   /|          /|    ',
       \'                                                  //||      ( /||    ',
       \'                                                 // ||______//_||    ',
       \'                                                //  ||     // W||    ',
       \'                                               //   ||    //   ||    ',
       \'                                               \\   ||    \\   ||    ',
       \'                                                \\  ||     \\  ||    ',
       \'                                                //  ||     //  ||    ',
       \'                                               /_\ /__\   /_\ /__\   ',
       \]

 let g:startify_custom_header =
       \ 'startify#pad(g:ascii_yang + startify#fortune#boxed() + g:ascii_art)'
" END   for mhinz/vim-startify ----------------------------------------------------------




" Nvim usage cheetsheet


" 目录
" - 设计理念
" - 查看当前设置
" - 坑


" ========== 设计理念 ==========
" buffer, window, tab的设计理念
" A buffer is the in-memory text of a file
" A window is a viewport on a buffer.
" A tab page is a collection of windows.


" ========== 查看当前设置 ==========
" global settings
" 检查按键到底被映射成什么了
" :verbose nmap <CR>


" ========== 坑 ==========
" terminal mode 可以解决终端乱码的问题， 还可以用  <c-\><c-n> 和 i 在normal
" model 和terminal model之间切换
