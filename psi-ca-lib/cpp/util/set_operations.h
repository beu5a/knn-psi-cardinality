#pragma once

#include <string>
#include <vector>
#include <unordered_map>







namespace private_set_intersection{


int intersection_cardinality(const std::vector<std::string>& arr1, const std::vector<std::string>& arr2) {
    std::unordered_map<std::string, int> freq;
    for (const auto& num : arr1) {
        freq[num]++;
    }
    int cnt = 0;
    for (const auto& num : arr2) {
        if (freq[num] > 0) {
            cnt++;
            freq[num]--;
        }
    }
    return cnt;
}

}