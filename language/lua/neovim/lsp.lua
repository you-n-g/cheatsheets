-- Function to print diagnostics for the current buffer
local function print_diagnostics()
  local bufnr -- Just for triggering the LSP information.
  -- Get the current buffer number
  local bufnr = vim.api.nvim_get_current_buf()
  -- Retrieve diagnostics for the current buffer
  local diagnostics = vim.diagnostic.get(bufnr)
  -- Iterate over diagnostics and print them
  for _, diagnostic in ipairs(diagnostics) do
    print(string.format("Line %d: %s", diagnostic.lnum + 1, diagnostic.message))
  end
end
-- Call the function to print diagnostics
print_diagnostics()

-- Function to print diagnostics for a specific line
local function print_line_diagnostics(line)
  local bufnr = vim.api.nvim_get_current_buf()
  local diagnostics = vim.diagnostic.get(bufnr, { lnum = line })
  for _, diagnostic in ipairs(diagnostics) do
    print(string.format("Line %d: %s", diagnostic.lnum + 1, diagnostic.message))
  end
end
-- Example: Print diagnostics for line 10
print_line_diagnostics(9)  -- Note: Line numbers are 0-indexed internally
