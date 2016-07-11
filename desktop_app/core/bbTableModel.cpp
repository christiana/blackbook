#include "bbTableModel.h"
#include "bbCostSplitCalculator.h"
#include <QBrush>
#include <iostream>
#include <QApplication>
#include <QClipboard>

namespace bb
{

TableModel::TableModel(QObject *parent, CostSplitCalculatorPtr costSplitter) :
	QAbstractTableModel(parent),
	mCostSplitter(costSplitter)
{
	connect(costSplitter.get(), SIGNAL(calculatorChanged()), this, SLOT(costSplitterChangedSlot()));
}

void TableModel::costSplitterChangedSlot()
{
	this->beginResetModel();
	this->endResetModel();
//	this->reset();
}

void TableModel::onCopyToClipboard()
{
	std::cout << "void TableModel::onCopyToClipboard()" << std::endl;
}

void TableModel::onPasteFromClipboard()
{
	std::cout << "void TableModel::onPasteFromClipboard()" << std::endl;

}

QDate TableModel::parseDateString(QString raw) const
{
	QDate retval;
	retval = QDate::fromString(raw, Qt::ISODate);
	if (retval.isNull())
		retval = QDate::fromString(raw, Qt::SystemLocaleLongDate);
	if (retval.isNull())
		retval = QDate::fromString(raw, Qt::SystemLocaleShortDate);
	return retval;
}



} // namespace bb
