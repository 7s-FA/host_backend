// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from host_pkg:action/Burger.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "host_pkg/action/burger.hpp"


#ifndef HOST_PKG__ACTION__DETAIL__BURGER__TRAITS_HPP_
#define HOST_PKG__ACTION__DETAIL__BURGER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "host_pkg/action/detail/burger__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace host_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const Burger_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: command
  {
    out << "command: ";
    rosidl_generator_traits::value_to_yaml(msg.command, out);
    out << ", ";
  }

  // member: cmd_val
  {
    out << "cmd_val: ";
    rosidl_generator_traits::value_to_yaml(msg.cmd_val, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Burger_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: command
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "command: ";
    rosidl_generator_traits::value_to_yaml(msg.command, out);
    out << "\n";
  }

  // member: cmd_val
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cmd_val: ";
    rosidl_generator_traits::value_to_yaml(msg.cmd_val, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Burger_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace host_pkg

namespace rosidl_generator_traits
{

[[deprecated("use host_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const host_pkg::action::Burger_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  host_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use host_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const host_pkg::action::Burger_Goal & msg)
{
  return host_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<host_pkg::action::Burger_Goal>()
{
  return "host_pkg::action::Burger_Goal";
}

template<>
inline const char * name<host_pkg::action::Burger_Goal>()
{
  return "host_pkg/action/Burger_Goal";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<host_pkg::action::Burger_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<host_pkg::action::Burger_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace host_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const Burger_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Burger_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Burger_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace host_pkg

namespace rosidl_generator_traits
{

[[deprecated("use host_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const host_pkg::action::Burger_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  host_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use host_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const host_pkg::action::Burger_Result & msg)
{
  return host_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<host_pkg::action::Burger_Result>()
{
  return "host_pkg::action::Burger_Result";
}

template<>
inline const char * name<host_pkg::action::Burger_Result>()
{
  return "host_pkg/action/Burger_Result";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<host_pkg::action::Burger_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<host_pkg::action::Burger_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace host_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const Burger_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: robot_x
  {
    out << "robot_x: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_x, out);
    out << ", ";
  }

  // member: robot_y
  {
    out << "robot_y: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_y, out);
    out << ", ";
  }

  // member: robot_theta
  {
    out << "robot_theta: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_theta, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Burger_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: robot_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_x: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_x, out);
    out << "\n";
  }

  // member: robot_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_y: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_y, out);
    out << "\n";
  }

  // member: robot_theta
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_theta: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_theta, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Burger_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace host_pkg

namespace rosidl_generator_traits
{

[[deprecated("use host_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const host_pkg::action::Burger_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  host_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use host_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const host_pkg::action::Burger_Feedback & msg)
{
  return host_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<host_pkg::action::Burger_Feedback>()
{
  return "host_pkg::action::Burger_Feedback";
}

template<>
inline const char * name<host_pkg::action::Burger_Feedback>()
{
  return "host_pkg/action/Burger_Feedback";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<host_pkg::action::Burger_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<host_pkg::action::Burger_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "host_pkg/action/detail/burger__traits.hpp"

namespace host_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const Burger_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Burger_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Burger_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace host_pkg

namespace rosidl_generator_traits
{

[[deprecated("use host_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const host_pkg::action::Burger_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  host_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use host_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const host_pkg::action::Burger_SendGoal_Request & msg)
{
  return host_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<host_pkg::action::Burger_SendGoal_Request>()
{
  return "host_pkg::action::Burger_SendGoal_Request";
}

template<>
inline const char * name<host_pkg::action::Burger_SendGoal_Request>()
{
  return "host_pkg/action/Burger_SendGoal_Request";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<host_pkg::action::Burger_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<host_pkg::action::Burger_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<host_pkg::action::Burger_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<host_pkg::action::Burger_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace host_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const Burger_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Burger_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Burger_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace host_pkg

namespace rosidl_generator_traits
{

[[deprecated("use host_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const host_pkg::action::Burger_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  host_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use host_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const host_pkg::action::Burger_SendGoal_Response & msg)
{
  return host_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<host_pkg::action::Burger_SendGoal_Response>()
{
  return "host_pkg::action::Burger_SendGoal_Response";
}

template<>
inline const char * name<host_pkg::action::Burger_SendGoal_Response>()
{
  return "host_pkg/action/Burger_SendGoal_Response";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<host_pkg::action::Burger_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<host_pkg::action::Burger_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace host_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const Burger_SendGoal_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Burger_SendGoal_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Burger_SendGoal_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace host_pkg

namespace rosidl_generator_traits
{

[[deprecated("use host_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const host_pkg::action::Burger_SendGoal_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  host_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use host_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const host_pkg::action::Burger_SendGoal_Event & msg)
{
  return host_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<host_pkg::action::Burger_SendGoal_Event>()
{
  return "host_pkg::action::Burger_SendGoal_Event";
}

template<>
inline const char * name<host_pkg::action::Burger_SendGoal_Event>()
{
  return "host_pkg/action/Burger_SendGoal_Event";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_SendGoal_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<host_pkg::action::Burger_SendGoal_Event>
  : std::integral_constant<bool, has_bounded_size<host_pkg::action::Burger_SendGoal_Request>::value && has_bounded_size<host_pkg::action::Burger_SendGoal_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<host_pkg::action::Burger_SendGoal_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<host_pkg::action::Burger_SendGoal>()
{
  return "host_pkg::action::Burger_SendGoal";
}

template<>
inline const char * name<host_pkg::action::Burger_SendGoal>()
{
  return "host_pkg/action/Burger_SendGoal";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<host_pkg::action::Burger_SendGoal_Request>::value &&
    has_fixed_size<host_pkg::action::Burger_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<host_pkg::action::Burger_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<host_pkg::action::Burger_SendGoal_Request>::value &&
    has_bounded_size<host_pkg::action::Burger_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<host_pkg::action::Burger_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<host_pkg::action::Burger_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<host_pkg::action::Burger_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace host_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const Burger_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Burger_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Burger_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace host_pkg

namespace rosidl_generator_traits
{

[[deprecated("use host_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const host_pkg::action::Burger_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  host_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use host_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const host_pkg::action::Burger_GetResult_Request & msg)
{
  return host_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<host_pkg::action::Burger_GetResult_Request>()
{
  return "host_pkg::action::Burger_GetResult_Request";
}

template<>
inline const char * name<host_pkg::action::Burger_GetResult_Request>()
{
  return "host_pkg/action/Burger_GetResult_Request";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<host_pkg::action::Burger_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<host_pkg::action::Burger_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "host_pkg/action/detail/burger__traits.hpp"

namespace host_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const Burger_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Burger_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Burger_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace host_pkg

namespace rosidl_generator_traits
{

[[deprecated("use host_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const host_pkg::action::Burger_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  host_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use host_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const host_pkg::action::Burger_GetResult_Response & msg)
{
  return host_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<host_pkg::action::Burger_GetResult_Response>()
{
  return "host_pkg::action::Burger_GetResult_Response";
}

template<>
inline const char * name<host_pkg::action::Burger_GetResult_Response>()
{
  return "host_pkg/action/Burger_GetResult_Response";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<host_pkg::action::Burger_Result>::value> {};

template<>
struct has_bounded_size<host_pkg::action::Burger_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<host_pkg::action::Burger_Result>::value> {};

template<>
struct is_message<host_pkg::action::Burger_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace host_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const Burger_GetResult_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Burger_GetResult_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Burger_GetResult_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace host_pkg

namespace rosidl_generator_traits
{

[[deprecated("use host_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const host_pkg::action::Burger_GetResult_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  host_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use host_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const host_pkg::action::Burger_GetResult_Event & msg)
{
  return host_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<host_pkg::action::Burger_GetResult_Event>()
{
  return "host_pkg::action::Burger_GetResult_Event";
}

template<>
inline const char * name<host_pkg::action::Burger_GetResult_Event>()
{
  return "host_pkg/action/Burger_GetResult_Event";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_GetResult_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<host_pkg::action::Burger_GetResult_Event>
  : std::integral_constant<bool, has_bounded_size<host_pkg::action::Burger_GetResult_Request>::value && has_bounded_size<host_pkg::action::Burger_GetResult_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<host_pkg::action::Burger_GetResult_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<host_pkg::action::Burger_GetResult>()
{
  return "host_pkg::action::Burger_GetResult";
}

template<>
inline const char * name<host_pkg::action::Burger_GetResult>()
{
  return "host_pkg/action/Burger_GetResult";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<host_pkg::action::Burger_GetResult_Request>::value &&
    has_fixed_size<host_pkg::action::Burger_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<host_pkg::action::Burger_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<host_pkg::action::Burger_GetResult_Request>::value &&
    has_bounded_size<host_pkg::action::Burger_GetResult_Response>::value
  >
{
};

template<>
struct is_service<host_pkg::action::Burger_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<host_pkg::action::Burger_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<host_pkg::action::Burger_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "host_pkg/action/detail/burger__traits.hpp"

namespace host_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const Burger_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Burger_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Burger_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace host_pkg

namespace rosidl_generator_traits
{

[[deprecated("use host_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const host_pkg::action::Burger_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  host_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use host_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const host_pkg::action::Burger_FeedbackMessage & msg)
{
  return host_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<host_pkg::action::Burger_FeedbackMessage>()
{
  return "host_pkg::action::Burger_FeedbackMessage";
}

template<>
inline const char * name<host_pkg::action::Burger_FeedbackMessage>()
{
  return "host_pkg/action/Burger_FeedbackMessage";
}

template<>
struct has_fixed_size<host_pkg::action::Burger_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<host_pkg::action::Burger_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<host_pkg::action::Burger_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<host_pkg::action::Burger_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<host_pkg::action::Burger_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<host_pkg::action::Burger>
  : std::true_type
{
};

template<>
struct is_action_goal<host_pkg::action::Burger_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<host_pkg::action::Burger_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<host_pkg::action::Burger_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // HOST_PKG__ACTION__DETAIL__BURGER__TRAITS_HPP_
