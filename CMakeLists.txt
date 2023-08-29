cmake_minimum_required(VERSION 3.14)
project(gtest_demo)

message("--- The demo need googletest and jsoncpp libraries ---")

# GoogleTest requires at least C++11
set(CMAKE_CXX_STANDARD 11)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
)

set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)


find_package(PkgConfig REQUIRED)
pkg_check_modules(JSONCPP jsoncpp)
include_directories("${JSONCPP_INCLUDE_DIRS}")
link_libraries(${JSONCPP_LIBRARIES})

include_directories(/usr/local/include)
link_directories(/usr/local/lib)

enable_testing()

add_executable(
  gtest_demo
  example/test_case_builder.h
  example/test_case_builder.cpp
  example/smart_ptr_test.cpp
)
target_link_libraries(
  gtest_demo
  gtest_main
  jsoncpp
)

include(GoogleTest)
gtest_discover_tests(gtest_demo)

add_subdirectory(doc)