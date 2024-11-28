local function add_virtual_lines_for_testing()
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
end
add_virtual_lines_for_testing()


-- TODO: get the position of current cursor related to current visible window
-- It is not solved now. I use a work-around pop the window relative to cursor

-- Get the current window ID
local win = vim.api.nvim_get_current_win()
-- Get the cursor position in the window
local cursor_pos = vim.api.nvim_win_get_cursor(win)
print("Cursor position in the window:", cursor_pos[1], cursor_pos[2])
-- Get the window's top-left corner position
local win_pos = vim.api.nvim_win_get_position(win)
-- Calculate the cursor's position relative to the window's display
local relative_line = cursor_pos[1] - win_pos[1] + 1 -- Adjust for 1-based index
local relative_col = cursor_pos[2] - win_pos[2]
print("Cursor position relative to window display:")
print("Line:", relative_line, "Column:", relative_col)
print("Win Pos:", win_pos[1], win_pos[2])
