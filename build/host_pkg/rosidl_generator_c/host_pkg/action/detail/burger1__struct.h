// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from host_pkg:action/Burger1.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "host_pkg/action/burger1.h"


#ifndef HOST_PKG__ACTION__DETAIL__BURGER1__STRUCT_H_
#define HOST_PKG__ACTION__DETAIL__BURGER1__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'command'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/Burger1 in the package host_pkg.
typedef struct host_pkg__action__Burger1_Goal
{
  rosidl_runtime_c__String command;
  float cmd_val;
} host_pkg__action__Burger1_Goal;

// Struct for a sequence of host_pkg__action__Burger1_Goal.
typedef struct host_pkg__action__Burger1_Goal__Sequence
{
  host_pkg__action__Burger1_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} host_pkg__action__Burger1_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/Burger1 in the package host_pkg.
typedef struct host_pkg__action__Burger1_Result
{
  bool success;
  rosidl_runtime_c__String message;
} host_pkg__action__Burger1_Result;

// Struct for a sequence of host_pkg__action__Burger1_Result.
typedef struct host_pkg__action__Burger1_Result__Sequence
{
  host_pkg__action__Burger1_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} host_pkg__action__Burger1_Result__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'robot_theta'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/Burger1 in the package host_pkg.
typedef struct host_pkg__action__Burger1_Feedback
{
  float robot_x;
  float robot_y;
  rosidl_runtime_c__String robot_theta;
} host_pkg__action__Burger1_Feedback;

// Struct for a sequence of host_pkg__action__Burger1_Feedback.
typedef struct host_pkg__action__Burger1_Feedback__Sequence
{
  host_pkg__action__Burger1_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} host_pkg__action__Burger1_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "host_pkg/action/detail/burger1__struct.h"

/// Struct defined in action/Burger1 in the package host_pkg.
typedef struct host_pkg__action__Burger1_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  host_pkg__action__Burger1_Goal goal;
} host_pkg__action__Burger1_SendGoal_Request;

// Struct for a sequence of host_pkg__action__Burger1_SendGoal_Request.
typedef struct host_pkg__action__Burger1_SendGoal_Request__Sequence
{
  host_pkg__action__Burger1_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} host_pkg__action__Burger1_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/Burger1 in the package host_pkg.
typedef struct host_pkg__action__Burger1_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} host_pkg__action__Burger1_SendGoal_Response;

// Struct for a sequence of host_pkg__action__Burger1_SendGoal_Response.
typedef struct host_pkg__action__Burger1_SendGoal_Response__Sequence
{
  host_pkg__action__Burger1_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} host_pkg__action__Burger1_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  host_pkg__action__Burger1_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  host_pkg__action__Burger1_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/Burger1 in the package host_pkg.
typedef struct host_pkg__action__Burger1_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  host_pkg__action__Burger1_SendGoal_Request__Sequence request;
  host_pkg__action__Burger1_SendGoal_Response__Sequence response;
} host_pkg__action__Burger1_SendGoal_Event;

// Struct for a sequence of host_pkg__action__Burger1_SendGoal_Event.
typedef struct host_pkg__action__Burger1_SendGoal_Event__Sequence
{
  host_pkg__action__Burger1_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} host_pkg__action__Burger1_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/Burger1 in the package host_pkg.
typedef struct host_pkg__action__Burger1_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} host_pkg__action__Burger1_GetResult_Request;

// Struct for a sequence of host_pkg__action__Burger1_GetResult_Request.
typedef struct host_pkg__action__Burger1_GetResult_Request__Sequence
{
  host_pkg__action__Burger1_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} host_pkg__action__Burger1_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "host_pkg/action/detail/burger1__struct.h"

/// Struct defined in action/Burger1 in the package host_pkg.
typedef struct host_pkg__action__Burger1_GetResult_Response
{
  int8_t status;
  host_pkg__action__Burger1_Result result;
} host_pkg__action__Burger1_GetResult_Response;

// Struct for a sequence of host_pkg__action__Burger1_GetResult_Response.
typedef struct host_pkg__action__Burger1_GetResult_Response__Sequence
{
  host_pkg__action__Burger1_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} host_pkg__action__Burger1_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  host_pkg__action__Burger1_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  host_pkg__action__Burger1_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/Burger1 in the package host_pkg.
typedef struct host_pkg__action__Burger1_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  host_pkg__action__Burger1_GetResult_Request__Sequence request;
  host_pkg__action__Burger1_GetResult_Response__Sequence response;
} host_pkg__action__Burger1_GetResult_Event;

// Struct for a sequence of host_pkg__action__Burger1_GetResult_Event.
typedef struct host_pkg__action__Burger1_GetResult_Event__Sequence
{
  host_pkg__action__Burger1_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} host_pkg__action__Burger1_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "host_pkg/action/detail/burger1__struct.h"

/// Struct defined in action/Burger1 in the package host_pkg.
typedef struct host_pkg__action__Burger1_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  host_pkg__action__Burger1_Feedback feedback;
} host_pkg__action__Burger1_FeedbackMessage;

// Struct for a sequence of host_pkg__action__Burger1_FeedbackMessage.
typedef struct host_pkg__action__Burger1_FeedbackMessage__Sequence
{
  host_pkg__action__Burger1_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} host_pkg__action__Burger1_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HOST_PKG__ACTION__DETAIL__BURGER1__STRUCT_H_
