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

local function g(x)
	print(x)
end
g(1, 2, 3, 4) -- you can always pass more parameters in lua. It only handle the first one. This helps understanding of following cases.

local x = { "good2", "bad2" }
P({unpack(x, 3, #x)}) -- it will correctly return a nil
P({unpack(x, 1, -1)}) -- it will return nothing. -1 is not recognized
P(type(table.unpack(x, 1, #x))) -- you will get string here
P(type(table.unpack(x, 2, #x))) -- you will get string here
P(type({ table.unpack(x, 1, #x) })) -- it is table
P(type({ table.unpack(x, 2, #x) })) -- it is table

P(type(table.unpack(x, 3, #x))) -- you will get string here


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


local x = {a=3}
require"snacks".debug(x)
print(x['a'])  -- equals to contains
x.a = nil  -- this will remove the key instead of setting it into nil.
require"snacks".debug(x)
print(x['a'])  -- equals to contains

