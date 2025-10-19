#!/bin/bash
echo "Verify mn, ovs-ofctl, and ryu-manager are available"
echo "> mn --version"
mn --version
echo "> ovs-ofctl --version"
ovs-ofctl --version
echo "> ryu-manager --version"
ryu-manager --version