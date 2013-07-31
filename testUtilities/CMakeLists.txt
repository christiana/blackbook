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
#        QT4_WRAP_CPP( CX_TESTUTILITIES_SOURCE_FILES
#            )
	set(BB_TESTUTILITIES_SOURCE_FILES
		bbtestCatchImpl.h
		bbtestCatchImpl.cpp
		${BB_TESTUTILITIES_SOURCE_FILES}
            )
	include_directories(
	    .
		${PROJECT_SOURCE_DIR}/catch
	    )
		add_library( bbtestUtilities ${BB_TESTUTILITIES_SOURCE_FILES} )
		target_link_libraries(bbtestUtilities ${QT_LIBRARIES})
endif (BUILD_TESTING)
