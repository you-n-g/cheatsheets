-- Motivation of the file
-- We only include basic syntax blocks in this file.
-- Knowledge about implementing more advanced mechanism(e.g. class), we should implement in other files.

-- # Syntax Suger
--
-- ## table assignment
-- Because the following code does not work.
-- local t = {
-- 	"a.b" = 3,
-- 	a.c = 3,
-- }

local t = {
	["a.b"] = 3,
}
print(t)


-- ## strings
local str0 = "%1what is the fuck \t"  -- this can't be linebreaks
print(str0)

-- [=[ have higher level. So string like [[]] can be embeded.
local str1 = [=[%1what is [[]]
the fuck \t]=]
print(str1)

-- [[]] can't be placed inside the string
local str2 = [[%1what is
the fuck \t]]
print(str2)


-- `...`  usage
local function f(...)
  for _, v in ipairs({...}) do
    print(v)
  end
  print(select("#", ...))  -- the number of elements
  print(select(2, ...))  -- select the second element of
end

f("good", "bad")

local x = {"good2", "bad2"}
f(unpack(x))  -- we can similating passing each elemment to f with `unpack`

-- # most basic syntaxes
if false or nil then
  print("true")
else
  print("false")  -- only false or nil will go false false
end

if "" and 1 and 0 and 0.0 and true then
  print("true") -- even "" and 0 goes ture
else
  print("false")
end
