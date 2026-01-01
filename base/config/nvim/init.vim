set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc

call plug#begin('~/.vim/plugged')

" Rust setup
" Use tag v2.3.0 with nvim <= 0.10
Plug 'neovim/nvim-lspconfig'
Plug 'simrat39/rust-tools.nvim'
Plug 'hrsh7th/nvim-cmp'
Plug 'hrsh7th/cmp-nvim-lsp'
Plug 'hrsh7th/cmp-nvim-lsp-signature-help'
Plug 'hrsh7th/cmp-path'
Plug 'hrsh7th/vim-vsnip'


" Ledger
let g:ledger_is_hledger=v:false
Plug 'ledger/vim-ledger'

call plug#end()

" Rust configuration
source ~/.config/nvim/rust.vim
