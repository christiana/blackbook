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
	this->createCostSplitter();

	this->createPersonsGui();
	this->createPaymentsGui();

	this->createActions();
	this->createToolbars();

	this->restoreGeometry(QSettings().value("mainWindow/geometry").toByteArray());
	this->restoreState(QSettings().value("mainWindow/windowState").toByteArray());

	this->show();

	QTimer::singleShot(0, this, SLOT(modelResetSlot()));
}

void MainWindow::closeEvent(QCloseEvent *event)
{
	QMainWindow::closeEvent(event);
	this->closeCostSplitter();
	QSettings().setValue("mainWindow/geometry", this->saveGeometry());
	QSettings().setValue("mainWindow/windowState", saveState());
}

void MainWindow::createCostSplitter()
{
	mCostSplitter.reset(new CostSplitCalculator);
	mCostSplitter->load(QSettings().value("mainWindow/lastFilename").toString());
}

void MainWindow::closeCostSplitter()
{
	if (QSettings().value("mainWindow/lastFilename").toString().isEmpty())
		QSettings().setValue("mainWindow/lastFilename", "autosave.xml");
	mCostSplitter->save(QSettings().value("mainWindow/lastFilename").toString());
}

void MainWindow::createPersonsGui()
{
	mPersonsTableModel = new PersonsTableModel(this, mCostSplitter);
	connect(mPersonsTableModel, SIGNAL(modelReset()), this, SLOT(modelResetSlot()));

	mPersonsTable = new QTableView();
	mPersonsTable->setWindowTitle("Persons");
	mPersonsTable->setObjectName("Persons");
	mPersonsTable->setModel(mPersonsTableModel);
	this->addAsDockWidget(mPersonsTable);
}

void MainWindow::createPaymentsGui()
{
	mPaymentsTableModel = new PaymentsTableModel(this, mCostSplitter);
	connect(mPaymentsTableModel, SIGNAL(modelReset()), this, SLOT(modelResetSlot()));

	mPaymentsTable = new QTableView();
	mPaymentsTable->setWindowTitle("Payments");
	mPaymentsTable->setObjectName("Payments");
	mPaymentsTable->setModel(mPaymentsTableModel);
	this->addAsDockWidget(mPaymentsTable);
}

void MainWindow::createActions()
{
	mNewPersonAction = new QAction("New Person", this);
	mNewPersonAction->setStatusTip(tr("Add a new person"));
	connect(mNewPersonAction, SIGNAL(triggered()), this, SLOT(newPersonSlot()));

	mNewPaymentAction = new QAction("New Payment", this);
	mNewPaymentAction->setStatusTip(tr("Add a new payment"));
	connect(mNewPaymentAction, SIGNAL(triggered()), this, SLOT(newPaymentSlot()));

	mDeleteRowAction = new QAction("Delete", this);
	mDeleteRowAction->setStatusTip(tr("Delete all selected rows"));
	connect(mDeleteRowAction, SIGNAL(triggered()), this, SLOT(deleteRowSlot()));
}

void MainWindow::createToolbars()
{
	QToolBar* allToolBar = addToolBar("All");
	allToolBar->setObjectName("AllToolBar");
	allToolBar->addAction(mNewPersonAction);
	allToolBar->addAction(mNewPaymentAction);
	allToolBar->addAction(mDeleteRowAction);
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

void MainWindow::deleteRowSlot()
{
	std::set<int> paymentRows = this->getRows(mPaymentsTable->selectionModel()->selectedIndexes());
	std::set<int> personsRows = this->getRows(mPersonsTable->selectionModel()->selectedIndexes());
	mPaymentsTableModel->deleteRows(paymentRows);
	mPersonsTableModel->deleteRows(personsRows);
}

std::set<int> MainWindow::getRows(QModelIndexList modelIndices)
{
	std::set<int> retval;
	for (unsigned i=0; i<modelIndices.size(); ++i)
		retval.insert(modelIndices[i].row());
	return retval;
}

void MainWindow::addAsDockWidget(QWidget* widget)
{
	QDockWidget* dockWidget = new QDockWidget(widget->windowTitle(), this);
	dockWidget->setObjectName(widget->objectName() + "DockWidget");
	dockWidget->setWidget(widget);
	QMainWindow::addDockWidget(Qt::LeftDockWidgetArea, dockWidget);
}

void MainWindow::modelResetSlot()
{
	mPaymentsTable->resizeColumnsToContents();
	mPersonsTable->resizeColumnsToContents();
}

}
