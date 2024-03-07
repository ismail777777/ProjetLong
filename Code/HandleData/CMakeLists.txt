cmake_minimum_required(VERSION 3.5)
project(ASTConsumer)


find_package(LLVM REQUIRED CONFIG)
find_package(Clang REQUIRED CONFIG)

include_directories(${LLVM_INCLUDE_DIRS} ${CLANG_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 17)

add_executable(ASTConsumer src/CommentCapturer.cpp)
target_link_libraries(ASTConsumer
    LLVM
    clangTooling
    clangBasic
    clangASTMatchers
)
