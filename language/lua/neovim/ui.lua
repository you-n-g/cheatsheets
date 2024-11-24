local Input = require("nui.input")
local event = require("nui.utils.autocmd").event

input = Input({
  position = "50%",
  size = {
    width = 20,
  },
  border = {
    style = "single",
    text = {
      top = "[Howdy?]",
      top_align = "center",
    },
  },
  win_options = {
    winhighlight = "Normal:Normal,FloatBorder:Normal",
  },
}, {
  prompt = "> ",
  default_value = "Hello",
  on_close = function()
    print("Input Closed!")
  end,
  on_submit = function(value)
    print("Input Submitted: " .. value)
  end,
})

-- mount/open the component
input:mount()
input:unmount()

-- Actively exit the window will 


input:hide()

input:show()

-- -- unmount component when cursor leaves buffer
-- input:on(event.BufLeave, function()
--   input:unmount()
-- end)
