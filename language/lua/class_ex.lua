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
