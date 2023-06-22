
#include "cpp/psi_node.h"

#include <random>
#include <string>
#include <sstream>
#include <iomanip>
#include <vector>
#include <unordered_map>



#include "absl/memory/memory.h"
#include "absl/strings/escaping.h"
#include "absl/strings/str_cat.h"
#include "openssl/obj_mac.h"
#include "openssl/evp.h"
#include "openssl/sha.h"


#include "cpp/util/crypto.h"
#include "cpp/util/set_operations.h"
#include "proto/psi.pb.h"
#include "psi_node.h"


//TODO ADD METHOD FOR SENDING RESULT ?


namespace private_set_intersection {

/**
 * @brief Construct a new Psi Client:: Psi Client object
 * @param ec_cipher A unique pointer to a commutative , which is used for
 * encryption and decryption in the Private Set Intersection (PSI) protocol.
 * @param reveal_intersection A boolean value indicating whether the
 * intersection of the two sets should be revealed after the PSI protocol is
 * completed.
 */
PsiNode::PsiNode(
    std::unique_ptr<::private_join_and_compute::ECCommutativeCipher> ec_cipher)
    : ec_cipher_(std::move(ec_cipher)) {}



/**
 * @brief Creates a new instance of the PsiNode class with a new key pair for
 * encryption and decryption using ECCommutativeCipher.
 * @return StatusOr<std::unique_ptr<PsiNode>>
 */
StatusOr<std::unique_ptr<PsiNode>> PsiNode::CreateWithNewKey() {
  // Create an EC cipher with curve P-256. This gives 128 bits of security.
  ASSIGN_OR_RETURN(
      auto ec_cipher,
      ::private_join_and_compute::ECCommutativeCipher::CreateWithNewKey(
          NID_X9_62_prime256v1,
          ::private_join_and_compute::ECCommutativeCipher::HashType::SHA256));

  // Create a new instance of the PsiNode class using the ECCommutativeCipher
  // object and the reveal_intersection boolean.
  return absl::WrapUnique(
      new PsiNode(std::move(ec_cipher)));
}

/**
 * @brief Creates a new PsiNode instance using an EC cipher created from the
 * provided key.
 *
 * @param key_bytes The bytes representing the key for the EC cipher.
 * @param reveal_intersection A boolean flag indicating whether the intersection
 * should be revealed.
 * @return StatusOr<std::unique_ptr<PsiNode>>
 */
StatusOr<std::unique_ptr<PsiNode>> PsiNode::CreateFromKey(
    const std::string& key_bytes) {
  // Create an EC cipher with curve P-256. This gives 128 bits of security.
  ASSIGN_OR_RETURN(
      auto ec_cipher,
      ::private_join_and_compute::ECCommutativeCipher::CreateFromKey(
          NID_X9_62_prime256v1, key_bytes,
          ::private_join_and_compute::ECCommutativeCipher::HashType::SHA256));
  return absl::WrapUnique(
      new PsiNode(std::move(ec_cipher)));
}


/**
 * @brief Creates a request protobuf with encrypted inputs.
 * 
 * @param inputs The inputs to encrypt and add to the request protobuf.
 *
 * @return StatusOr<psi_proto::Request>
 */
StatusOr<psi_proto::Request> PsiNode::CreateRequest(
    absl::Span<const std::string> inputs) const {
  // Encrypt inputs one by one.
  int64_t input_size = static_cast<int64_t>(inputs.size());
  std::vector<std::string> encrypted_inputs(input_size);


  // Node hashes its items into the EC and masks them with a secret random value 
  for (int64_t i = 0; i < input_size; i++) {
    ASSIGN_OR_RETURN( encrypted_inputs[i], ec_cipher_->Encrypt(inputs[i]));
  }

  // Create a request protobuf
  psi_proto::Request request;

  // Add the encrypted elements 
  for (int64_t i = 0; i < input_size; i++) {
    request.add_elements(encrypted_inputs[i]);
  }

  return request;
}



/**
 * @brief Processes another node's request and returns a response containing 
 * shuffled values (a′_{i}) and the output of the hash function ts_{i} = H'(bs_{j})).
 * @param request The encrypted elements to process
 * @param inputs The inputs to encrypt and add to the request protobuf.
 * @return StatusOr<psi_proto::Response>
 */
StatusOr<psi_proto::Response> PsiNode::ProcessRequest(
    const psi_proto::Request& request,
    absl::Span<const std::string> inputs) const {
    
  // Check if the request is initialized
  if (!request.IsInitialized()) {
    return absl::InvalidArgumentError("request is corrupt!");
  }


  int64_t input_size = static_cast<int64_t>(inputs.size());
  std::vector<std::string> encrypted_hashes(input_size);
   
  
  
  // Node hashes its items into the EC and masks them with a secret random value then hashes the result
  for (int64_t i = 0; i < input_size; i++) {
    ASSIGN_OR_RETURN(std::string enc, ec_cipher_->Encrypt(inputs[i]));
    ASSIGN_OR_RETURN(encrypted_hashes[i], sha256_hash_string(enc)); 
  }
  

  // Shuffle the hashes
  std::random_device rd0;
  std::mt19937 g0(rd0());
  std::shuffle(encrypted_hashes.begin(), encrypted_hashes.end(), g0);

  // Create the response
  psi_proto::Response response;

  for (int64_t i = 0; i < input_size; i++) {
    response.mutable_hashed()->add_elements(encrypted_hashes[i]);
  }


  // Get the encrypted elements from the request
  const auto& encrypted_elements = request.elements();
  const std::int64_t num_client_elements =
      static_cast<std::int64_t>(encrypted_elements.size());



  // Re-encrypt the request's elements and add to the response
  for (int i = 0; i < num_client_elements; i++) {
    ASSIGN_OR_RETURN(std::string encrypted,
                     ec_cipher_->ReEncrypt(encrypted_elements[i]));
    response.mutable_masked()->add_elements(encrypted);
  }

  
  std::random_device rd;
  std::mt19937 g(rd());
  
 // Get mutable reference to encrypted_elements array and shuffle it.
  auto& elements = *(response.mutable_masked()->mutable_elements());
  std::shuffle(elements.begin(), elements.end(), g);

  sha256_cleanup();
  return response;

}



/**
 * @brief Process the node's response to obtain the intersection
 * @param response The previous response
 * @return StatusOr<std::vector<int64_t>>
 */
StatusOr<int64_t> PsiNode::ProcessResponse(
    const psi_proto::Response& response) const {


  if (!response.IsInitialized()) {
    return absl::InvalidArgumentError("response is corrupt!");
  }

  
  const auto& response_masked = response.masked().elements();
  const auto& response_hashed = response.hashed().elements();


  const std::int64_t masked_size = static_cast<std::int64_t>(response_masked.size());
  const std::int64_t hashed_size = static_cast<std::int64_t>(response_hashed.size());


  std::vector<std::string> decrypted_hashed;
  decrypted_hashed.reserve(masked_size);


  for (int64_t i = 0; i < masked_size; i++) {
    ASSIGN_OR_RETURN(std::string decrypted_elem,
                     ec_cipher_->Decrypt(response_masked[i]));

    ASSIGN_OR_RETURN(std::string hashed_elem,
                     sha256_hash_string(decrypted_elem));
    decrypted_hashed.push_back(hashed_elem);
  }


  std::vector<std::string> other_hashed;
  other_hashed.reserve(hashed_size);

  for (const auto& h : response_hashed) {
    other_hashed.emplace_back(h);
  }


  sha256_cleanup();
  return intersection_cardinality(decrypted_hashed, other_hashed);   
}



/**
 * @brief Get the client's private key
 *
 * @return The private key as a null-terminated binary string
 */
std::string PsiNode::GetPrivateKeyBytes() const {
  std::string key = ec_cipher_->GetPrivateKeyBytes();
  key.insert(key.begin(), 32 - key.length(), '\0');
  return key;
}



}  // namespace private_set_intersection
