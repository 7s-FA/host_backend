// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from host_pkg:action/Burger.idl
// generated code does not contain a copyright notice
#include "host_pkg/action/detail/burger__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `command`
#include "rosidl_runtime_c/string_functions.h"

bool
host_pkg__action__Burger_Goal__init(host_pkg__action__Burger_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // command
  if (!rosidl_runtime_c__String__init(&msg->command)) {
    host_pkg__action__Burger_Goal__fini(msg);
    return false;
  }
  // cmd_val
  return true;
}

void
host_pkg__action__Burger_Goal__fini(host_pkg__action__Burger_Goal * msg)
{
  if (!msg) {
    return;
  }
  // command
  rosidl_runtime_c__String__fini(&msg->command);
  // cmd_val
}

bool
host_pkg__action__Burger_Goal__are_equal(const host_pkg__action__Burger_Goal * lhs, const host_pkg__action__Burger_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // command
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->command), &(rhs->command)))
  {
    return false;
  }
  // cmd_val
  if (lhs->cmd_val != rhs->cmd_val) {
    return false;
  }
  return true;
}

bool
host_pkg__action__Burger_Goal__copy(
  const host_pkg__action__Burger_Goal * input,
  host_pkg__action__Burger_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // command
  if (!rosidl_runtime_c__String__copy(
      &(input->command), &(output->command)))
  {
    return false;
  }
  // cmd_val
  output->cmd_val = input->cmd_val;
  return true;
}

host_pkg__action__Burger_Goal *
host_pkg__action__Burger_Goal__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_Goal * msg = (host_pkg__action__Burger_Goal *)allocator.allocate(sizeof(host_pkg__action__Burger_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(host_pkg__action__Burger_Goal));
  bool success = host_pkg__action__Burger_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
host_pkg__action__Burger_Goal__destroy(host_pkg__action__Burger_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    host_pkg__action__Burger_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
host_pkg__action__Burger_Goal__Sequence__init(host_pkg__action__Burger_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_Goal * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(host_pkg__action__Burger_Goal)) {
      return false;
    }
    data = (host_pkg__action__Burger_Goal *)allocator.zero_allocate(size, sizeof(host_pkg__action__Burger_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = host_pkg__action__Burger_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        host_pkg__action__Burger_Goal__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
host_pkg__action__Burger_Goal__Sequence__fini(host_pkg__action__Burger_Goal__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      host_pkg__action__Burger_Goal__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

host_pkg__action__Burger_Goal__Sequence *
host_pkg__action__Burger_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_Goal__Sequence * array = (host_pkg__action__Burger_Goal__Sequence *)allocator.allocate(sizeof(host_pkg__action__Burger_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = host_pkg__action__Burger_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
host_pkg__action__Burger_Goal__Sequence__destroy(host_pkg__action__Burger_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    host_pkg__action__Burger_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
host_pkg__action__Burger_Goal__Sequence__are_equal(const host_pkg__action__Burger_Goal__Sequence * lhs, const host_pkg__action__Burger_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!host_pkg__action__Burger_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
host_pkg__action__Burger_Goal__Sequence__copy(
  const host_pkg__action__Burger_Goal__Sequence * input,
  host_pkg__action__Burger_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(host_pkg__action__Burger_Goal)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(host_pkg__action__Burger_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    host_pkg__action__Burger_Goal * data =
      (host_pkg__action__Burger_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!host_pkg__action__Burger_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          host_pkg__action__Burger_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!host_pkg__action__Burger_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
host_pkg__action__Burger_Result__init(host_pkg__action__Burger_Result * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    host_pkg__action__Burger_Result__fini(msg);
    return false;
  }
  return true;
}

void
host_pkg__action__Burger_Result__fini(host_pkg__action__Burger_Result * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
host_pkg__action__Burger_Result__are_equal(const host_pkg__action__Burger_Result * lhs, const host_pkg__action__Burger_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
host_pkg__action__Burger_Result__copy(
  const host_pkg__action__Burger_Result * input,
  host_pkg__action__Burger_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

host_pkg__action__Burger_Result *
host_pkg__action__Burger_Result__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_Result * msg = (host_pkg__action__Burger_Result *)allocator.allocate(sizeof(host_pkg__action__Burger_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(host_pkg__action__Burger_Result));
  bool success = host_pkg__action__Burger_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
host_pkg__action__Burger_Result__destroy(host_pkg__action__Burger_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    host_pkg__action__Burger_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
host_pkg__action__Burger_Result__Sequence__init(host_pkg__action__Burger_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_Result * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(host_pkg__action__Burger_Result)) {
      return false;
    }
    data = (host_pkg__action__Burger_Result *)allocator.zero_allocate(size, sizeof(host_pkg__action__Burger_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = host_pkg__action__Burger_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        host_pkg__action__Burger_Result__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
host_pkg__action__Burger_Result__Sequence__fini(host_pkg__action__Burger_Result__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      host_pkg__action__Burger_Result__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

host_pkg__action__Burger_Result__Sequence *
host_pkg__action__Burger_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_Result__Sequence * array = (host_pkg__action__Burger_Result__Sequence *)allocator.allocate(sizeof(host_pkg__action__Burger_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = host_pkg__action__Burger_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
host_pkg__action__Burger_Result__Sequence__destroy(host_pkg__action__Burger_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    host_pkg__action__Burger_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
host_pkg__action__Burger_Result__Sequence__are_equal(const host_pkg__action__Burger_Result__Sequence * lhs, const host_pkg__action__Burger_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!host_pkg__action__Burger_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
host_pkg__action__Burger_Result__Sequence__copy(
  const host_pkg__action__Burger_Result__Sequence * input,
  host_pkg__action__Burger_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(host_pkg__action__Burger_Result)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(host_pkg__action__Burger_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    host_pkg__action__Burger_Result * data =
      (host_pkg__action__Burger_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!host_pkg__action__Burger_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          host_pkg__action__Burger_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!host_pkg__action__Burger_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `robot_theta`
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
host_pkg__action__Burger_Feedback__init(host_pkg__action__Burger_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // robot_x
  // robot_y
  // robot_theta
  if (!rosidl_runtime_c__String__init(&msg->robot_theta)) {
    host_pkg__action__Burger_Feedback__fini(msg);
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    host_pkg__action__Burger_Feedback__fini(msg);
    return false;
  }
  return true;
}

void
host_pkg__action__Burger_Feedback__fini(host_pkg__action__Burger_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // robot_x
  // robot_y
  // robot_theta
  rosidl_runtime_c__String__fini(&msg->robot_theta);
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
host_pkg__action__Burger_Feedback__are_equal(const host_pkg__action__Burger_Feedback * lhs, const host_pkg__action__Burger_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // robot_x
  if (lhs->robot_x != rhs->robot_x) {
    return false;
  }
  // robot_y
  if (lhs->robot_y != rhs->robot_y) {
    return false;
  }
  // robot_theta
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->robot_theta), &(rhs->robot_theta)))
  {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
host_pkg__action__Burger_Feedback__copy(
  const host_pkg__action__Burger_Feedback * input,
  host_pkg__action__Burger_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // robot_x
  output->robot_x = input->robot_x;
  // robot_y
  output->robot_y = input->robot_y;
  // robot_theta
  if (!rosidl_runtime_c__String__copy(
      &(input->robot_theta), &(output->robot_theta)))
  {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

host_pkg__action__Burger_Feedback *
host_pkg__action__Burger_Feedback__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_Feedback * msg = (host_pkg__action__Burger_Feedback *)allocator.allocate(sizeof(host_pkg__action__Burger_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(host_pkg__action__Burger_Feedback));
  bool success = host_pkg__action__Burger_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
host_pkg__action__Burger_Feedback__destroy(host_pkg__action__Burger_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    host_pkg__action__Burger_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
host_pkg__action__Burger_Feedback__Sequence__init(host_pkg__action__Burger_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_Feedback * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(host_pkg__action__Burger_Feedback)) {
      return false;
    }
    data = (host_pkg__action__Burger_Feedback *)allocator.zero_allocate(size, sizeof(host_pkg__action__Burger_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = host_pkg__action__Burger_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        host_pkg__action__Burger_Feedback__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
host_pkg__action__Burger_Feedback__Sequence__fini(host_pkg__action__Burger_Feedback__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      host_pkg__action__Burger_Feedback__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

host_pkg__action__Burger_Feedback__Sequence *
host_pkg__action__Burger_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_Feedback__Sequence * array = (host_pkg__action__Burger_Feedback__Sequence *)allocator.allocate(sizeof(host_pkg__action__Burger_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = host_pkg__action__Burger_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
host_pkg__action__Burger_Feedback__Sequence__destroy(host_pkg__action__Burger_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    host_pkg__action__Burger_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
host_pkg__action__Burger_Feedback__Sequence__are_equal(const host_pkg__action__Burger_Feedback__Sequence * lhs, const host_pkg__action__Burger_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!host_pkg__action__Burger_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
host_pkg__action__Burger_Feedback__Sequence__copy(
  const host_pkg__action__Burger_Feedback__Sequence * input,
  host_pkg__action__Burger_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(host_pkg__action__Burger_Feedback)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(host_pkg__action__Burger_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    host_pkg__action__Burger_Feedback * data =
      (host_pkg__action__Burger_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!host_pkg__action__Burger_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          host_pkg__action__Burger_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!host_pkg__action__Burger_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "host_pkg/action/detail/burger__functions.h"

bool
host_pkg__action__Burger_SendGoal_Request__init(host_pkg__action__Burger_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    host_pkg__action__Burger_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!host_pkg__action__Burger_Goal__init(&msg->goal)) {
    host_pkg__action__Burger_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
host_pkg__action__Burger_SendGoal_Request__fini(host_pkg__action__Burger_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  host_pkg__action__Burger_Goal__fini(&msg->goal);
}

bool
host_pkg__action__Burger_SendGoal_Request__are_equal(const host_pkg__action__Burger_SendGoal_Request * lhs, const host_pkg__action__Burger_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!host_pkg__action__Burger_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
host_pkg__action__Burger_SendGoal_Request__copy(
  const host_pkg__action__Burger_SendGoal_Request * input,
  host_pkg__action__Burger_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!host_pkg__action__Burger_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

host_pkg__action__Burger_SendGoal_Request *
host_pkg__action__Burger_SendGoal_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_SendGoal_Request * msg = (host_pkg__action__Burger_SendGoal_Request *)allocator.allocate(sizeof(host_pkg__action__Burger_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(host_pkg__action__Burger_SendGoal_Request));
  bool success = host_pkg__action__Burger_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
host_pkg__action__Burger_SendGoal_Request__destroy(host_pkg__action__Burger_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    host_pkg__action__Burger_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
host_pkg__action__Burger_SendGoal_Request__Sequence__init(host_pkg__action__Burger_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_SendGoal_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(host_pkg__action__Burger_SendGoal_Request)) {
      return false;
    }
    data = (host_pkg__action__Burger_SendGoal_Request *)allocator.zero_allocate(size, sizeof(host_pkg__action__Burger_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = host_pkg__action__Burger_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        host_pkg__action__Burger_SendGoal_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
host_pkg__action__Burger_SendGoal_Request__Sequence__fini(host_pkg__action__Burger_SendGoal_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      host_pkg__action__Burger_SendGoal_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

host_pkg__action__Burger_SendGoal_Request__Sequence *
host_pkg__action__Burger_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_SendGoal_Request__Sequence * array = (host_pkg__action__Burger_SendGoal_Request__Sequence *)allocator.allocate(sizeof(host_pkg__action__Burger_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = host_pkg__action__Burger_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
host_pkg__action__Burger_SendGoal_Request__Sequence__destroy(host_pkg__action__Burger_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    host_pkg__action__Burger_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
host_pkg__action__Burger_SendGoal_Request__Sequence__are_equal(const host_pkg__action__Burger_SendGoal_Request__Sequence * lhs, const host_pkg__action__Burger_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!host_pkg__action__Burger_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
host_pkg__action__Burger_SendGoal_Request__Sequence__copy(
  const host_pkg__action__Burger_SendGoal_Request__Sequence * input,
  host_pkg__action__Burger_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(host_pkg__action__Burger_SendGoal_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(host_pkg__action__Burger_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    host_pkg__action__Burger_SendGoal_Request * data =
      (host_pkg__action__Burger_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!host_pkg__action__Burger_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          host_pkg__action__Burger_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!host_pkg__action__Burger_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
host_pkg__action__Burger_SendGoal_Response__init(host_pkg__action__Burger_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    host_pkg__action__Burger_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
host_pkg__action__Burger_SendGoal_Response__fini(host_pkg__action__Burger_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
host_pkg__action__Burger_SendGoal_Response__are_equal(const host_pkg__action__Burger_SendGoal_Response * lhs, const host_pkg__action__Burger_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
host_pkg__action__Burger_SendGoal_Response__copy(
  const host_pkg__action__Burger_SendGoal_Response * input,
  host_pkg__action__Burger_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

host_pkg__action__Burger_SendGoal_Response *
host_pkg__action__Burger_SendGoal_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_SendGoal_Response * msg = (host_pkg__action__Burger_SendGoal_Response *)allocator.allocate(sizeof(host_pkg__action__Burger_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(host_pkg__action__Burger_SendGoal_Response));
  bool success = host_pkg__action__Burger_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
host_pkg__action__Burger_SendGoal_Response__destroy(host_pkg__action__Burger_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    host_pkg__action__Burger_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
host_pkg__action__Burger_SendGoal_Response__Sequence__init(host_pkg__action__Burger_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_SendGoal_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(host_pkg__action__Burger_SendGoal_Response)) {
      return false;
    }
    data = (host_pkg__action__Burger_SendGoal_Response *)allocator.zero_allocate(size, sizeof(host_pkg__action__Burger_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = host_pkg__action__Burger_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        host_pkg__action__Burger_SendGoal_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
host_pkg__action__Burger_SendGoal_Response__Sequence__fini(host_pkg__action__Burger_SendGoal_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      host_pkg__action__Burger_SendGoal_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

host_pkg__action__Burger_SendGoal_Response__Sequence *
host_pkg__action__Burger_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_SendGoal_Response__Sequence * array = (host_pkg__action__Burger_SendGoal_Response__Sequence *)allocator.allocate(sizeof(host_pkg__action__Burger_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = host_pkg__action__Burger_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
host_pkg__action__Burger_SendGoal_Response__Sequence__destroy(host_pkg__action__Burger_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    host_pkg__action__Burger_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
host_pkg__action__Burger_SendGoal_Response__Sequence__are_equal(const host_pkg__action__Burger_SendGoal_Response__Sequence * lhs, const host_pkg__action__Burger_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!host_pkg__action__Burger_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
host_pkg__action__Burger_SendGoal_Response__Sequence__copy(
  const host_pkg__action__Burger_SendGoal_Response__Sequence * input,
  host_pkg__action__Burger_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(host_pkg__action__Burger_SendGoal_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(host_pkg__action__Burger_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    host_pkg__action__Burger_SendGoal_Response * data =
      (host_pkg__action__Burger_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!host_pkg__action__Burger_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          host_pkg__action__Burger_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!host_pkg__action__Burger_SendGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "host_pkg/action/detail/burger__functions.h"

bool
host_pkg__action__Burger_SendGoal_Event__init(host_pkg__action__Burger_SendGoal_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    host_pkg__action__Burger_SendGoal_Event__fini(msg);
    return false;
  }
  // request
  if (!host_pkg__action__Burger_SendGoal_Request__Sequence__init(&msg->request, 0)) {
    host_pkg__action__Burger_SendGoal_Event__fini(msg);
    return false;
  }
  // response
  if (!host_pkg__action__Burger_SendGoal_Response__Sequence__init(&msg->response, 0)) {
    host_pkg__action__Burger_SendGoal_Event__fini(msg);
    return false;
  }
  return true;
}

void
host_pkg__action__Burger_SendGoal_Event__fini(host_pkg__action__Burger_SendGoal_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  host_pkg__action__Burger_SendGoal_Request__Sequence__fini(&msg->request);
  // response
  host_pkg__action__Burger_SendGoal_Response__Sequence__fini(&msg->response);
}

bool
host_pkg__action__Burger_SendGoal_Event__are_equal(const host_pkg__action__Burger_SendGoal_Event * lhs, const host_pkg__action__Burger_SendGoal_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!host_pkg__action__Burger_SendGoal_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!host_pkg__action__Burger_SendGoal_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
host_pkg__action__Burger_SendGoal_Event__copy(
  const host_pkg__action__Burger_SendGoal_Event * input,
  host_pkg__action__Burger_SendGoal_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!host_pkg__action__Burger_SendGoal_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!host_pkg__action__Burger_SendGoal_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

host_pkg__action__Burger_SendGoal_Event *
host_pkg__action__Burger_SendGoal_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_SendGoal_Event * msg = (host_pkg__action__Burger_SendGoal_Event *)allocator.allocate(sizeof(host_pkg__action__Burger_SendGoal_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(host_pkg__action__Burger_SendGoal_Event));
  bool success = host_pkg__action__Burger_SendGoal_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
host_pkg__action__Burger_SendGoal_Event__destroy(host_pkg__action__Burger_SendGoal_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    host_pkg__action__Burger_SendGoal_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
host_pkg__action__Burger_SendGoal_Event__Sequence__init(host_pkg__action__Burger_SendGoal_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_SendGoal_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(host_pkg__action__Burger_SendGoal_Event)) {
      return false;
    }
    data = (host_pkg__action__Burger_SendGoal_Event *)allocator.zero_allocate(size, sizeof(host_pkg__action__Burger_SendGoal_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = host_pkg__action__Burger_SendGoal_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        host_pkg__action__Burger_SendGoal_Event__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
host_pkg__action__Burger_SendGoal_Event__Sequence__fini(host_pkg__action__Burger_SendGoal_Event__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      host_pkg__action__Burger_SendGoal_Event__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

host_pkg__action__Burger_SendGoal_Event__Sequence *
host_pkg__action__Burger_SendGoal_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_SendGoal_Event__Sequence * array = (host_pkg__action__Burger_SendGoal_Event__Sequence *)allocator.allocate(sizeof(host_pkg__action__Burger_SendGoal_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = host_pkg__action__Burger_SendGoal_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
host_pkg__action__Burger_SendGoal_Event__Sequence__destroy(host_pkg__action__Burger_SendGoal_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    host_pkg__action__Burger_SendGoal_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
host_pkg__action__Burger_SendGoal_Event__Sequence__are_equal(const host_pkg__action__Burger_SendGoal_Event__Sequence * lhs, const host_pkg__action__Burger_SendGoal_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!host_pkg__action__Burger_SendGoal_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
host_pkg__action__Burger_SendGoal_Event__Sequence__copy(
  const host_pkg__action__Burger_SendGoal_Event__Sequence * input,
  host_pkg__action__Burger_SendGoal_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(host_pkg__action__Burger_SendGoal_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(host_pkg__action__Burger_SendGoal_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    host_pkg__action__Burger_SendGoal_Event * data =
      (host_pkg__action__Burger_SendGoal_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!host_pkg__action__Burger_SendGoal_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          host_pkg__action__Burger_SendGoal_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!host_pkg__action__Burger_SendGoal_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
host_pkg__action__Burger_GetResult_Request__init(host_pkg__action__Burger_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    host_pkg__action__Burger_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
host_pkg__action__Burger_GetResult_Request__fini(host_pkg__action__Burger_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
host_pkg__action__Burger_GetResult_Request__are_equal(const host_pkg__action__Burger_GetResult_Request * lhs, const host_pkg__action__Burger_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
host_pkg__action__Burger_GetResult_Request__copy(
  const host_pkg__action__Burger_GetResult_Request * input,
  host_pkg__action__Burger_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

host_pkg__action__Burger_GetResult_Request *
host_pkg__action__Burger_GetResult_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_GetResult_Request * msg = (host_pkg__action__Burger_GetResult_Request *)allocator.allocate(sizeof(host_pkg__action__Burger_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(host_pkg__action__Burger_GetResult_Request));
  bool success = host_pkg__action__Burger_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
host_pkg__action__Burger_GetResult_Request__destroy(host_pkg__action__Burger_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    host_pkg__action__Burger_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
host_pkg__action__Burger_GetResult_Request__Sequence__init(host_pkg__action__Burger_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_GetResult_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(host_pkg__action__Burger_GetResult_Request)) {
      return false;
    }
    data = (host_pkg__action__Burger_GetResult_Request *)allocator.zero_allocate(size, sizeof(host_pkg__action__Burger_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = host_pkg__action__Burger_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        host_pkg__action__Burger_GetResult_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
host_pkg__action__Burger_GetResult_Request__Sequence__fini(host_pkg__action__Burger_GetResult_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      host_pkg__action__Burger_GetResult_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

host_pkg__action__Burger_GetResult_Request__Sequence *
host_pkg__action__Burger_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_GetResult_Request__Sequence * array = (host_pkg__action__Burger_GetResult_Request__Sequence *)allocator.allocate(sizeof(host_pkg__action__Burger_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = host_pkg__action__Burger_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
host_pkg__action__Burger_GetResult_Request__Sequence__destroy(host_pkg__action__Burger_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    host_pkg__action__Burger_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
host_pkg__action__Burger_GetResult_Request__Sequence__are_equal(const host_pkg__action__Burger_GetResult_Request__Sequence * lhs, const host_pkg__action__Burger_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!host_pkg__action__Burger_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
host_pkg__action__Burger_GetResult_Request__Sequence__copy(
  const host_pkg__action__Burger_GetResult_Request__Sequence * input,
  host_pkg__action__Burger_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(host_pkg__action__Burger_GetResult_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(host_pkg__action__Burger_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    host_pkg__action__Burger_GetResult_Request * data =
      (host_pkg__action__Burger_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!host_pkg__action__Burger_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          host_pkg__action__Burger_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!host_pkg__action__Burger_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "host_pkg/action/detail/burger__functions.h"

bool
host_pkg__action__Burger_GetResult_Response__init(host_pkg__action__Burger_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!host_pkg__action__Burger_Result__init(&msg->result)) {
    host_pkg__action__Burger_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
host_pkg__action__Burger_GetResult_Response__fini(host_pkg__action__Burger_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  host_pkg__action__Burger_Result__fini(&msg->result);
}

bool
host_pkg__action__Burger_GetResult_Response__are_equal(const host_pkg__action__Burger_GetResult_Response * lhs, const host_pkg__action__Burger_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!host_pkg__action__Burger_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
host_pkg__action__Burger_GetResult_Response__copy(
  const host_pkg__action__Burger_GetResult_Response * input,
  host_pkg__action__Burger_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!host_pkg__action__Burger_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

host_pkg__action__Burger_GetResult_Response *
host_pkg__action__Burger_GetResult_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_GetResult_Response * msg = (host_pkg__action__Burger_GetResult_Response *)allocator.allocate(sizeof(host_pkg__action__Burger_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(host_pkg__action__Burger_GetResult_Response));
  bool success = host_pkg__action__Burger_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
host_pkg__action__Burger_GetResult_Response__destroy(host_pkg__action__Burger_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    host_pkg__action__Burger_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
host_pkg__action__Burger_GetResult_Response__Sequence__init(host_pkg__action__Burger_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_GetResult_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(host_pkg__action__Burger_GetResult_Response)) {
      return false;
    }
    data = (host_pkg__action__Burger_GetResult_Response *)allocator.zero_allocate(size, sizeof(host_pkg__action__Burger_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = host_pkg__action__Burger_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        host_pkg__action__Burger_GetResult_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
host_pkg__action__Burger_GetResult_Response__Sequence__fini(host_pkg__action__Burger_GetResult_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      host_pkg__action__Burger_GetResult_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

host_pkg__action__Burger_GetResult_Response__Sequence *
host_pkg__action__Burger_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_GetResult_Response__Sequence * array = (host_pkg__action__Burger_GetResult_Response__Sequence *)allocator.allocate(sizeof(host_pkg__action__Burger_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = host_pkg__action__Burger_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
host_pkg__action__Burger_GetResult_Response__Sequence__destroy(host_pkg__action__Burger_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    host_pkg__action__Burger_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
host_pkg__action__Burger_GetResult_Response__Sequence__are_equal(const host_pkg__action__Burger_GetResult_Response__Sequence * lhs, const host_pkg__action__Burger_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!host_pkg__action__Burger_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
host_pkg__action__Burger_GetResult_Response__Sequence__copy(
  const host_pkg__action__Burger_GetResult_Response__Sequence * input,
  host_pkg__action__Burger_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(host_pkg__action__Burger_GetResult_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(host_pkg__action__Burger_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    host_pkg__action__Burger_GetResult_Response * data =
      (host_pkg__action__Burger_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!host_pkg__action__Burger_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          host_pkg__action__Burger_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!host_pkg__action__Burger_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
// already included above
// #include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "host_pkg/action/detail/burger__functions.h"

bool
host_pkg__action__Burger_GetResult_Event__init(host_pkg__action__Burger_GetResult_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    host_pkg__action__Burger_GetResult_Event__fini(msg);
    return false;
  }
  // request
  if (!host_pkg__action__Burger_GetResult_Request__Sequence__init(&msg->request, 0)) {
    host_pkg__action__Burger_GetResult_Event__fini(msg);
    return false;
  }
  // response
  if (!host_pkg__action__Burger_GetResult_Response__Sequence__init(&msg->response, 0)) {
    host_pkg__action__Burger_GetResult_Event__fini(msg);
    return false;
  }
  return true;
}

void
host_pkg__action__Burger_GetResult_Event__fini(host_pkg__action__Burger_GetResult_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  host_pkg__action__Burger_GetResult_Request__Sequence__fini(&msg->request);
  // response
  host_pkg__action__Burger_GetResult_Response__Sequence__fini(&msg->response);
}

bool
host_pkg__action__Burger_GetResult_Event__are_equal(const host_pkg__action__Burger_GetResult_Event * lhs, const host_pkg__action__Burger_GetResult_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!host_pkg__action__Burger_GetResult_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!host_pkg__action__Burger_GetResult_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
host_pkg__action__Burger_GetResult_Event__copy(
  const host_pkg__action__Burger_GetResult_Event * input,
  host_pkg__action__Burger_GetResult_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!host_pkg__action__Burger_GetResult_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!host_pkg__action__Burger_GetResult_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

host_pkg__action__Burger_GetResult_Event *
host_pkg__action__Burger_GetResult_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_GetResult_Event * msg = (host_pkg__action__Burger_GetResult_Event *)allocator.allocate(sizeof(host_pkg__action__Burger_GetResult_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(host_pkg__action__Burger_GetResult_Event));
  bool success = host_pkg__action__Burger_GetResult_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
host_pkg__action__Burger_GetResult_Event__destroy(host_pkg__action__Burger_GetResult_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    host_pkg__action__Burger_GetResult_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
host_pkg__action__Burger_GetResult_Event__Sequence__init(host_pkg__action__Burger_GetResult_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_GetResult_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(host_pkg__action__Burger_GetResult_Event)) {
      return false;
    }
    data = (host_pkg__action__Burger_GetResult_Event *)allocator.zero_allocate(size, sizeof(host_pkg__action__Burger_GetResult_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = host_pkg__action__Burger_GetResult_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        host_pkg__action__Burger_GetResult_Event__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
host_pkg__action__Burger_GetResult_Event__Sequence__fini(host_pkg__action__Burger_GetResult_Event__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      host_pkg__action__Burger_GetResult_Event__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

host_pkg__action__Burger_GetResult_Event__Sequence *
host_pkg__action__Burger_GetResult_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_GetResult_Event__Sequence * array = (host_pkg__action__Burger_GetResult_Event__Sequence *)allocator.allocate(sizeof(host_pkg__action__Burger_GetResult_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = host_pkg__action__Burger_GetResult_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
host_pkg__action__Burger_GetResult_Event__Sequence__destroy(host_pkg__action__Burger_GetResult_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    host_pkg__action__Burger_GetResult_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
host_pkg__action__Burger_GetResult_Event__Sequence__are_equal(const host_pkg__action__Burger_GetResult_Event__Sequence * lhs, const host_pkg__action__Burger_GetResult_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!host_pkg__action__Burger_GetResult_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
host_pkg__action__Burger_GetResult_Event__Sequence__copy(
  const host_pkg__action__Burger_GetResult_Event__Sequence * input,
  host_pkg__action__Burger_GetResult_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(host_pkg__action__Burger_GetResult_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(host_pkg__action__Burger_GetResult_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    host_pkg__action__Burger_GetResult_Event * data =
      (host_pkg__action__Burger_GetResult_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!host_pkg__action__Burger_GetResult_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          host_pkg__action__Burger_GetResult_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!host_pkg__action__Burger_GetResult_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "host_pkg/action/detail/burger__functions.h"

bool
host_pkg__action__Burger_FeedbackMessage__init(host_pkg__action__Burger_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    host_pkg__action__Burger_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!host_pkg__action__Burger_Feedback__init(&msg->feedback)) {
    host_pkg__action__Burger_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
host_pkg__action__Burger_FeedbackMessage__fini(host_pkg__action__Burger_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  host_pkg__action__Burger_Feedback__fini(&msg->feedback);
}

bool
host_pkg__action__Burger_FeedbackMessage__are_equal(const host_pkg__action__Burger_FeedbackMessage * lhs, const host_pkg__action__Burger_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!host_pkg__action__Burger_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
host_pkg__action__Burger_FeedbackMessage__copy(
  const host_pkg__action__Burger_FeedbackMessage * input,
  host_pkg__action__Burger_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!host_pkg__action__Burger_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

host_pkg__action__Burger_FeedbackMessage *
host_pkg__action__Burger_FeedbackMessage__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_FeedbackMessage * msg = (host_pkg__action__Burger_FeedbackMessage *)allocator.allocate(sizeof(host_pkg__action__Burger_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(host_pkg__action__Burger_FeedbackMessage));
  bool success = host_pkg__action__Burger_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
host_pkg__action__Burger_FeedbackMessage__destroy(host_pkg__action__Burger_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    host_pkg__action__Burger_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
host_pkg__action__Burger_FeedbackMessage__Sequence__init(host_pkg__action__Burger_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_FeedbackMessage * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(host_pkg__action__Burger_FeedbackMessage)) {
      return false;
    }
    data = (host_pkg__action__Burger_FeedbackMessage *)allocator.zero_allocate(size, sizeof(host_pkg__action__Burger_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = host_pkg__action__Burger_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        host_pkg__action__Burger_FeedbackMessage__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
host_pkg__action__Burger_FeedbackMessage__Sequence__fini(host_pkg__action__Burger_FeedbackMessage__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      host_pkg__action__Burger_FeedbackMessage__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

host_pkg__action__Burger_FeedbackMessage__Sequence *
host_pkg__action__Burger_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  host_pkg__action__Burger_FeedbackMessage__Sequence * array = (host_pkg__action__Burger_FeedbackMessage__Sequence *)allocator.allocate(sizeof(host_pkg__action__Burger_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = host_pkg__action__Burger_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
host_pkg__action__Burger_FeedbackMessage__Sequence__destroy(host_pkg__action__Burger_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    host_pkg__action__Burger_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
host_pkg__action__Burger_FeedbackMessage__Sequence__are_equal(const host_pkg__action__Burger_FeedbackMessage__Sequence * lhs, const host_pkg__action__Burger_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!host_pkg__action__Burger_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
host_pkg__action__Burger_FeedbackMessage__Sequence__copy(
  const host_pkg__action__Burger_FeedbackMessage__Sequence * input,
  host_pkg__action__Burger_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(host_pkg__action__Burger_FeedbackMessage)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(host_pkg__action__Burger_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    host_pkg__action__Burger_FeedbackMessage * data =
      (host_pkg__action__Burger_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!host_pkg__action__Burger_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          host_pkg__action__Burger_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!host_pkg__action__Burger_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
