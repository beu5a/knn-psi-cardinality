#ifndef PRIVATE_SET_INTERSECTION_CPP_RAW_H_
#define PRIVATE_SET_INTERSECTION_CPP_RAW_H_

#include <vector>

#include "absl/status/statusor.h"
#include "absl/types/span.h"
#include "private_join_and_compute/crypto/context.h"
#include "proto/psi.pb.h"

namespace private_set_intersection {

using absl::StatusOr;

// Container for holding the raw encrypted elements.
class Raw {
 public:
  Raw() = delete;
 
 private:
};

}  // namespace private_set_intersection

#endif  // PRIVATE_SET_INTERSECTION_CPP_RAW_H_
