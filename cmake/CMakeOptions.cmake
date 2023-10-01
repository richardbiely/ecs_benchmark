# Config options ###
include(CMakeDependentOption)
include(CheckCXXCompilerFlag)

option(ENABLE_STATIC_ANALYZER "Enable Static analyzer" OFF)
option(ENABLE_STATIC_ANALYZER_INCLUDE_WHAT_YOU_USE "Enable Static analyzer for include-what-you-use" OFF)
option(ENABLE_TESTING "Enable the tests" ${PROJECT_IS_TOP_LEVEL})
if(CMAKE_CXX_COMPILER_ID MATCHES ".*Clang.*")
  option(ENABLE_TIME_TRACE "enable (clang) -ftime-trace flag" OFF)
endif()
if(ENABLE_TESTING)
  list(APPEND VCPKG_MANIFEST_FEATURES "tests")
endif()

option(ENABLE_BENCHMARKS "Enable Benchmark" ON)

if(NOT PROJECT_IS_TOP_LEVEL OR OPT_PACKAGING_MAINTAINER_MODE)
  option(OPT_ENABLE_IPO "Enable IPO/LTO" OFF)
  option(OPT_WARNINGS_AS_ERRORS "Treat Warnings As Errors" OFF)
  option(OPT_ENABLE_SANITIZER_ADDRESS "Enable address sanitizer" OFF)
  option(OPT_ENABLE_SANITIZER_UNDEFINED "Enable undefined sanitizer" OFF)
  option(OPT_ENABLE_SANITIZER_THREAD "Enable thread sanitizer" OFF)
  option(OPT_ENABLE_SANITIZER_MEMORY "Enable memory sanitizer" OFF)
  option(OPT_ENABLE_UNITY_BUILD "Enable unity builds" OFF)
  option(OPT_ENABLE_CLANG_TIDY "Enable clang-tidy" OFF)
  option(OPT_ENABLE_CPPCHECK "Enable cpp-check analysis" OFF)
  option(OPT_ENABLE_PCH "Enable precompiled headers" OFF)
  option(OPT_ENABLE_CACHE "Enable ccache" OFF)
  option(OPT_ENABLE_HARDENING "Enable hardening" OFF)
  option(OPT_ENABLE_COVERAGE "Enable Testing coverage" OFF)
else()
  option(OPT_ENABLE_IPO "Enable IPO/LTO" ON)
  option(OPT_WARNINGS_AS_ERRORS "Treat Warnings As Errors" OFF)

  if(ENABLE_TESTING AND (CMAKE_BUILD_TYPE MATCHES Debug OR CMAKE_BUILD_TYPE MATCHES RelWithDebInfo))
    set(DEFAULT_OPT_ENABLE_SANITIZER_ADDRESS ON)
  else()
    set(DEFAULT_OPT_ENABLE_SANITIZER_ADDRESS OFF)
  endif()
  option(OPT_ENABLE_SANITIZER_ADDRESS "Enable address sanitizer" ${DEFAULT_OPT_ENABLE_SANITIZER_ADDRESS})

  if(ENABLE_TESTING AND (CMAKE_BUILD_TYPE MATCHES Debug OR CMAKE_BUILD_TYPE MATCHES RelWithDebInfo))
    if(NOT MSVC)
      set(DEFAULT_OPT_ENABLE_SANITIZER_UNDEFINED ON)
    else()
      set(DEFAULT_OPT_ENABLE_SANITIZER_UNDEFINED OFF)
    endif()
  else()
    set(DEFAULT_OPT_ENABLE_SANITIZER_UNDEFINED OFF)
  endif()
  option(OPT_ENABLE_SANITIZER_UNDEFINED "Enable undefined sanitizer" ${DEFAULT_OPT_ENABLE_SANITIZER_UNDEFINED})
  option(OPT_ENABLE_SANITIZER_THREAD "Enable thread sanitizer" OFF)
  option(OPT_ENABLE_SANITIZER_MEMORY "Enable memory sanitizer" OFF)

  option(OPT_ENABLE_UNITY_BUILD "Enable unity builds" OFF)
  cmake_dependent_option(OPT_ENABLE_CLANG_TIDY "Enable clang-tidy" ON ENABLE_STATIC_ANALYZER OFF)
  cmake_dependent_option(OPT_ENABLE_CPPCHECK "Enable cpp-check analysis" ON ENABLE_STATIC_ANALYZER OFF)
  option(OPT_ENABLE_PCH "Enable precompiled headers" OFF)
  option(OPT_ENABLE_CACHE "Enable ccache" ON)
  option(OPT_ENABLE_HARDENING "Enable hardening" OFF)

  if(CMAKE_BUILD_TYPE MATCHES Debug OR CMAKE_BUILD_TYPE MATCHES RelWithDebInfo)
    set(DEFAULT_OPT_ENABLE_COVERAGE ON)
  else()
    set(DEFAULT_OPT_ENABLE_COVERAGE OFF)
  endif()
  cmake_dependent_option(OPT_ENABLE_COVERAGE "Enable Testing coverage" ${DEFAULT_OPT_ENABLE_COVERAGE} ENABLE_TESTING OFF)
endif()

# option(ENABLE_FUZZING "Enable Fuzzing Builds" ${ENABLE_DEVELOPER_MODE})
include(cmake/LibFuzzer.cmake)
check_libfuzzer_support(LIBFUZZER_SUPPORTED)
if(LIBFUZZER_SUPPORTED
   AND (OPT_ENABLE_SANITIZER_ADDRESS
        OR OPT_ENABLE_SANITIZER_THREAD
        OR OPT_ENABLE_SANITIZER_UNDEFINED))
  set(DEFAULT_ENABLE_FUZZING ON)
else()
  set(DEFAULT_ENABLE_FUZZING OFF)
endif()
option(ENABLE_FUZZING "Enable Fuzzing Builds" ${DEFAULT_ENABLE_FUZZING})
