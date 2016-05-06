

# 读取或修改环境变量
set(ENV{PATH} "/path/to/foo:$ENV{PATH}")


# 输出当前可执行的变量
# http://stackoverflow.com/questions/9298278/cmake-print-out-all-accessible-variables-in-a-script

# 方法1) 但是这个方法 不会输出所有变量
cmake -LAH

# 方法2)
get_cmake_property(_variableNames VARIABLES)
foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
endforeach()
