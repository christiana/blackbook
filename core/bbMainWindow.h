#ifndef BBMAINWINDOW_H
#define BBMAINWINDOW_H

#include <QMainWindow>
#include <QtGui>
#include "boost/shared_ptr.hpp"
#include <set>

namespace bb
{

typedef boost::shared_ptr<class CostSplitCalculator> CostSplitCalculatorPtr;
class PersonsTableModel;
class PaymentsTableModel;
class DebtsTableModel;

/**
 *
 *
 * \ingroup bb
 * \date 29.07.2013, 2013
 * \author christiana
 */
class MainWindow : public QMainWindow
{
	Q_OBJECT
public:
	explicit MainWindow(QWidget *parent = 0);
	
signals:
	
public slots:
	void newPersonSlot();
	void newPaymentSlot();
	void newDebtSlot();
	void deleteRowSlot();
	void modelResetSlot();

private:
	QAction* mNewPersonAction;
	QAction* mNewPaymentAction;
	QAction* mNewDebtAction;
	QAction* mDeleteRowAction;

	CostSplitCalculatorPtr mCostSplitter;
	PersonsTableModel* mPersonsTableModel;
	PaymentsTableModel* mPaymentsTableModel;
	DebtsTableModel* mDebtsTableModel;

	QTableView* mPersonsTable;
	QTableView* mPaymentsTable;
	QTableView* mDebtsTable;

	void closeEvent(QCloseEvent *event);
	void addAsDockWidget(QWidget* widget);
	std::set<int> getRows(QModelIndexList modelIndices);
	void createCostSplitter();
	void closeCostSplitter();
	void createPersonsGui();
	void createPaymentsGui();
	void createDebtsGui();
	void createActions();
	void createToolbars();
};

}

#endif // BBMAINWINDOW_H
