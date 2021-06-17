cmake_minimum_required(VERSION 2.8)
project(instant_messaging_utility)

IF(NOT CMAKE_BUILD_TYPE)
	SET(CMAKE_BUILD_TYPE Release)
ENDIF()

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

include_directories(
${PROJECT_SOURCE_DIR}/include
)

add_executable(chatroom_server src/Server.cpp src/ServerMain.cpp)
add_executable(chatroom_client src/Client.cpp src/ClientMain.cpp)



