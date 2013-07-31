#include "bbMainWindow.h"

#include <QTableView>
#include "bbPersonsTableModel.h"
#include "bbCostSplitCalculator.h"
#include "bbPersonsTableModel.h"
#include "bbPaymentsTableModel.h"
#include <QInputDialog>

namespace bb
{

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent)
{
	this->setDockNestingEnabled(true);
	mCostSplitter.reset(new CostSplitCalculator);
	mPersonsTableModel = new PersonsTableModel(this, mCostSplitter);
	mPaymentsTableModel = new PaymentsTableModel(this, mCostSplitter);

	QTableView* personsTable = new QTableView();
	personsTable->setWindowTitle("Persons");
	personsTable->setModel(mPersonsTableModel);
	this->addAsDockWidget(personsTable);
//	this->setCentralWidget(personsTable);

	QTableView* paymentsTable = new QTableView();
	paymentsTable->setWindowTitle("Payments");
	paymentsTable->setModel(mPaymentsTableModel);
	this->addAsDockWidget(paymentsTable);

	mNewPersonAction = new QAction("New Person", this);
	mNewPersonAction->setStatusTip(tr("Add a new person"));
	connect(mNewPersonAction, SIGNAL(triggered()), this, SLOT(newPersonSlot()));

	mNewPaymentAction = new QAction("New Payment", this);
	mNewPaymentAction->setStatusTip(tr("Add a new payment"));
	connect(mNewPaymentAction, SIGNAL(triggered()), this, SLOT(newPaymentSlot()));

	QToolBar* allToolBar = addToolBar("All");
	allToolBar->setObjectName("AllToolBar");
	allToolBar->addAction(mNewPersonAction);
	allToolBar->addAction(mNewPaymentAction);

	this->show();
}

void MainWindow::newPersonSlot()
{
	bool ok;
	QString text = QInputDialog::getText(this, "New Person",
										 "Enter name:", QLineEdit::Normal, "NN", &ok);
	if (!ok)
		return;
	mCostSplitter->addPerson(text);
}

void MainWindow::newPaymentSlot()
{
	Payment payment("", 0, "", mCostSplitter->getPersons(), QDate::currentDate());
	mCostSplitter->addPayment(payment);
}

void MainWindow::addAsDockWidget(QWidget* widget)
{
//	// add a scroller to allow for very large widgets in the vertical direction
//	QScrollArea* scroller = new QScrollArea(NULL);
//	scroller->setWidget(widget);
//	scroller->setWidgetResizable(true);
//	scroller->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
//	QSizePolicy policy = scroller->sizePolicy();
//	policy.setHorizontalPolicy(QSizePolicy::Minimum);
//	scroller->setSizePolicy(policy);

	QDockWidget* dockWidget = new QDockWidget(widget->windowTitle(), this);
	dockWidget->setObjectName(widget->objectName() + "DockWidget");
//	dockWidget->setWidget(scroller);
	dockWidget->setWidget(widget);

	QMainWindow::addDockWidget(Qt::LeftDockWidgetArea, dockWidget);

//	// tabify the widget onto one of the left widgets.
//	for (std::set<QDockWidget*>::iterator iter = mDockWidgets.begin(); iter != mDockWidgets.end(); ++iter)
//	{
//		if (this->dockWidgetArea(*iter) == Qt::LeftDockWidgetArea)
//		{
//			this->tabifyDockWidget(*iter, dockWidget);
//			break;
//		}
//	}

//	mDockWidgets.insert(dockWidget);
//	dockWidget->setVisible(false); // default visibility

//	this->addToWidgetGroupMap(dockWidget->toggleViewAction(), groupname);
}

}
