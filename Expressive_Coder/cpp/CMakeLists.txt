cmake_minimum_required(VERSION 3.16)
project(expressive_coder_primitives LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(test_primitives tests/test_primitives.cpp)
target_include_directories(test_primitives PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)

enable_testing()
add_test(NAME expressive_coder_primitives COMMAND test_primitives)
