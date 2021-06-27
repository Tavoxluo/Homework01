
cmake_minimum_required(VERSION 3.16)
project(webserver)

set(CMAKE_CXX_STANDARD 17)
set(var SRC)
file(GLOB_RECURSE SRC src/*.cpp)
add_executable(webserver ${SRC})
target_link_libraries(webserver pthread)
