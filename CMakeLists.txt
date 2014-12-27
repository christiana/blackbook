###########################################################
##               BlackBook project
###########################################################

project(BlackBook)
cmake_minimum_required(VERSION 2.8)

set(CMAKE_MODULE_PATH
	${CMAKE_MODULE_PATH}
	${PROJECT_SOURCE_DIR}/cmake)
include(bbUtilities)

cx_initialize_Boost()
cx_initialize_QT()

add_subdirectory(testUtilities)
add_subdirectory(core)

include_directories(
		${BlackBook_SOURCE_DIR}/core
		)

#------------------------------------------------------------------------------
# Installer stuff
#-----------------------------------------------------------------------------
set(BlackBook_VERSION_STRING "0.1")

if(APPLE) # For Apple set the icns file containing icons
	set(MACOSX_BUNDLE_ICON_FILE "application.icns") # set how it shows up in the Info.plist file
	set_source_files_properties(${BlackBook_SOURCE_DIR}/icons/application.icns
															PROPERTIES MACOSX_PACKAGE_LOCATION Resources)  # set where in the bundle to put the icns file
	
	set(BBMAIN_SOURCE_FILES ${BBMAIN_SOURCE_FILES} ${BlackBook_SOURCE_DIR}/icons/application.icns)  # include the icns file in the target
	set(MACOSX_BUNDLE_INFO_STRING "BlackBook")
	set(MACOSX_BUNDLE_BUNDLE_NAME "BlackBook")
	set(MACOSX_BUNDLE_BUNDLE_VERSION "${BlackBook_VERSION_STRING}")
	set(MACOSX_BUNDLE_SHORT_VERSION_STRING "${MACOSX_BUNDLE_BUNDLE_VERSION}")
	set(MACOSX_BUNDLE_LONG_VERSION_STRING "BlackBook ${MACOSX_BUNDLE_BUNDLE_VERSION}")
	set(MACOSX_BUNDLE_COPYRIGHT "Copyright Christian Askeland\nAll rights reserved")
endif(APPLE)

#------------------------------------------------------------------------------
# Executable
#-----------------------------------------------------------------------------

QT5_ADD_RESOURCES(BBMAIN_SOURCE_FILES bbResources.qrc)
set(BBMAIN_SOURCE_FILES bbMain.cpp ${BBMAIN_SOURCE_FILES})
add_executable(BlackBook MACOSX_BUNDLE ${BBMAIN_SOURCE_FILES} )
target_link_libraries(BlackBook bbCore)

