// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from host_pkg:action/Burger1.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "host_pkg/action/burger1.hpp"


#ifndef HOST_PKG__ACTION__DETAIL__BURGER1__BUILDER_HPP_
#define HOST_PKG__ACTION__DETAIL__BURGER1__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "host_pkg/action/detail/burger1__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Burger1_Goal_cmd_val
{
public:
  explicit Init_Burger1_Goal_cmd_val(::host_pkg::action::Burger1_Goal & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Burger1_Goal cmd_val(::host_pkg::action::Burger1_Goal::_cmd_val_type arg)
  {
    msg_.cmd_val = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Burger1_Goal msg_;
};

class Init_Burger1_Goal_command
{
public:
  Init_Burger1_Goal_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Burger1_Goal_cmd_val command(::host_pkg::action::Burger1_Goal::_command_type arg)
  {
    msg_.command = std::move(arg);
    return Init_Burger1_Goal_cmd_val(msg_);
  }

private:
  ::host_pkg::action::Burger1_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Burger1_Goal>()
{
  return host_pkg::action::builder::Init_Burger1_Goal_command();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Burger1_Result_message
{
public:
  explicit Init_Burger1_Result_message(::host_pkg::action::Burger1_Result & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Burger1_Result message(::host_pkg::action::Burger1_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Burger1_Result msg_;
};

class Init_Burger1_Result_success
{
public:
  Init_Burger1_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Burger1_Result_message success(::host_pkg::action::Burger1_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_Burger1_Result_message(msg_);
  }

private:
  ::host_pkg::action::Burger1_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Burger1_Result>()
{
  return host_pkg::action::builder::Init_Burger1_Result_success();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Burger1_Feedback_robot_theta
{
public:
  explicit Init_Burger1_Feedback_robot_theta(::host_pkg::action::Burger1_Feedback & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Burger1_Feedback robot_theta(::host_pkg::action::Burger1_Feedback::_robot_theta_type arg)
  {
    msg_.robot_theta = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Burger1_Feedback msg_;
};

class Init_Burger1_Feedback_robot_y
{
public:
  explicit Init_Burger1_Feedback_robot_y(::host_pkg::action::Burger1_Feedback & msg)
  : msg_(msg)
  {}
  Init_Burger1_Feedback_robot_theta robot_y(::host_pkg::action::Burger1_Feedback::_robot_y_type arg)
  {
    msg_.robot_y = std::move(arg);
    return Init_Burger1_Feedback_robot_theta(msg_);
  }

private:
  ::host_pkg::action::Burger1_Feedback msg_;
};

class Init_Burger1_Feedback_robot_x
{
public:
  Init_Burger1_Feedback_robot_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Burger1_Feedback_robot_y robot_x(::host_pkg::action::Burger1_Feedback::_robot_x_type arg)
  {
    msg_.robot_x = std::move(arg);
    return Init_Burger1_Feedback_robot_y(msg_);
  }

private:
  ::host_pkg::action::Burger1_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Burger1_Feedback>()
{
  return host_pkg::action::builder::Init_Burger1_Feedback_robot_x();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Burger1_SendGoal_Request_goal
{
public:
  explicit Init_Burger1_SendGoal_Request_goal(::host_pkg::action::Burger1_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Burger1_SendGoal_Request goal(::host_pkg::action::Burger1_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Burger1_SendGoal_Request msg_;
};

class Init_Burger1_SendGoal_Request_goal_id
{
public:
  Init_Burger1_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Burger1_SendGoal_Request_goal goal_id(::host_pkg::action::Burger1_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Burger1_SendGoal_Request_goal(msg_);
  }

private:
  ::host_pkg::action::Burger1_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Burger1_SendGoal_Request>()
{
  return host_pkg::action::builder::Init_Burger1_SendGoal_Request_goal_id();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Burger1_SendGoal_Response_stamp
{
public:
  explicit Init_Burger1_SendGoal_Response_stamp(::host_pkg::action::Burger1_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Burger1_SendGoal_Response stamp(::host_pkg::action::Burger1_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Burger1_SendGoal_Response msg_;
};

class Init_Burger1_SendGoal_Response_accepted
{
public:
  Init_Burger1_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Burger1_SendGoal_Response_stamp accepted(::host_pkg::action::Burger1_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Burger1_SendGoal_Response_stamp(msg_);
  }

private:
  ::host_pkg::action::Burger1_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Burger1_SendGoal_Response>()
{
  return host_pkg::action::builder::Init_Burger1_SendGoal_Response_accepted();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Burger1_SendGoal_Event_response
{
public:
  explicit Init_Burger1_SendGoal_Event_response(::host_pkg::action::Burger1_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Burger1_SendGoal_Event response(::host_pkg::action::Burger1_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Burger1_SendGoal_Event msg_;
};

class Init_Burger1_SendGoal_Event_request
{
public:
  explicit Init_Burger1_SendGoal_Event_request(::host_pkg::action::Burger1_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_Burger1_SendGoal_Event_response request(::host_pkg::action::Burger1_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Burger1_SendGoal_Event_response(msg_);
  }

private:
  ::host_pkg::action::Burger1_SendGoal_Event msg_;
};

class Init_Burger1_SendGoal_Event_info
{
public:
  Init_Burger1_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Burger1_SendGoal_Event_request info(::host_pkg::action::Burger1_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Burger1_SendGoal_Event_request(msg_);
  }

private:
  ::host_pkg::action::Burger1_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Burger1_SendGoal_Event>()
{
  return host_pkg::action::builder::Init_Burger1_SendGoal_Event_info();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Burger1_GetResult_Request_goal_id
{
public:
  Init_Burger1_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::host_pkg::action::Burger1_GetResult_Request goal_id(::host_pkg::action::Burger1_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Burger1_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Burger1_GetResult_Request>()
{
  return host_pkg::action::builder::Init_Burger1_GetResult_Request_goal_id();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Burger1_GetResult_Response_result
{
public:
  explicit Init_Burger1_GetResult_Response_result(::host_pkg::action::Burger1_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Burger1_GetResult_Response result(::host_pkg::action::Burger1_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Burger1_GetResult_Response msg_;
};

class Init_Burger1_GetResult_Response_status
{
public:
  Init_Burger1_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Burger1_GetResult_Response_result status(::host_pkg::action::Burger1_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Burger1_GetResult_Response_result(msg_);
  }

private:
  ::host_pkg::action::Burger1_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Burger1_GetResult_Response>()
{
  return host_pkg::action::builder::Init_Burger1_GetResult_Response_status();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Burger1_GetResult_Event_response
{
public:
  explicit Init_Burger1_GetResult_Event_response(::host_pkg::action::Burger1_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Burger1_GetResult_Event response(::host_pkg::action::Burger1_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Burger1_GetResult_Event msg_;
};

class Init_Burger1_GetResult_Event_request
{
public:
  explicit Init_Burger1_GetResult_Event_request(::host_pkg::action::Burger1_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_Burger1_GetResult_Event_response request(::host_pkg::action::Burger1_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Burger1_GetResult_Event_response(msg_);
  }

private:
  ::host_pkg::action::Burger1_GetResult_Event msg_;
};

class Init_Burger1_GetResult_Event_info
{
public:
  Init_Burger1_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Burger1_GetResult_Event_request info(::host_pkg::action::Burger1_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Burger1_GetResult_Event_request(msg_);
  }

private:
  ::host_pkg::action::Burger1_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Burger1_GetResult_Event>()
{
  return host_pkg::action::builder::Init_Burger1_GetResult_Event_info();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Burger1_FeedbackMessage_feedback
{
public:
  explicit Init_Burger1_FeedbackMessage_feedback(::host_pkg::action::Burger1_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Burger1_FeedbackMessage feedback(::host_pkg::action::Burger1_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Burger1_FeedbackMessage msg_;
};

class Init_Burger1_FeedbackMessage_goal_id
{
public:
  Init_Burger1_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Burger1_FeedbackMessage_feedback goal_id(::host_pkg::action::Burger1_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Burger1_FeedbackMessage_feedback(msg_);
  }

private:
  ::host_pkg::action::Burger1_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Burger1_FeedbackMessage>()
{
  return host_pkg::action::builder::Init_Burger1_FeedbackMessage_goal_id();
}

}  // namespace host_pkg

#endif  // HOST_PKG__ACTION__DETAIL__BURGER1__BUILDER_HPP_
