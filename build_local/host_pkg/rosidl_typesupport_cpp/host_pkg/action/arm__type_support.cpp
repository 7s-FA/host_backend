// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from host_pkg:action/Arm.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "host_pkg/action/detail/arm__functions.h"
#include "host_pkg/action/detail/arm__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_Goal_type_support_ids_t;

static const _Arm_Goal_type_support_ids_t _Arm_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_Goal_type_support_symbol_names_t _Arm_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_Goal)),
  }
};

typedef struct _Arm_Goal_type_support_data_t
{
  void * data[2];
} _Arm_Goal_type_support_data_t;

static _Arm_Goal_type_support_data_t _Arm_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_Goal_message_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_Arm_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_Arm_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Arm_Goal_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_Goal_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &host_pkg__action__Arm_Goal__get_type_hash,
  &host_pkg__action__Arm_Goal__get_type_description,
  &host_pkg__action__Arm_Goal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<host_pkg::action::Arm_Goal>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_Goal_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_Goal)() {
  return get_message_type_support_handle<host_pkg::action::Arm_Goal>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "host_pkg/action/detail/arm__functions.h"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_Result_type_support_ids_t;

static const _Arm_Result_type_support_ids_t _Arm_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_Result_type_support_symbol_names_t _Arm_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_Result)),
  }
};

typedef struct _Arm_Result_type_support_data_t
{
  void * data[2];
} _Arm_Result_type_support_data_t;

static _Arm_Result_type_support_data_t _Arm_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_Result_message_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_Result_message_typesupport_ids.typesupport_identifier[0],
  &_Arm_Result_message_typesupport_symbol_names.symbol_name[0],
  &_Arm_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Arm_Result_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_Result_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &host_pkg__action__Arm_Result__get_type_hash,
  &host_pkg__action__Arm_Result__get_type_description,
  &host_pkg__action__Arm_Result__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<host_pkg::action::Arm_Result>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_Result_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_Result)() {
  return get_message_type_support_handle<host_pkg::action::Arm_Result>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "host_pkg/action/detail/arm__functions.h"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_Feedback_type_support_ids_t;

static const _Arm_Feedback_type_support_ids_t _Arm_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_Feedback_type_support_symbol_names_t _Arm_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_Feedback)),
  }
};

typedef struct _Arm_Feedback_type_support_data_t
{
  void * data[2];
} _Arm_Feedback_type_support_data_t;

static _Arm_Feedback_type_support_data_t _Arm_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_Feedback_message_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_Arm_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_Arm_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Arm_Feedback_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_Feedback_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &host_pkg__action__Arm_Feedback__get_type_hash,
  &host_pkg__action__Arm_Feedback__get_type_description,
  &host_pkg__action__Arm_Feedback__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<host_pkg::action::Arm_Feedback>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_Feedback)() {
  return get_message_type_support_handle<host_pkg::action::Arm_Feedback>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "host_pkg/action/detail/arm__functions.h"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_SendGoal_Request_type_support_ids_t;

static const _Arm_SendGoal_Request_type_support_ids_t _Arm_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_SendGoal_Request_type_support_symbol_names_t _Arm_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_SendGoal_Request)),
  }
};

typedef struct _Arm_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _Arm_SendGoal_Request_type_support_data_t;

static _Arm_SendGoal_Request_type_support_data_t _Arm_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_SendGoal_Request_message_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_Arm_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_Arm_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Arm_SendGoal_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_SendGoal_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &host_pkg__action__Arm_SendGoal_Request__get_type_hash,
  &host_pkg__action__Arm_SendGoal_Request__get_type_description,
  &host_pkg__action__Arm_SendGoal_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<host_pkg::action::Arm_SendGoal_Request>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_SendGoal_Request)() {
  return get_message_type_support_handle<host_pkg::action::Arm_SendGoal_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "host_pkg/action/detail/arm__functions.h"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_SendGoal_Response_type_support_ids_t;

static const _Arm_SendGoal_Response_type_support_ids_t _Arm_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_SendGoal_Response_type_support_symbol_names_t _Arm_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_SendGoal_Response)),
  }
};

typedef struct _Arm_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _Arm_SendGoal_Response_type_support_data_t;

static _Arm_SendGoal_Response_type_support_data_t _Arm_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_SendGoal_Response_message_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_Arm_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_Arm_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Arm_SendGoal_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_SendGoal_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &host_pkg__action__Arm_SendGoal_Response__get_type_hash,
  &host_pkg__action__Arm_SendGoal_Response__get_type_description,
  &host_pkg__action__Arm_SendGoal_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<host_pkg::action::Arm_SendGoal_Response>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_SendGoal_Response)() {
  return get_message_type_support_handle<host_pkg::action::Arm_SendGoal_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "host_pkg/action/detail/arm__functions.h"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_SendGoal_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_SendGoal_Event_type_support_ids_t;

static const _Arm_SendGoal_Event_type_support_ids_t _Arm_SendGoal_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_SendGoal_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_SendGoal_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_SendGoal_Event_type_support_symbol_names_t _Arm_SendGoal_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_SendGoal_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_SendGoal_Event)),
  }
};

typedef struct _Arm_SendGoal_Event_type_support_data_t
{
  void * data[2];
} _Arm_SendGoal_Event_type_support_data_t;

static _Arm_SendGoal_Event_type_support_data_t _Arm_SendGoal_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_SendGoal_Event_message_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_SendGoal_Event_message_typesupport_ids.typesupport_identifier[0],
  &_Arm_SendGoal_Event_message_typesupport_symbol_names.symbol_name[0],
  &_Arm_SendGoal_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Arm_SendGoal_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_SendGoal_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &host_pkg__action__Arm_SendGoal_Event__get_type_hash,
  &host_pkg__action__Arm_SendGoal_Event__get_type_description,
  &host_pkg__action__Arm_SendGoal_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<host_pkg::action::Arm_SendGoal_Event>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_SendGoal_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_SendGoal_Event)() {
  return get_message_type_support_handle<host_pkg::action::Arm_SendGoal_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_SendGoal_type_support_ids_t;

static const _Arm_SendGoal_type_support_ids_t _Arm_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_SendGoal_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_SendGoal_type_support_symbol_names_t _Arm_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_SendGoal)),
  }
};

typedef struct _Arm_SendGoal_type_support_data_t
{
  void * data[2];
} _Arm_SendGoal_type_support_data_t;

static _Arm_SendGoal_type_support_data_t _Arm_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_SendGoal_service_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_Arm_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_Arm_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t Arm_SendGoal_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_SendGoal_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<host_pkg::action::Arm_SendGoal_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<host_pkg::action::Arm_SendGoal_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<host_pkg::action::Arm_SendGoal_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<host_pkg::action::Arm_SendGoal>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<host_pkg::action::Arm_SendGoal>,
  &host_pkg__action__Arm_SendGoal__get_type_hash,
  &host_pkg__action__Arm_SendGoal__get_type_description,
  &host_pkg__action__Arm_SendGoal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<host_pkg::action::Arm_SendGoal>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_SendGoal_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_SendGoal)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<host_pkg::action::Arm_SendGoal>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "host_pkg/action/detail/arm__functions.h"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_GetResult_Request_type_support_ids_t;

static const _Arm_GetResult_Request_type_support_ids_t _Arm_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_GetResult_Request_type_support_symbol_names_t _Arm_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_GetResult_Request)),
  }
};

typedef struct _Arm_GetResult_Request_type_support_data_t
{
  void * data[2];
} _Arm_GetResult_Request_type_support_data_t;

static _Arm_GetResult_Request_type_support_data_t _Arm_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_GetResult_Request_message_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_Arm_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_Arm_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Arm_GetResult_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_GetResult_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &host_pkg__action__Arm_GetResult_Request__get_type_hash,
  &host_pkg__action__Arm_GetResult_Request__get_type_description,
  &host_pkg__action__Arm_GetResult_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<host_pkg::action::Arm_GetResult_Request>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_GetResult_Request)() {
  return get_message_type_support_handle<host_pkg::action::Arm_GetResult_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "host_pkg/action/detail/arm__functions.h"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_GetResult_Response_type_support_ids_t;

static const _Arm_GetResult_Response_type_support_ids_t _Arm_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_GetResult_Response_type_support_symbol_names_t _Arm_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_GetResult_Response)),
  }
};

typedef struct _Arm_GetResult_Response_type_support_data_t
{
  void * data[2];
} _Arm_GetResult_Response_type_support_data_t;

static _Arm_GetResult_Response_type_support_data_t _Arm_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_GetResult_Response_message_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_Arm_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_Arm_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Arm_GetResult_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_GetResult_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &host_pkg__action__Arm_GetResult_Response__get_type_hash,
  &host_pkg__action__Arm_GetResult_Response__get_type_description,
  &host_pkg__action__Arm_GetResult_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<host_pkg::action::Arm_GetResult_Response>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_GetResult_Response)() {
  return get_message_type_support_handle<host_pkg::action::Arm_GetResult_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "host_pkg/action/detail/arm__functions.h"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_GetResult_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_GetResult_Event_type_support_ids_t;

static const _Arm_GetResult_Event_type_support_ids_t _Arm_GetResult_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_GetResult_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_GetResult_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_GetResult_Event_type_support_symbol_names_t _Arm_GetResult_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_GetResult_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_GetResult_Event)),
  }
};

typedef struct _Arm_GetResult_Event_type_support_data_t
{
  void * data[2];
} _Arm_GetResult_Event_type_support_data_t;

static _Arm_GetResult_Event_type_support_data_t _Arm_GetResult_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_GetResult_Event_message_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_GetResult_Event_message_typesupport_ids.typesupport_identifier[0],
  &_Arm_GetResult_Event_message_typesupport_symbol_names.symbol_name[0],
  &_Arm_GetResult_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Arm_GetResult_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_GetResult_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &host_pkg__action__Arm_GetResult_Event__get_type_hash,
  &host_pkg__action__Arm_GetResult_Event__get_type_description,
  &host_pkg__action__Arm_GetResult_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<host_pkg::action::Arm_GetResult_Event>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_GetResult_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_GetResult_Event)() {
  return get_message_type_support_handle<host_pkg::action::Arm_GetResult_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_GetResult_type_support_ids_t;

static const _Arm_GetResult_type_support_ids_t _Arm_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_GetResult_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_GetResult_type_support_symbol_names_t _Arm_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_GetResult)),
  }
};

typedef struct _Arm_GetResult_type_support_data_t
{
  void * data[2];
} _Arm_GetResult_type_support_data_t;

static _Arm_GetResult_type_support_data_t _Arm_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_GetResult_service_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_Arm_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_Arm_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t Arm_GetResult_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_GetResult_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<host_pkg::action::Arm_GetResult_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<host_pkg::action::Arm_GetResult_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<host_pkg::action::Arm_GetResult_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<host_pkg::action::Arm_GetResult>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<host_pkg::action::Arm_GetResult>,
  &host_pkg__action__Arm_GetResult__get_type_hash,
  &host_pkg__action__Arm_GetResult__get_type_description,
  &host_pkg__action__Arm_GetResult__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<host_pkg::action::Arm_GetResult>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_GetResult_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_GetResult)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<host_pkg::action::Arm_GetResult>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "host_pkg/action/detail/arm__functions.h"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Arm_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Arm_FeedbackMessage_type_support_ids_t;

static const _Arm_FeedbackMessage_type_support_ids_t _Arm_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Arm_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Arm_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Arm_FeedbackMessage_type_support_symbol_names_t _Arm_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, host_pkg, action, Arm_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, host_pkg, action, Arm_FeedbackMessage)),
  }
};

typedef struct _Arm_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _Arm_FeedbackMessage_type_support_data_t;

static _Arm_FeedbackMessage_type_support_data_t _Arm_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Arm_FeedbackMessage_message_typesupport_map = {
  2,
  "host_pkg",
  &_Arm_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_Arm_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_Arm_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Arm_FeedbackMessage_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Arm_FeedbackMessage_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &host_pkg__action__Arm_FeedbackMessage__get_type_hash,
  &host_pkg__action__Arm_FeedbackMessage__get_type_description,
  &host_pkg__action__Arm_FeedbackMessage__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<host_pkg::action::Arm_FeedbackMessage>()
{
  return &::host_pkg::action::rosidl_typesupport_cpp::Arm_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm_FeedbackMessage)() {
  return get_message_type_support_handle<host_pkg::action::Arm_FeedbackMessage>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

#include "action_msgs/msg/goal_status_array.hpp"
#include "action_msgs/srv/cancel_goal.hpp"
// already included above
// #include "host_pkg/action/detail/arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_typesupport_cpp/action_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"

namespace host_pkg
{

namespace action
{

namespace rosidl_typesupport_cpp
{

static rosidl_action_type_support_t Arm_action_type_support_handle = {
  NULL, NULL, NULL, NULL, NULL,
  &host_pkg__action__Arm__get_type_hash,
  &host_pkg__action__Arm__get_type_description,
  &host_pkg__action__Arm__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace host_pkg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
get_action_type_support_handle<host_pkg::action::Arm>()
{
  using ::host_pkg::action::rosidl_typesupport_cpp::Arm_action_type_support_handle;
  // Thread-safe by always writing the same values to the static struct
  Arm_action_type_support_handle.goal_service_type_support = get_service_type_support_handle<::host_pkg::action::Arm::Impl::SendGoalService>();
  Arm_action_type_support_handle.result_service_type_support = get_service_type_support_handle<::host_pkg::action::Arm::Impl::GetResultService>();
  Arm_action_type_support_handle.cancel_service_type_support = get_service_type_support_handle<::host_pkg::action::Arm::Impl::CancelGoalService>();
  Arm_action_type_support_handle.feedback_message_type_support = get_message_type_support_handle<::host_pkg::action::Arm::Impl::FeedbackMessage>();
  Arm_action_type_support_handle.status_message_type_support = get_message_type_support_handle<::host_pkg::action::Arm::Impl::GoalStatusMessage>();
  return &Arm_action_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(rosidl_typesupport_cpp, host_pkg, action, Arm)() {
  return ::rosidl_typesupport_cpp::get_action_type_support_handle<host_pkg::action::Arm>();
}

#ifdef __cplusplus
}
#endif
