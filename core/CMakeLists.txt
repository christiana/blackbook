###########################################################
##               BlackBook project
###########################################################

# Core library
set(BBCORE_SOURCE_FILES
	bbMainWindow.cpp
	bbMainWindow.h
	bbPersonsTableModel.h
	bbPersonsTableModel.cpp
	bbPaymentsTableModel.h
	bbPaymentsTableModel.cpp
	bbDebtsTableModel.h
	bbDebtsTableModel.cpp
	bbTableModel.cpp

	bbCostSplitCalculator.h
	bbCostSplitCalculator.cpp
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
QT5_WRAP_CPP(BBCORE_SOURCE_FILES
	bbMainWindow.h
	bbPersonsTableModel.h
	bbPaymentsTableModel.h
	bbDebtsTableModel.h
	bbTableModel.h

	bbCostSplitCalculator.h
	)
add_library( bbCore ${BBCORE_SOURCE_FILES} )
target_link_libraries( bbCore Qt5::Widgets Qt5::Xml )

