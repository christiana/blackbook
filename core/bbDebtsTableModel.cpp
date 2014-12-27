#include "bbDebtsTableModel.h"
#include "bbCostSplitCalculator.h"
#include <QBrush>
#include <iostream>
#include <QApplication>
#include <QClipboard>


namespace bb
{

DebtsTableModel::DebtsTableModel(QObject *parent, CostSplitCalculatorPtr costSplitter) :
	TableModel(parent, costSplitter)
{
}

int DebtsTableModel::rowCount(const QModelIndex& parent) const
{
	return mCostSplitter->getDebtsCount();
}

int DebtsTableModel::columnCount(const QModelIndex& parent) const
{
	return ciCOUNT;
}

QVariant DebtsTableModel::headerData(int section, Qt::Orientation orientation, int role) const
{
	if (orientation == Qt::Horizontal)
	{
		if (role==Qt::DisplayRole)
		{
			if (section==ciDEBITOR)
				return QVariant("Debitor");
			if (section==ciVALUE)
				return QVariant("Value");
			if (section==ciCREDITOR)
				return QVariant("Creditor");
			if (section==ciDESCRIPTION)
				return QVariant("Description");
			if (section==ciDATE)
				return QVariant("Date");
		}
	}
	return QVariant();
}

QVariant DebtsTableModel::data(const QModelIndex& index, int role) const
{
	if (role==Qt::DisplayRole || role==Qt::EditRole)
	{
		Debt debt = mCostSplitter->getDebt(index.row());

		if (index.column()==ciDEBITOR)
		{
			return QVariant(debt.mPayment.mPerson);
		}
		if (index.column()==ciVALUE)
		{
			return QVariant(debt.mPayment.mValue);
		}
		if (index.column()==ciCREDITOR)
		{
			return QVariant(debt.mCreditor);
		}
		if (index.column()==ciDESCRIPTION)
		{
			return QVariant::fromValue<QString>(debt.mPayment.mDescription);
		}
		if (index.column()==ciDATE)
		{
			return QVariant(debt.mPayment.mDate.toString(Qt::ISODate));
		}
	}

	if (role==Qt::ForegroundRole)
	{
		Debt debt = mCostSplitter->getDebt(index.row());
//		Payment payment = mCostSplitter->getPayment(index.row());

		if (index.column()==ciDEBITOR)
		{
			if (!mCostSplitter->getPersons().contains(debt.mPayment.mPerson))
				return QBrush("red");
		}
		if (index.column()==ciCREDITOR)
		{
			if (!mCostSplitter->getPersons().contains(debt.mCreditor))
				return QBrush("red");
		}
	}

	return QVariant();
}

bool DebtsTableModel::setData(const QModelIndex& index, const QVariant& value, int role)
{
	if (role==Qt::EditRole)
	{
		Debt debt = mCostSplitter->getDebt(index.row());

		if (index.column()==ciDEBITOR)
		{
			debt.mPayment.mPerson = value.toString();
		}
		if (index.column()==ciVALUE)
		{
			debt.mPayment.mValue = value.toDouble();
		}
		if (index.column()==ciCREDITOR)
		{
			debt.mCreditor = value.toString();
		}
		if (index.column()==ciDESCRIPTION)
		{
			debt.mPayment.mDescription = value.toString();
		}
		if (index.column()==ciDATE)
		{
			debt.mPayment.mDate = this->parseDateString(value.toString());
		}

		mCostSplitter->setDebt(index.row(), debt);
		return true;
	}

	return false;
}

Qt::ItemFlags DebtsTableModel::flags(const QModelIndex& index) const
{
//	if (index.column()>=ciPARTICIPANT_START)
//		return Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsEditable | Qt::ItemIsUserCheckable;
	return Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsEditable;
//	return Qt::ItemIsEnabled | Qt::ItemIsSelectable;
}

void DebtsTableModel::deleteRows(const std::set<int>& rows)
{
	for (std::set<int>::const_reverse_iterator iter=rows.rbegin(); iter!=rows.rend(); ++iter)
	{
		mCostSplitter->removeDebt(*iter);
	}
}

void DebtsTableModel::onPasteFromClipboard()
{
	std::cout << "void DebtsTableModel::onPasteFromClipboard()" << std::endl;

	QString clipText = QApplication::clipboard()->text();

	QStringList lines = clipText.split(QRegExp("[\\n|\\r]"));

	for (int i=0; i< lines.size(); ++i)
	{
		this->insertLineFromClipboard(lines[i]);
	}
}

void DebtsTableModel::insertLineFromClipboard(QString line)
{
	QStringList elements = line.split(QRegExp("\t"));

	// debitor, value, creditor, desc, date
	Debt debt;
	debt.mPayment.mDate = this->parseDateString(elements[0]);
	if (elements.size()>1)
		debt.mPayment.mPerson = elements[1];
	if (elements.size()>2)
		debt.mPayment.mValue = elements[2].toDouble();
	if (elements.size()>3)
		debt.mCreditor = elements[3];
	if (elements.size()>4)
		debt.mPayment.mDescription = elements[4];

	mCostSplitter->addDebt(debt);
}


} // namespace bb
