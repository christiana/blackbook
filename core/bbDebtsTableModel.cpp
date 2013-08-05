#include "bbDebtsTableModel.h"
#include "bbCostSplitCalculator.h"

namespace bb
{

DebtsTableModel::DebtsTableModel(QObject *parent, CostSplitCalculatorPtr costSplitter) :
	QAbstractTableModel(parent),
	mCostSplitter(costSplitter)
{
	connect(costSplitter.get(), SIGNAL(calculatorChanged()), this, SLOT(costSplitterChangedSlot()));
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
			return QVariant::fromValue<QDate>(debt.mPayment.mDate);
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
			debt.mPayment.mDate = value.toDate();
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

void DebtsTableModel::costSplitterChangedSlot()
{
	this->reset();
}

void DebtsTableModel::deleteRows(const std::set<int>& rows)
{
	for (std::set<int>::const_reverse_iterator iter=rows.rbegin(); iter!=rows.rend(); ++iter)
	{
		mCostSplitter->removeDebt(*iter);
	}
}

} // namespace bb
