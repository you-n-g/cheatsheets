vim.api.nvim_set_option_value("winbar", "test", {win=vim.api.nvim_get_current_win()})

-- Function to add inline virtual text
local function add_inline_virtual_text(bufnr, line, col, text, hl_group)
    vim.api.nvim_buf_set_extmark(bufnr, vim.api.nvim_create_namespace('inline_virtual_text'), line, col, {
        virt_text = {{text, hl_group}},
        -- virt_text_pos = 'eol', -- Position at the end of the line
        -- virt_text_pos = 'overlay',
        -- virt_text_pos = 'right_align',
        virt_text_pos = 'inline',
    })
end

-- Example usage
local bufnr = vim.api.nvim_get_current_buf()
local line = 0 -- Line number (0-indexed)
local col = 10 -- Column number (0-indexed)
local text = "Inline Virtual Text"
local hl_group = "Comment" -- Highlight group

add_inline_virtual_text(bufnr, line, col, text, hl_group)



-- Create a namespace for your extmarks
local ns_id = vim.api.nvim_create_namespace("my_virtual_lines")
-- Get the current buffer
local buf = vim.api.nvim_get_current_buf()
-- Define the virtual lines you want to add
local virt_lines = {
  {
    {"          This is a ", "Comment"},  -- Text with "Comment" highlight group
    {"virtual ", "String"},               -- Text with "String" highlight group
    {"line", "Function"}                  -- Text with "Function" highlight group
  },
  {
    {"          Another ", "Keyword"},    -- Text with "Keyword" highlight group
    {"virtual line", "Type"}              -- Text with "Type" highlight group
  }
}
-- Set the extmark with virtual lines
vim.api.nvim_buf_set_extmark(buf, ns_id, 20, 10, {
  virt_lines = virt_lines,
  virt_lines_above = true,  -- Place the virtual lines above the specified line
})
-- You can also set virt_lines_above to false to place them below

vim.api.nvim_buf_clear_namespace(0, -1, 0, -1)

local function create_hover_window(contents, duration)
  -- Get the current cursor position
  local row, col = unpack(vim.api.nvim_win_get_cursor(0))
  -- Create a new buffer for the floating window
  local buf = vim.api.nvim_create_buf(false, true)
  -- Set the contents of the buffer
  vim.api.nvim_buf_set_lines(buf, 0, -1, false, contents)
  -- Calculate the width and height of the floating window
  local width = 40
  local height = #contents
  -- Calculate the position of the floating window
  local opts = {
    relative = 'cursor',
    row = 1,
    col = 0,
    width = width,
    height = height,
    style = 'minimal',
    border = 'rounded',
  }
  -- Create the floating window
  local win = vim.api.nvim_open_win(buf, false, opts)
  -- Set the winbar for the floating window
  vim.api.nvim_set_option_value("winbar", "Hover Window", {win=win})
  -- Set up a timer to close the window after the specified duration
  vim.defer_fn(function()
    vim.api.nvim_win_close(win, true)
  end, duration)
end
local function show_hover()
  -- Define the contents to display in the hover window
  local contents = {
    "This is a custom hover window.",
    "You can display any information here.",
    "Line 3: More information.",
    "Line 4: Even more information.",
  }
  -- Create the hover window with the specified contents and duration (e.g., 3000 ms)
  create_hover_window(contents, 3000)
end
-- Map the hover function to a key (e.g., K)
-- vim.api.nvim_set_keymap('n', 'K', '<cmd>lua show_hover()<CR>', { noremap = true, silent = true })
show_hover()


vim.api.nvim_buf_add_highlight(vim.api.nvim_get_current_buf(), -1, 'Visual', 10, 0, -1)
