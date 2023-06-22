#!/bin/bash

# Add Bazel distribution URI as a package source
echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list

# Download and install the Bazel signing key
curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -

# Update the package lists
sudo apt update

# Install Bazel
sudo apt install bazel
sudo apt install bazel-6.0.0

# Verify the installation
bazel version
