###############################################################################
# Initialize Boost library
# Find the package.
###############################################################################
macro(cx_initialize_Boost)
	find_package( Boost REQUIRED )
	include_directories( ${Boost_INCLUDE_DIRS} )
endmacro()

###############################################################################
# Initialize Qt library
# Find the package and run the include USE file.
###############################################################################
macro(cx_initialize_QT)
	set(QT_USE_QTXML TRUE)
	set(QT_USE_QTTEST TRUE)
	find_package(Qt4 REQUIRED)
	if(QT_USE_FILE)
		include(${QT_USE_FILE})
	else(QT_USE_FILE)
		set(QT_LIBRARIES  ${QT_QT_LIBRARY})
	endif(QT_USE_FILE)
endmacro()

###############################################################################
# Add targets for the Catch unit testing framework.
#
# A library containing all the tests is created. This can be linked
# in by other catch libs.
#
# A catch executable for running all the tests are also created.
#
# Input variables:
#    LIB_TO_TEST : Name of the library to create tests for.
#    SOURCES     : List of test source files.
#
###############################################################################
function(cx_catch_add_lib_and_exe LIB_TO_TEST SOURCES)
	message(STATUS "Adding catch test targets based on: ${LIB_TO_TEST}")

	include_directories(
		.
		${PROJECT_SOURCE_DIR}/testUtilities
		${PROJECT_SOURCE_DIR}/catch)

#        cx_catch__private_define_platform_specific_linker_options()
	set(TEST_LIB_NAME "cxtestCatch${LIB_TO_TEST}")
		add_library(${TEST_LIB_NAME} ${CX_CATCH_SHARED_LIB_TYPE} ${SOURCES} )
		message(STATUS "          Lib name : ${TEST_LIB_NAME}")
	target_link_libraries(${TEST_LIB_NAME} ${LIB_TO_TEST} bbtestUtilities )

	set(CX_TEST_CATCH_GENERATED_LIBRARIES
		"${TEST_LIB_NAME}" "${CX_TEST_CATCH_GENERATED_LIBRARIES}"
		CACHE INTERNAL
		"List of all catch unit test libs that should be added to the master test exe.")

	set(TEST_EXE_NAME "Catch${LIB_TO_TEST}")
	message(STATUS "          Exe name : ${TEST_EXE_NAME}")

	set(cxtest_MAIN ${PROJECT_SOURCE_DIR}/testUtilities/bbtestCatchMain.cpp)
	add_executable(${TEST_EXE_NAME} ${cxtest_MAIN} )
	target_link_libraries(${TEST_EXE_NAME} ${CX_CATCH_PRE_WHOLE_ARCHIVE} ${TEST_LIB_NAME} ${CX_CATCH_POST_WHOLE_ARCHIVE})
endfunction()

