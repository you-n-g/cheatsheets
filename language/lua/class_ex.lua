-- 基本的原理
local t = {}

local mt = { a = 123 }
setmetatable(t, mt)
print(vim.inspect(t))
print(t.a) --  this will not work


local mt2 = { __index = { a = 123 } }
setmetatable(t, mt2)
print(vim.inspect(t))
print(t.a) -- it only works when __index is set

vim.inspect(t)


-- class的实验
-- - 来自 https://zhuanlan.zhihu.com/p/123971515

-- 声明一个 lua class
-- className 是类名
-- super 为父类
local function class(className, super)
    -- 构建类
    local clazz = { __cname = className, super = super }
    if super then
        -- 设置类的元表，此类中没有的，可以查找父类是否含有
        setmetatable(clazz, { __index = super })
    end
    -- new 方法创建类对象
    clazz.new = function(...)
        -- 构造一个对象
        -- local instance = {}
        -- 设置对象的元表为当前类，这样，对象就可以调用当前类生命的方法了
        local self = setmetatable({}, { __index = clazz })
        if clazz.ctor then
            clazz.ctor(self, ...)
        end
        return self
    end
    return clazz
end


local A = class("A")
A.b = "[b]: a class attribute"
A.a = "[a]: a class attribute"


function A:ctor(a, b)
    self.a = a
    self.b = b
end

function A:print()
    print(self.a)
    print(self.b)
end

local a = A.new(10)
print(a.a)
print(a.b)
a:print()   -- NOTE: 这里的调用方式，和python的不一样，Python是 a.print();  lua是 a:print().  用:才相当于Python的self传到第一个参数

local B = class("B", A)

local b = B.new(20)
print(b.a)
print(b.b)


