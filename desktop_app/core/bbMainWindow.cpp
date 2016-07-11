#include "bbMainWindow.h"

#include <QTableView>
#include <QAction>
#include <QToolBar>
#include <QDockWidget>
#include "bbPersonsTableModel.h"
#include "bbCostSplitCalculator.h"
#include "bbPersonsTableModel.h"
#include "bbPaymentsTableModel.h"
#include "bbDebtsTableModel.h"
#include "bbTableModel.h"
#include <QInputDialog>
#include <iostream>
#include <QApplication>
#include <QClipboard>
#include <QHeaderView>
#include <QFileDialog>

namespace bb
{

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent)
{
	this->setDockNestingEnabled(true);
	this->createCostSplitter();

	this->createPersonsGui();
	this->createPaymentsGui();
	this->createDebtsGui();

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

	QString fileName = QSettings().value("mainWindow/lastFilename").toString();
	if (fileName.isEmpty())
		fileName = "blackbook.data.xml";
	this->loadFile(fileName);

//	mCurrentFile = QSettings().value("mainWindow/lastFilename").toString();

//	mCostSplitter->load(mCurrentFile);
//	mCostSplitter->load(QSettings().value("mainWindow/lastFilename").toString());
}

void MainWindow::closeCostSplitter()
{
	mCostSplitter->save(mCurrentFile);

//	if (QSettings().value("mainWindow/lastFilename").toString().isEmpty())
//		QSettings().setValue("mainWindow/lastFilename", "autosave.xml");
//	mCostSplitter->save(QSettings().value("mainWindow/lastFilename").toString());
}

void MainWindow::loadFile(QString filename)
{
	mCurrentFile = filename;
	mCostSplitter->load(mCurrentFile);
	QSettings().setValue("mainWindow/lastFilename", mCurrentFile);

//	if (QSettings().value("mainWindow/lastFilename").toString().isEmpty())
//		QSettings().setValue("mainWindow/lastFilename", "autosave.xml");
//	mCostSplitter->save(QSettings().value("mainWindow/lastFilename").toString());
}

void MainWindow::newFileSlot()
{
	QString fileName = QFileDialog::getSaveFileName(this, tr("New File"),
							   "",
							   tr("BlackBook files (*.xml)"));

	if (fileName.isEmpty())
		return;

	this->loadFile(fileName);

//	mCurrentFile = fileName;
//	QSettings().setValue("mainWindow/lastFilename", mCurrentFile);
//	mCostSplitter->clear();
}

void MainWindow::loadFileSlot()
{
	QString fileName = QFileDialog::getOpenFileName(this, tr("Open File"),
							   "",
							   tr("BlackBook files (*.xml)"));

	if (fileName.isEmpty())
		return;

	this->loadFile(fileName);
//	mCurrentFile = fileName;
//	QSettings().setValue("mainWindow/lastFilename", mCurrentFile);
//	mCostSplitter->load(fileName);
}

void MainWindow::saveFileSlot()
{
	mCostSplitter->save(mCurrentFile);
}

void MainWindow::createPersonsGui()
{
	mPersonsTableModel = new PersonsTableModel(this, mCostSplitter);
	connect(mPersonsTableModel, SIGNAL(modelReset()), this, SLOT(modelResetSlot()));

	mPersonsTable = this->createTableView(mPersonsTableModel);
}

void MainWindow::createPaymentsGui()
{
	mPaymentsTableModel = new PaymentsTableModel(this, mCostSplitter);
	connect(mPaymentsTableModel, SIGNAL(modelReset()), this, SLOT(modelResetSlot()));

	mPaymentsTable = this->createTableView(mPaymentsTableModel);
}

MyTableView* MainWindow::createTableView(TableModel* model)
{
	MyTableView* retval = new MyTableView();
	retval->setWindowTitle(model->getTitle());
	retval->setObjectName(model->getTitle());
	retval->setModel(model);
	retval->setTabKeyNavigation(true);
	connect(retval, &MyTableView::copyToClipboard, model, &TableModel::onCopyToClipboard);
	connect(retval, &MyTableView::pasteFromClipboard, model, &TableModel::onPasteFromClipboard);

	QFontMetrics metric(retval->font());
	int textLineHeight = metric.lineSpacing()* 1.2;
	QHeaderView *verticalHeader = retval->verticalHeader();
	verticalHeader->setSectionResizeMode(QHeaderView::Fixed);
	verticalHeader->setDefaultSectionSize(textLineHeight);

	this->addAsDockWidget(retval);
	return retval;
}

void MainWindow::createDebtsGui()
{
	mDebtsTableModel = new DebtsTableModel(this, mCostSplitter);
	connect(mDebtsTableModel, SIGNAL(modelReset()), this, SLOT(modelResetSlot()));

	mDebtsTable = this->createTableView(mDebtsTableModel);
}

void MainWindow::createActions()
{
	mNewFileAction = new QAction(QIcon(":/icons/new.png"), "New file", this);
	mNewFileAction->setShortcut(tr("Ctrl+N"));
	mNewFileAction->setStatusTip("Create a new file");
	connect(mNewFileAction, &QAction::triggered, this, &MainWindow::newFileSlot);

	mSaveFileAction = new QAction(QIcon(":/icons/save.png"), "Save file", this);
	mSaveFileAction->setShortcut(tr("Ctrl+S"));
	mSaveFileAction->setStatusTip(tr("Save file"));
	connect(mSaveFileAction, &QAction::triggered, this, &MainWindow::saveFileSlot);

	mLoadFileAction = new QAction(QIcon(":/icons/open.png"), "Load file", this);
	mLoadFileAction->setShortcut(tr("Ctrl+L"));
	mLoadFileAction->setStatusTip(tr("Load file"));
	connect(mLoadFileAction, &QAction::triggered, this, &MainWindow::loadFileSlot);

	mNewPersonAction = new QAction(QIcon(":icons/user-new-3.png"), "New Person", this);
	mNewPersonAction->setStatusTip(tr("Add a new person"));
	connect(mNewPersonAction, SIGNAL(triggered()), this, SLOT(newPersonSlot()));

	mNewPaymentAction = new QAction(QIcon(":icons/tab-new-raised.png"), "New Payment", this);
	mNewPaymentAction->setStatusTip(tr("Add a new payment"));
	connect(mNewPaymentAction, SIGNAL(triggered()), this, SLOT(newPaymentSlot()));

	mNewDebtAction = new QAction(QIcon(":icons/tab-new-raised.png"), "New Debt", this);
	mNewDebtAction->setStatusTip(tr("Add a new debt"));
	connect(mNewDebtAction, SIGNAL(triggered()), this, SLOT(newDebtSlot()));

	mDeleteRowAction = new QAction(QIcon(":icons/tab-close-3.png"), "Delete", this);
	mDeleteRowAction->setStatusTip(tr("Delete all selected rows"));
	connect(mDeleteRowAction, SIGNAL(triggered()), this, SLOT(deleteRowSlot()));
}

void MainWindow::createToolbars()
{
	QToolBar* fileToolBar = addToolBar("File");
	fileToolBar->setObjectName("FileToolBar");
	fileToolBar->addAction(mNewFileAction);
	fileToolBar->addAction(mSaveFileAction);
	fileToolBar->addAction(mLoadFileAction);

	QToolBar* allToolBar = addToolBar("All");
	allToolBar->setObjectName("AllToolBar");

	allToolBar->addAction(mNewPersonAction);
	allToolBar->addAction(mNewPaymentAction);
	allToolBar->addAction(mNewDebtAction);
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

void MainWindow::newDebtSlot()
{
	Debt debt("", Payment("", 0, "", QStringList(), QDate::currentDate()));
	mCostSplitter->addDebt(debt);
}

void MainWindow::deleteRowSlot()
{
	std::set<int> paymentRows = this->getRows(mPaymentsTable->selectionModel()->selectedIndexes());
	std::set<int> personsRows = this->getRows(mPersonsTable->selectionModel()->selectedIndexes());
	std::set<int> debtRows = this->getRows(mDebtsTable->selectionModel()->selectedIndexes());
	mPaymentsTableModel->deleteRows(paymentRows);
	mPersonsTableModel->deleteRows(personsRows);
	mDebtsTableModel->deleteRows(debtRows);
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
	mDebtsTable->resizeColumnsToContents();

	this->setWindowTitle(mCurrentFile);

	std::cout << "modelreset" << std::endl;
	mCostSplitter->verifyCalculations();
}


//source: http://stackoverflow.com/questions/3135737/copying-part-of-qtableview
void MyTableView::keyPressEvent(QKeyEvent* event)
{
	if (event->key() == Qt::Key_C && (event->modifiers() & Qt::ControlModifier))
	{
		this->onCopyToClipboard();
	}
	if (event->key() == Qt::Key_V && (event->modifiers() & Qt::ControlModifier))
	{
		emit pasteFromClipboard();
	}
	if (event->key() == Qt::Key_A && (event->modifiers() & Qt::ControlModifier))
	{
		this->selectAll();
	}
}

void MyTableView::onCopyToClipboard()
{
	std::cout << "void MyTableView::onCopyToClipboard()" << std::endl;

	QModelIndexList cells = this->selectedIndexes();
	qSort(cells); // Necessary, otherwise they are in column order

	QString text;
	int currentRow = 0; // To determine when to insert newlines
	foreach (const QModelIndex& cell, cells)
	{
		if (text.length() == 0)
		{
			// First item
		}
		else if (cell.row() != currentRow)
		{
			// New row
			text += '\n';
		}
		else
		{
			// Next cell
			text += '\t';
		}
		currentRow = cell.row();
		text += cell.data().toString();
	}

	QApplication::clipboard()->setText(text);
}

}

