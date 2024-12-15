--TOOD:
-- insert current path to path, so that we can require to import
print(package.path)

-- print(debug.getinfo(1, "S").source:sub(2))
-- local current_path = debug.getinfo(1, "S").source:sub(2):match("(.*/)")
-- print(current_path) -- this will not work lua

local current_path = "/home/xiaoyang/cheatsheets/language/lua/"

if not string.find(package.path, current_path, 1, true) then
    package.path = package.path .. ";" .. current_path .. "?.lua"
end

local mod = require"test_require.mod"
print("Object id of mod:", tostring(mod))
local mod2 = require"test_require/mod"
print("Object id of mod2:", tostring(mod2))
print(tostring(mod) == tostring(mod2))  -- Amazing, it does not point to the same object
