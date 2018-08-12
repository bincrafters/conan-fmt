project(test_ranges CXX)
cmake_minimum_required(VERSION 2.8.12)

add_executable(${PROJECT_NAME} test_ranges.cpp)
target_link_libraries(${PROJECT_NAME} CONAN_PKG::fmt)
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 11)

if (FMT_HEADER_ONLY)
    target_compile_definitions(${PROJECT_NAME} PRIVATE FMT_HEADER_ONLY=1)
endif(FMT_HEADER_ONLY)
