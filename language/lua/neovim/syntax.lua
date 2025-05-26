print(vim.tbl_deep_extend("force", { "good", "2" }, { "bad" }))
print(vim.tbl_deep_extend("force", { "good", "2", "3" }, { "bad", "XX" }))
-- it is not recursive for pure nesetd list
print(vim.tbl_deep_extend("force", { opts = { "good", "2", "3" } }, { opts = { "bad", "XX" } }))
-- the when it becomes dict, part of the list can also be merged
print(vim.tbl_deep_extend("force", { opts = { "good", "2", "3", b = 10 } }, { opts = { "bad", "XX", a = 3 } }))
print(vim.tbl_deep_extend("force", { opts = { "good", "2", "3" } }, { opts = { "bad", { "XX" } } }))
print(vim.tbl_deep_extend("force", { opts = { { "good" }, { "2" } } }, { opts = { { "XX" } } }))
