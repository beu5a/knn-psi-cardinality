#ifndef PRIVATE_SET_INTERSECTION_CPP_PSI_NODE_H_
#define PRIVATE_SET_INTERSECTION_CPP_PSI_NODE_H_


#include "absl/status/statusor.h"
#include "absl/types/span.h"
#include "private_join_and_compute/crypto/ec_commutative_cipher.h"
#include "proto/psi.pb.h"





namespace private_set_intersection {

using absl::StatusOr;

class PsiNode {
 public:
  PsiNode() = delete;
  static StatusOr<std::unique_ptr<PsiNode>> CreateWithNewKey();
  static StatusOr<std::unique_ptr<PsiNode>> CreateFromKey(const std::string& key_bytes);

  StatusOr<psi_proto::Request> CreateRequest(absl::Span<const std::string> inputs) const;
  StatusOr<psi_proto::Response> ProcessRequest(const psi_proto::Request& client_request,absl::Span<const std::string> inputs) const; 
  StatusOr<int64_t> ProcessResponse(const psi_proto::Response& server_response) const;

  std::string GetPrivateKeyBytes() const;



 private:
    explicit PsiNode(
      std::unique_ptr<::private_join_and_compute::ECCommutativeCipher> ec_cipher);
      std::unique_ptr<::private_join_and_compute::ECCommutativeCipher> ec_cipher_;

};

}  // namespace private_set_intersection
#endif 
