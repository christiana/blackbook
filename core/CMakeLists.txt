###########################################################
##               BlackBook project
###########################################################

# Core library
set(BBCORE_SOURCE_FILES
	bbMainWindow.cpp
	bbMainWindow.h
	bbCostSplitCalculator.h
	bbCostSplitCalculator.cpp
	bbPersonsTableModel.h
	bbPersonsTableModel.cpp
	bbPaymentsTableModel.h
	bbPaymentsTableModel.cpp
	bbDebtsTableModel.h
	bbDebtsTableModel.cpp
	bbXmlFile.h
	bbXmlFile.cpp
	bbPersonList.h
	bbPersonList.cpp
	bbUtilities.h
	bbUtilities.cpp
	bbEntry.h
	bbEntry.cpp
	bbPaymentEntry.h
	bbPaymentEntry.cpp
	bbDebtEntry.h
	bbDebtEntry.cpp
	bbPayment.h
	bbPayment.cpp
	)
QT4_WRAP_CPP(BBCORE_SOURCE_FILES
	bbCostSplitCalculator.h
	bbMainWindow.h
	bbPersonsTableModel.h
	bbPaymentsTableModel.h
	bbDebtsTableModel.h
	)
add_library( bbCore ${BBCORE_SOURCE_FILES} )
target_link_libraries( bbCore ${QT_LIBRARIES} )

if (BUILD_TESTING)
	QT4_WRAP_CPP(BBTEST_CORE_SOURCES
		)
	set(BBTEST_CORE_SOURCES ${BBTEST_CORE_SOURCES}
		bbCostSplitCalculatorTest.cpp
		)
	cx_catch_add_lib_and_exe(bbCore "${BBTEST_CORE_SOURCES}")
endif (BUILD_TESTING)
