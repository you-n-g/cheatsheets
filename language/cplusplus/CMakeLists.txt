


# ------------------------------------------ 编写CMakeLists.txt ------------------------------------------

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




# 设置配置文件, 后者是对前者的转义后的解释
configure_file ("${PROJECT_SOURCE_DIR}/TutorialConfig.h.in" "${PROJECT_BINARY_DIR}/TutorialConfig.h")


 # 保证里面 .h文件可以被include进来, 这个在主CMakelists.txt里加了， 在其他的子目录就不用加了; 但是如果只是是在子目录里加了，在其他子目录里不会生效
include_directories ("${PROJECT_SOURCE_DIR}/MathFunctions")


# 加子目录:
add_subdirectory (MathFunctions)  # 这样子目录下的 CMakeLists.txt就会被执行



# 定义编译出来的结果
add_library(MathFunctions libsource.cxx)  # 根据libsource.cxx编译生成MathFunctions这个库
add_executable (executable source.cxx)  # 根据source.cxx编译生成 executable
target_link_libraries (executable MathFunctions)  # 编译executable的时候把 MathFunctions也链接进去


# 定义如何安装
install (TARGETS MathFunctions DESTINATION bin)  # 定义这些targets要安装到bin里
install (FILES MathFunctions.h DESTINATION include)  # 定义这些文件要安装到include里
if (UNIX)
    install(CODE "execute_process(COMMAND ldconfig)")  # 安装后自动运行 ldconfig
endif()


# introspection
include (${CMAKE_ROOT}/Modules/CheckFunctionExists.cmake)
check_function_exists (log HAVE_LOG)  # 查看系统中是否有Log这个函数, 有则定义相应的macro


# reference
# https://cmake.org/cmake-tutorial/



# ------------------------------------------ 使用CMakeLists.txt ------------------------------------------
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
