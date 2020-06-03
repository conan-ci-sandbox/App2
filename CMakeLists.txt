cmake_minimum_required(VERSION 3.0.2)
project(conan-ci-sandbox)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

set(SOURCES src/main.cpp)

add_executable(App2 ${SOURCES})
target_link_libraries(App2 PRIVATE CONAN_PKG::libC)

install(TARGETS App2
        RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/bin
        LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
        ARCHIVE DESTINATION ${CMAKE_INSTALL_PREFIX}/lib)

