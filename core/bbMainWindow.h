#ifndef BBMAINWINDOW_H
#define BBMAINWINDOW_H

#include <QMainWindow>
#include <QtGui>
#include "boost/shared_ptr.hpp"
#include <set>
#include <QTableView>
class QTableView;

namespace bb
{
class TableModel;

typedef boost::shared_ptr<class CostSplitCalculator> CostSplitCalculatorPtr;
class PersonsTableModel;
class PaymentsTableModel;
class DebtsTableModel;

class MyTableView : public QTableView
{
	Q_OBJECT
public:
	MyTableView(QWidget* parent=NULL) : QTableView(parent) {}
	virtual ~MyTableView() {}
	virtual void keyPressEvent(QKeyEvent* event);
signals:
	void copyToClipboard();
	void pasteFromClipboard();
private:
	void onCopyToClipboard();
};

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
	void newFileSlot();
	void loadFileSlot();
	void saveFileSlot();

private:
	QAction* mNewPersonAction;
	QAction* mNewPaymentAction;
	QAction* mNewDebtAction;
	QAction* mDeleteRowAction;

	QAction* mNewFileAction;
	QAction* mSaveFileAction;
	QAction* mLoadFileAction;

	CostSplitCalculatorPtr mCostSplitter;
	PersonsTableModel* mPersonsTableModel;
	PaymentsTableModel* mPaymentsTableModel;
	DebtsTableModel* mDebtsTableModel;

	MyTableView* mPersonsTable;
	MyTableView* mPaymentsTable;
	MyTableView* mDebtsTable;

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
	MyTableView* createTableView(TableModel* model);
	void loadFile(QString filename);

	QString mCurrentFile;
};

}

#endif // BBMAINWINDOW_H
