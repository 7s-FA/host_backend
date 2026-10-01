
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "host_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_Goal() -> *const std::ffi::c_void;
}

#[link(name = "host_pkg__rosidl_generator_c")]
extern "C" {
    fn host_pkg__action__Burger_Goal__init(msg: *mut Burger_Goal) -> bool;
    fn host_pkg__action__Burger_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Burger_Goal>, size: usize) -> bool;
    fn host_pkg__action__Burger_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Burger_Goal>);
    fn host_pkg__action__Burger_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Burger_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<Burger_Goal>) -> bool;
}

// Corresponds to host_pkg__action__Burger_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Burger_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub command: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub cmd_val: f32,

}



impl Default for Burger_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !host_pkg__action__Burger_Goal__init(&mut msg as *mut _) {
        panic!("Call to host_pkg__action__Burger_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Burger_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Burger_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Burger_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "host_pkg/action/Burger_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_Goal() }
  }
}


#[link(name = "host_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_Result() -> *const std::ffi::c_void;
}

#[link(name = "host_pkg__rosidl_generator_c")]
extern "C" {
    fn host_pkg__action__Burger_Result__init(msg: *mut Burger_Result) -> bool;
    fn host_pkg__action__Burger_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Burger_Result>, size: usize) -> bool;
    fn host_pkg__action__Burger_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Burger_Result>);
    fn host_pkg__action__Burger_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Burger_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<Burger_Result>) -> bool;
}

// Corresponds to host_pkg__action__Burger_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Burger_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for Burger_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !host_pkg__action__Burger_Result__init(&mut msg as *mut _) {
        panic!("Call to host_pkg__action__Burger_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Burger_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Burger_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Burger_Result where Self: Sized {
  const TYPE_NAME: &'static str = "host_pkg/action/Burger_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_Result() }
  }
}


#[link(name = "host_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "host_pkg__rosidl_generator_c")]
extern "C" {
    fn host_pkg__action__Burger_Feedback__init(msg: *mut Burger_Feedback) -> bool;
    fn host_pkg__action__Burger_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Burger_Feedback>, size: usize) -> bool;
    fn host_pkg__action__Burger_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Burger_Feedback>);
    fn host_pkg__action__Burger_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Burger_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<Burger_Feedback>) -> bool;
}

// Corresponds to host_pkg__action__Burger_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Burger_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_y: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_theta: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for Burger_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !host_pkg__action__Burger_Feedback__init(&mut msg as *mut _) {
        panic!("Call to host_pkg__action__Burger_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Burger_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Burger_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Burger_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "host_pkg/action/Burger_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_Feedback() }
  }
}


#[link(name = "host_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "host_pkg__rosidl_generator_c")]
extern "C" {
    fn host_pkg__action__Burger_FeedbackMessage__init(msg: *mut Burger_FeedbackMessage) -> bool;
    fn host_pkg__action__Burger_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Burger_FeedbackMessage>, size: usize) -> bool;
    fn host_pkg__action__Burger_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Burger_FeedbackMessage>);
    fn host_pkg__action__Burger_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Burger_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<Burger_FeedbackMessage>) -> bool;
}

// Corresponds to host_pkg__action__Burger_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Burger_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::Burger_Feedback,

}



impl Default for Burger_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !host_pkg__action__Burger_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to host_pkg__action__Burger_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Burger_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Burger_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Burger_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "host_pkg/action/Burger_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_FeedbackMessage() }
  }
}




#[link(name = "host_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "host_pkg__rosidl_generator_c")]
extern "C" {
    fn host_pkg__action__Burger_SendGoal_Request__init(msg: *mut Burger_SendGoal_Request) -> bool;
    fn host_pkg__action__Burger_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Burger_SendGoal_Request>, size: usize) -> bool;
    fn host_pkg__action__Burger_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Burger_SendGoal_Request>);
    fn host_pkg__action__Burger_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Burger_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Burger_SendGoal_Request>) -> bool;
}

// Corresponds to host_pkg__action__Burger_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Burger_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::Burger_Goal,

}



impl Default for Burger_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !host_pkg__action__Burger_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to host_pkg__action__Burger_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Burger_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Burger_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Burger_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "host_pkg/action/Burger_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_SendGoal_Request() }
  }
}


#[link(name = "host_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "host_pkg__rosidl_generator_c")]
extern "C" {
    fn host_pkg__action__Burger_SendGoal_Response__init(msg: *mut Burger_SendGoal_Response) -> bool;
    fn host_pkg__action__Burger_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Burger_SendGoal_Response>, size: usize) -> bool;
    fn host_pkg__action__Burger_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Burger_SendGoal_Response>);
    fn host_pkg__action__Burger_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Burger_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Burger_SendGoal_Response>) -> bool;
}

// Corresponds to host_pkg__action__Burger_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Burger_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for Burger_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !host_pkg__action__Burger_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to host_pkg__action__Burger_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Burger_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Burger_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Burger_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "host_pkg/action/Burger_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_SendGoal_Response() }
  }
}


#[link(name = "host_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "host_pkg__rosidl_generator_c")]
extern "C" {
    fn host_pkg__action__Burger_GetResult_Request__init(msg: *mut Burger_GetResult_Request) -> bool;
    fn host_pkg__action__Burger_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Burger_GetResult_Request>, size: usize) -> bool;
    fn host_pkg__action__Burger_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Burger_GetResult_Request>);
    fn host_pkg__action__Burger_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Burger_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Burger_GetResult_Request>) -> bool;
}

// Corresponds to host_pkg__action__Burger_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Burger_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for Burger_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !host_pkg__action__Burger_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to host_pkg__action__Burger_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Burger_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Burger_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Burger_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "host_pkg/action/Burger_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_GetResult_Request() }
  }
}


#[link(name = "host_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "host_pkg__rosidl_generator_c")]
extern "C" {
    fn host_pkg__action__Burger_GetResult_Response__init(msg: *mut Burger_GetResult_Response) -> bool;
    fn host_pkg__action__Burger_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Burger_GetResult_Response>, size: usize) -> bool;
    fn host_pkg__action__Burger_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Burger_GetResult_Response>);
    fn host_pkg__action__Burger_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Burger_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Burger_GetResult_Response>) -> bool;
}

// Corresponds to host_pkg__action__Burger_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Burger_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::Burger_Result,

}



impl Default for Burger_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !host_pkg__action__Burger_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to host_pkg__action__Burger_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Burger_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { host_pkg__action__Burger_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Burger_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Burger_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "host_pkg/action/Burger_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__host_pkg__action__Burger_GetResult_Response() }
  }
}






#[link(name = "host_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__host_pkg__action__Burger_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to host_pkg__action__Burger_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct Burger_SendGoal;

impl rosidl_runtime_rs::Service for Burger_SendGoal {
    type Request = Burger_SendGoal_Request;
    type Response = Burger_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__host_pkg__action__Burger_SendGoal() }
    }
}




#[link(name = "host_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__host_pkg__action__Burger_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to host_pkg__action__Burger_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct Burger_GetResult;

impl rosidl_runtime_rs::Service for Burger_GetResult {
    type Request = Burger_GetResult_Request;
    type Response = Burger_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__host_pkg__action__Burger_GetResult() }
    }
}


