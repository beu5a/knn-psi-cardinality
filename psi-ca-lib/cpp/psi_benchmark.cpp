#include "psi_node.h"

#include "benchmark/benchmark.h"
#include "absl/memory/memory.h"
#include "absl/strings/escaping.h"
#include "absl/strings/str_cat.h"

using private_set_intersection::PsiNode;



static void BM_PsiNodeCreateRequest(benchmark::State& state) {
  // Create a new PsiNode object
  auto node01 = PsiNode::CreateWithNewKey();
  auto node02 = PsiNode::CreateWithNewKey();

  auto node1 = std::move(node01.value());
  auto node2 = std::move(node02.value());

  for (auto _ : state) {
    std::vector<std::string> inputs(state.range(0));
    for (int i = 0; i < state.range(0); ++i) {
      inputs[i] = absl::StrCat("input", i);
    }
    absl::Span<const std::string> span_inputs(inputs.data(), inputs.size());

    // Generate a request protobuf with the encrypted inputs
    auto request = std::move(node1->CreateRequest(span_inputs).value());

    benchmark::DoNotOptimize(request);
  }
}

static void BM_PsiNodeProcessRequest(benchmark::State& state) {
  // Create a new PsiNode object
  auto node01 = PsiNode::CreateWithNewKey();
  auto node02 = PsiNode::CreateWithNewKey();

  auto node1 = std::move(node01.value());
  auto node2 = std::move(node02.value());

  std::vector<std::string> inputs1{"input1", "input2", "input3", "input4"};
  absl::Span<const std::string> span_inputs1(inputs1.data(), inputs1.size());

  for (auto _ : state) {
    std::vector<std::string> inputs2(state.range(0));
    for (int i = 0; i < state.range(0); ++i) {
      inputs2[i] = absl::StrCat("input", i);
    }
    absl::Span<const std::string> span_inputs2(inputs2.data(), inputs2.size());

    // Generate a request protobuf with the encrypted inputs
    auto request = std::move(node1->CreateRequest(span_inputs1).value());

    // Process the request and generate a response protobuf
    auto response = std::move(node2->ProcessRequest(request, span_inputs2).value());

    benchmark::DoNotOptimize(response);
  }
}

static void BM_PsiNodeProcessResponse(benchmark::State& state) {
  // Create a new PsiNode object
  auto node01 = PsiNode::CreateWithNewKey();
  auto node02 = PsiNode::CreateWithNewKey();

  auto node1 = std::move(node01.value());
  auto node2 = std::move(node02.value());

  std::vector<std::string> inputs1(state.range(0));
  for (int i = 0; i < state.range(0); ++i) {
    inputs1[i] = absl::StrCat("input", i);
  }
  absl::Span<const std::string> span_inputs1(inputs1.data(), inputs1.size());

  std::vector<std::string> inputs2(state.range(0));
  for (int i = 0; i < state.range(0); ++i) {
    inputs2[i] = absl::StrCat("input", i);
  }
  absl::Span<const std::string> span_inputs2(inputs2.data(), inputs2.size());

  // Generate a request protobuf with the encrypted inputs
  auto request = std::move(node1->CreateRequest(span_inputs1).value());

  // Process the request and generate a response protobuf
  auto response = std::move(node2->ProcessRequest(request, span_inputs2).value());

  for (auto _ : state) {
    // Process the response
    auto result = node1->ProcessResponse(response);

    benchmark::DoNotOptimize(result);
  }
}


// Register the benchmarks
BENCHMARK(BM_PsiNodeCreateRequest)->Arg(5)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeCreateRequest)->Arg(10)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeCreateRequest)->Arg(50)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeCreateRequest)->Arg(100)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeCreateRequest)->Arg(500)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeCreateRequest)->Arg(1000)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeCreateRequest)->Arg(5000)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeCreateRequest)->Arg(10000)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeCreateRequest)->Arg(50000)->Unit(benchmark::kMillisecond);



BENCHMARK(BM_PsiNodeProcessRequest)->Arg(5)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessRequest)->Arg(10)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessRequest)->Arg(50)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessRequest)->Arg(100)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessRequest)->Arg(500)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessRequest)->Arg(1000)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessRequest)->Arg(5000)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessRequest)->Arg(10000)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessRequest)->Arg(50000)->Unit(benchmark::kMillisecond);



BENCHMARK(BM_PsiNodeProcessResponse)->Arg(5)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessResponse)->Arg(10)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessResponse)->Arg(50)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessResponse)->Arg(100)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessResponse)->Arg(500)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessResponse)->Arg(1000)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessResponse)->Arg(5000)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessResponse)->Arg(10000)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_PsiNodeProcessResponse)->Arg(50000)->Unit(benchmark::kMillisecond);


int main(int argc, char** argv) {
  benchmark::Initialize(&argc, argv);
  benchmark::RunSpecifiedBenchmarks();
}
