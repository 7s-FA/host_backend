// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from host_pkg:action/Arm.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "host_pkg/action/arm.hpp"


#ifndef HOST_PKG__ACTION__DETAIL__ARM__BUILDER_HPP_
#define HOST_PKG__ACTION__DETAIL__ARM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "host_pkg/action/detail/arm__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Arm_Goal_command
{
public:
  Init_Arm_Goal_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::host_pkg::action::Arm_Goal command(::host_pkg::action::Arm_Goal::_command_type arg)
  {
    msg_.command = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Arm_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Arm_Goal>()
{
  return host_pkg::action::builder::Init_Arm_Goal_command();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Arm_Result_message
{
public:
  explicit Init_Arm_Result_message(::host_pkg::action::Arm_Result & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Arm_Result message(::host_pkg::action::Arm_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Arm_Result msg_;
};

class Init_Arm_Result_success
{
public:
  Init_Arm_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Arm_Result_message success(::host_pkg::action::Arm_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_Arm_Result_message(msg_);
  }

private:
  ::host_pkg::action::Arm_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Arm_Result>()
{
  return host_pkg::action::builder::Init_Arm_Result_success();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Arm_Feedback_message
{
public:
  Init_Arm_Feedback_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::host_pkg::action::Arm_Feedback message(::host_pkg::action::Arm_Feedback::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Arm_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Arm_Feedback>()
{
  return host_pkg::action::builder::Init_Arm_Feedback_message();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Arm_SendGoal_Request_goal
{
public:
  explicit Init_Arm_SendGoal_Request_goal(::host_pkg::action::Arm_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Arm_SendGoal_Request goal(::host_pkg::action::Arm_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Arm_SendGoal_Request msg_;
};

class Init_Arm_SendGoal_Request_goal_id
{
public:
  Init_Arm_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Arm_SendGoal_Request_goal goal_id(::host_pkg::action::Arm_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Arm_SendGoal_Request_goal(msg_);
  }

private:
  ::host_pkg::action::Arm_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Arm_SendGoal_Request>()
{
  return host_pkg::action::builder::Init_Arm_SendGoal_Request_goal_id();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Arm_SendGoal_Response_stamp
{
public:
  explicit Init_Arm_SendGoal_Response_stamp(::host_pkg::action::Arm_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Arm_SendGoal_Response stamp(::host_pkg::action::Arm_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Arm_SendGoal_Response msg_;
};

class Init_Arm_SendGoal_Response_accepted
{
public:
  Init_Arm_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Arm_SendGoal_Response_stamp accepted(::host_pkg::action::Arm_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Arm_SendGoal_Response_stamp(msg_);
  }

private:
  ::host_pkg::action::Arm_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Arm_SendGoal_Response>()
{
  return host_pkg::action::builder::Init_Arm_SendGoal_Response_accepted();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Arm_SendGoal_Event_response
{
public:
  explicit Init_Arm_SendGoal_Event_response(::host_pkg::action::Arm_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Arm_SendGoal_Event response(::host_pkg::action::Arm_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Arm_SendGoal_Event msg_;
};

class Init_Arm_SendGoal_Event_request
{
public:
  explicit Init_Arm_SendGoal_Event_request(::host_pkg::action::Arm_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_Arm_SendGoal_Event_response request(::host_pkg::action::Arm_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Arm_SendGoal_Event_response(msg_);
  }

private:
  ::host_pkg::action::Arm_SendGoal_Event msg_;
};

class Init_Arm_SendGoal_Event_info
{
public:
  Init_Arm_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Arm_SendGoal_Event_request info(::host_pkg::action::Arm_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Arm_SendGoal_Event_request(msg_);
  }

private:
  ::host_pkg::action::Arm_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Arm_SendGoal_Event>()
{
  return host_pkg::action::builder::Init_Arm_SendGoal_Event_info();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Arm_GetResult_Request_goal_id
{
public:
  Init_Arm_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::host_pkg::action::Arm_GetResult_Request goal_id(::host_pkg::action::Arm_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Arm_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Arm_GetResult_Request>()
{
  return host_pkg::action::builder::Init_Arm_GetResult_Request_goal_id();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Arm_GetResult_Response_result
{
public:
  explicit Init_Arm_GetResult_Response_result(::host_pkg::action::Arm_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Arm_GetResult_Response result(::host_pkg::action::Arm_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Arm_GetResult_Response msg_;
};

class Init_Arm_GetResult_Response_status
{
public:
  Init_Arm_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Arm_GetResult_Response_result status(::host_pkg::action::Arm_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Arm_GetResult_Response_result(msg_);
  }

private:
  ::host_pkg::action::Arm_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Arm_GetResult_Response>()
{
  return host_pkg::action::builder::Init_Arm_GetResult_Response_status();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Arm_GetResult_Event_response
{
public:
  explicit Init_Arm_GetResult_Event_response(::host_pkg::action::Arm_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Arm_GetResult_Event response(::host_pkg::action::Arm_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Arm_GetResult_Event msg_;
};

class Init_Arm_GetResult_Event_request
{
public:
  explicit Init_Arm_GetResult_Event_request(::host_pkg::action::Arm_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_Arm_GetResult_Event_response request(::host_pkg::action::Arm_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Arm_GetResult_Event_response(msg_);
  }

private:
  ::host_pkg::action::Arm_GetResult_Event msg_;
};

class Init_Arm_GetResult_Event_info
{
public:
  Init_Arm_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Arm_GetResult_Event_request info(::host_pkg::action::Arm_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Arm_GetResult_Event_request(msg_);
  }

private:
  ::host_pkg::action::Arm_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Arm_GetResult_Event>()
{
  return host_pkg::action::builder::Init_Arm_GetResult_Event_info();
}

}  // namespace host_pkg


namespace host_pkg
{

namespace action
{

namespace builder
{

class Init_Arm_FeedbackMessage_feedback
{
public:
  explicit Init_Arm_FeedbackMessage_feedback(::host_pkg::action::Arm_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::host_pkg::action::Arm_FeedbackMessage feedback(::host_pkg::action::Arm_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::host_pkg::action::Arm_FeedbackMessage msg_;
};

class Init_Arm_FeedbackMessage_goal_id
{
public:
  Init_Arm_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Arm_FeedbackMessage_feedback goal_id(::host_pkg::action::Arm_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Arm_FeedbackMessage_feedback(msg_);
  }

private:
  ::host_pkg::action::Arm_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::host_pkg::action::Arm_FeedbackMessage>()
{
  return host_pkg::action::builder::Init_Arm_FeedbackMessage_goal_id();
}

}  // namespace host_pkg

#endif  // HOST_PKG__ACTION__DETAIL__ARM__BUILDER_HPP_
