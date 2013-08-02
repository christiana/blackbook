#include "bbPaymentsTableModel.h"
#include "bbCostSplitCalculator.h"

namespace bb
{

PaymentsTableModel::PaymentsTableModel(QObject *parent, CostSplitCalculatorPtr costSplitter) :
	QAbstractTableModel(parent),
	mCostSplitter(costSplitter)
{
	connect(costSplitter.get(), SIGNAL(calculatorChanged()), this, SLOT(costSplitterChangedSlot()));
}

int PaymentsTableModel::rowCount(const QModelIndex& parent) const
{
	return mCostSplitter->getPayments().size();
}

int PaymentsTableModel::columnCount(const QModelIndex& parent) const
{
	return this->columnCount();
}

int PaymentsTableModel::columnCount() const
{
	return ciPARTICIPANT_START + mCostSplitter->getPersons().size();
}

QVariant PaymentsTableModel::headerData(int section, Qt::Orientation orientation, int role) const
{
	if (orientation == Qt::Horizontal)
	{
		if (role==Qt::DisplayRole)
		{
			int cols = this->columnCount();
			if (section==ciPERSON)
				return QVariant("Person");
			if (section==ciVALUE)
				return QVariant("Value");
			if (section==ciDESCRIPTION)
				return QVariant("Description");
			if (section==ciDATE)
				return QVariant("Date");


			QString participant = this->getParticipantForColumn(section);
			if (!participant.isEmpty())
			{
				return QVariant(participant);
			}
		}
	}
	return QVariant();
}

QVariant PaymentsTableModel::data(const QModelIndex& index, int role) const
{
	if (role==Qt::DisplayRole || role==Qt::EditRole)
	{
		Payment payment = mCostSplitter->getPayments()[index.row()];

		if (index.column()==ciPERSON)
		{
			return QVariant(payment.mPerson);
		}
		if (index.column()==ciVALUE)
		{
			return QVariant::fromValue<double>(payment.mValue);
		}
		if (index.column()==ciDESCRIPTION)
		{
			return QVariant::fromValue<QString>(payment.mDescription);
		}
		if (index.column()==ciDATE)
		{
			return QVariant::fromValue<QDate>(payment.mDate);
		}
	}

	if (role==Qt::CheckStateRole)
	{
		Payment payment = mCostSplitter->getPayments()[index.row()];
		QString participant = this->getParticipantForColumn(index.column());
		if (!participant.isEmpty())
		{
			bool val = payment.mParticipants.contains(participant);
			return QVariant(2*(int(val))); // convert to tristate
		}
	}

	return QVariant();
}

bool PaymentsTableModel::setData(const QModelIndex& index, const QVariant& value, int role)
{
	if (role==Qt::EditRole)
	{
		Payment payment = mCostSplitter->getPayments()[index.row()];

		if (index.column()==ciPERSON)
		{
			payment.mPerson = value.toString();
		}
		if (index.column()==ciVALUE)
		{
			payment.mValue = value.toDouble();
		}
		if (index.column()==ciDESCRIPTION)
		{
			payment.mDescription = value.toString();
		}
		if (index.column()==ciDATE)
		{
			payment.mDate = value.toDate();
		}

		mCostSplitter->setPayment(index.row(), payment);
		return true;
	}

	if (role==Qt::CheckStateRole)
	{
		Payment payment = mCostSplitter->getPayments()[index.row()];
		QString participant = this->getParticipantForColumn(index.column());
		if (!participant.isEmpty())
		{
			bool val = value.toInt();
			if (val)
				payment.mParticipants.append(participant);
			else
				payment.mParticipants.removeAll(participant);
			payment.mParticipants.removeDuplicates();
		}
		mCostSplitter->setPayment(index.row(), payment);
		return true;
	}

	return false;
}

QString PaymentsTableModel::getParticipantForColumn(int column) const
{
	QStringList persons = mCostSplitter->getPersons();
	int personIndex = column - ciPARTICIPANT_START;
	if (personIndex>=0 && personIndex<persons.size())
	{
		return persons[personIndex];
	}
	return "";
}

Qt::ItemFlags PaymentsTableModel::flags(const QModelIndex& index) const
{
	if (index.column()>=ciPARTICIPANT_START)
		return Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsEditable | Qt::ItemIsUserCheckable;
	return Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsEditable;
//	return Qt::ItemIsEnabled | Qt::ItemIsSelectable;
}

void PaymentsTableModel::costSplitterChangedSlot()
{
	this->reset();
}

void PaymentsTableModel::deleteRows(const std::set<int>& rows)
{
	for (std::set<int>::const_reverse_iterator iter=rows.rbegin(); iter!=rows.rend(); ++iter)
	{
		mCostSplitter->removePayment(*iter);
	}
}

} // namespace bb
