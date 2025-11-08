# =============================================================================
# Project: SOLIS
# 
# Configuration file for this project
# 
# Author    Meltwin (github@meltwin.fr)
# Date      08/11/2025 (created 20/10/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025 
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================

cmake_minimum_required(VERSION 3.25)
project(solis)

find_package(solis_cmake REQUIRED)

add_solis_python(solis.app "solis_app")
add_solis_script(LINUX FILES "bin/solis")

solis_install()