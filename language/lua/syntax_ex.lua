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

