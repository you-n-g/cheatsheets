-- 基本的原理
local B = {}

local A = { a = 123, __call = function() print("I'm in!!!") end }

-- this will not work, only setmetatable can support magic method
print(pcall(A))
setmetatable(A, {
  __call = function(...)
    print(vim.inspect({ ... }))
    return ("I'm in!!!")
  end
})
print(pcall(A))
print(vim.inspect(A))

-- wrong way to set parent class
setmetatable(B, A) -- `setmetatable` is a built-in function that sets the metatable of a given table.
print(vim.inspect(B))
print(B.a)         --  this will not work

-- right way to set parent class
-- setmetatable(B, { __index = A, __call = function() return("I'm in!!!") end })
setmetatable(B, { __index = A, __call = getmetatable(A).__call })
print(vim.inspect(B))
print(B.a) -- it only works when __index is set
print(pcall(B))

setmetatable(B, { __index = A })
print(vim.inspect(B))
-- - the magic methods can't be inherited simply by __index
print(pcall(B))

-- Logically, index can be inherited recursively. So normal attributes can inherit recursively.
local C = {}
setmetatable(C, { __index = B })
print(vim.inspect(C))
print(C.a)


-- class的实验
-- - 来自 https://zhuanlan.zhihu.com/p/123971515

-- 声明一个 lua class
-- className 是类名
-- super 为父类
local function class(className, super)
  -- 构建类
  local clazz = { __cname = className, super = super }
  local mt = {
    __call = function(cls, ...)
      -- local instance = {}
      -- 设置对象的元表为当前类，这样，对象就可以调用当前类生命的方法了
      local self = setmetatable({}, { __index = cls })
      if cls.ctor then
        cls.ctor(self, ...)
      end
      return self
    end
  }
  if super then
    -- 设置类的元表，此类中没有的，可以查找父类是否含有
    mt.__index = super
  end
  setmetatable(clazz, mt)
  return clazz
end


local A = class("A")
A.a = "A[a]: a class attribute"
A.b = "A[b]: a class attribute"
A.c = "A[c]: a class attribute"


function A:ctor(a, b)
  self.a = a
  self.b = b
  -- NOTE: you don't have to return anything. It is better than other implementations
end

function A:print()
  print(self.a)
  print(self.b)
  return self.a .. self.b
end

local a = A(10)
print(a.a)
print(a.b)
print(a.print)
print(a:print()) -- NOTE: 这里的调用方式，和python的不一样，Python是 a.print();  lua是 a:print().  用:才相当于Python的self传到第一个参数


function A:test_self()
  print(self)
end


local B = class("B", A)
B.b = "B[b]: a class attribute"

local b = B(20)
print(b.a)
print(b.b)
print(b.c)
print(b.print)
-- manually bind the method
print(b.print(b))
-- auto bind the method
print(b:print())


-- NOTE: Please note the right way to call the super class method
function B:test_self()
  -- print(self.super:test_self()) -- NOTE: this will result in changing `self` to the super class
  -- print(self.super.test_self(self))  -- this is also not the right way to call super
  -- Because when self come from a descendant class deeper than level 3, the `super` will be the `super` class in that level
  print(B.super.test_self(self))  -- this is the right way call super!!!
  print(self)
end

b = B(30)
b.test_self(b)

function B:ctor(a, b, c)
  self.super:ctor(a, b) -- a wrong demo to call super class ctor
  self.c = c
end
print(A)
b = B(10, 20, 30)
-- NOTE:  !!! this will result in a extream weird result. it apply super.ctor to super class instead of current instance.
print(A)

