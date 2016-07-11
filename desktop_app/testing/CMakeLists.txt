###########################################################
#               cxTestUtilities
#
# Utilities library for testing.
# Contains the catch unit test framework.
# Add all system-wide test utilities here.
###########################################################

cmake_minimum_required( VERSION 2.6 )

if(COMMAND cmake_policy)
  cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

if (BUILD_TESTING)
	set(BB_TESTUTILITIES_SOURCE_FILES
		bbCostSplitCalculatorTest.cpp
		bbtestCatchImpl.h
		bbtestCatchImpl.cpp
		bbtestCatchMain.cpp
		${BB_TESTUTILITIES_SOURCE_FILES}
            )
	include_directories(
	    .
		${PROJECT_SOURCE_DIR}/catch
	    )
		add_executable( bbtest ${BB_TESTUTILITIES_SOURCE_FILES} )
		target_link_libraries(bbtest bbCore  Qt5::Widgets Qt5::Xml)
endif (BUILD_TESTING)
