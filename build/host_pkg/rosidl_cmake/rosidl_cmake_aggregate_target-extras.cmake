# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target host_pkg::host_pkg
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${host_pkg_TARGETS}.
if(host_pkg_TARGETS AND NOT TARGET host_pkg::host_pkg)
  add_library(host_pkg::host_pkg INTERFACE IMPORTED)
  set_target_properties(host_pkg::host_pkg PROPERTIES
    INTERFACE_LINK_LIBRARIES "${host_pkg_TARGETS}")
endif()
