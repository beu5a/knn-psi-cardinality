#include "psi_node.h"
#include "gtest/gtest.h"

#include "absl/memory/memory.h"
#include "absl/strings/escaping.h"
#include "absl/strings/str_cat.h"



using private_set_intersection::PsiNode;


TEST(PsiNodeTest, BasicTest) {
  // Create a new PsiNode object
    auto node01 = PsiNode::CreateWithNewKey();
    auto node02 = PsiNode::CreateWithNewKey();

    auto node1 = std::move(node01.value());
    auto node2 = std::move(node02.value());


  // Define the inputs for the PsiNode
  std::vector<std::string> inputs01{"foo", "bar", "baz","match"};
  std::vector<std::string> inputs02{"foo", "bar", "test","xy","match"};
  absl::Span<const std::string> inputs1(inputs01.data(), inputs01.size());
  absl::Span<const std::string> inputs2(inputs02.data(), inputs02.size());



  // Generate a request protobuf with the encrypted inputs
  auto request = std::move(node1->CreateRequest(inputs1).value());




  // Process the request and generate a response protobuf
  auto response = std::move(node2->ProcessRequest(request, inputs2).value());

  auto result = node1->ProcessResponse(response);

  // Check that the response has the correct number of elements
    EXPECT_EQ(result.value(),3);
}
