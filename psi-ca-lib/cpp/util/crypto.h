#pragma once

#include <string>
#include <vector>
#include <sstream>



#include "absl/status/statusor.h"
#include "openssl/obj_mac.h"
#include "openssl/evp.h"
#include "openssl/sha.h"




namespace private_set_intersection{

using absl::StatusOr;

static EVP_MD_CTX* mdctx = nullptr;

absl::StatusOr<std::string> sha256_hash_string(std::string& str){
  // Initialize a SHA-256 context
    if (mdctx == nullptr) {
        mdctx = EVP_MD_CTX_new();
        if (mdctx == nullptr) {
            return absl::InternalError("Failed to initialize EVP_MD_CTX");
        }
    }

    EVP_DigestInit_ex(mdctx, EVP_sha256(), nullptr);

    // Feed the input string to the context
    if (EVP_DigestUpdate(mdctx, str.data(), str.size()) != 1) {
        return absl::InternalError("Failed to update SHA-256 context");
    }

    // Finalize the hash and obtain the output
    std::vector<uint8_t> hash(EVP_MD_size(EVP_sha256()));
    unsigned int hash_len = 0;
    if (EVP_DigestFinal_ex(mdctx, hash.data(), &hash_len) != 1) {
        return absl::InternalError("Failed to finalize SHA-256 context");
    }

    // Convert the hash to a hex-encoded string
    std::stringstream ss;
    ss << std::hex << std::setfill('0');
    for (const auto& byte : hash) {
        ss << std::setw(2) << static_cast<int>(byte);
    }
    std::string hex_string = ss.str();

    // Reset the context for the next hash
    if (EVP_MD_CTX_reset(mdctx) != 1) {
        return absl::InternalError("Failed to reset SHA-256 context");
    }

    // Return the hex-encoded hash
    return hex_string;
}


absl::Status sha256_cleanup() {
    if (EVP_MD_CTX_reset(mdctx) != 1) {
        return absl::InternalError("Failed to reset SHA-256 context");
    }
    return absl::OkStatus();
}



}