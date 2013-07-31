#ifndef BBMAINWINDOW_H
#define BBMAINWINDOW_H

#include <QMainWindow>
#include <QtGui>
#include "boost/shared_ptr.hpp"

namespace bb
{

typedef boost::shared_ptr<class CostSplitCalculator> CostSplitCalculatorPtr;
class PersonsTableModel;
class PaymentsTableModel;

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

private:
	QAction* mNewPersonAction;
	QAction* mNewPaymentAction;

	CostSplitCalculatorPtr mCostSplitter;
	PersonsTableModel* mPersonsTableModel;
	PaymentsTableModel* mPaymentsTableModel;

	void addAsDockWidget(QWidget* widget);
};

}

#endif // BBMAINWINDOW_H
