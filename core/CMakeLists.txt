###########################################################
##               BlackBook project
###########################################################

# Core library
set(BBCORE_SOURCE_FILES
	bbMainWindow.cpp
	bbMainWindow.h
	bbCostSplitCalculator.h
	bbCostSplitCalculator.cpp
	)
QT4_WRAP_CPP(BBCORE_SOURCE_FILES  bbMainWindow.h)
add_library( bbCore ${BBCORE_SOURCE_FILES} )
target_link_libraries( bbCore ${QT_LIBRARIES} )

if (BUILD_TESTING)
#	QT4_WRAP_CPP(CXTEST_VIDEOSERVICE_SOURCES
#		)
	set(BBTEST_CORE_SOURCES ${BBTEST_CORE_SOURCES}
		bbCostSplitCalculatorTest.cpp
		)
	cx_catch_add_lib_and_exe(bbCore "${BBTEST_CORE_SOURCES}")
endif (BUILD_TESTING)
