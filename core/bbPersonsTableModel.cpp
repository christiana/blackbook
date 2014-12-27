#include "bbPersonsTableModel.h"
#include "bbCostSplitCalculator.h"
#include <iostream>
#include <QApplication>
#include <QClipboard>

namespace bb
{

PersonsTableModel::PersonsTableModel(QObject *parent, CostSplitCalculatorPtr costSplitter) :
	TableModel(parent, costSplitter)
{
}

int PersonsTableModel::rowCount(const QModelIndex& parent) const
{
	return mCostSplitter->getPersons().size();
}

int PersonsTableModel::columnCount(const QModelIndex& parent) const
{
	return 3;
}

QVariant PersonsTableModel::headerData(int section, Qt::Orientation orientation, int role) const
{
	if (orientation == Qt::Horizontal)
	{
		if (role==Qt::DisplayRole)
		{
			if (section==0)
				return QVariant("Name");
			if (section==1)
				return QVariant("Weight");
			if (section==2)
				return QVariant("Balance");
		}
	}
	return QVariant();
}

QVariant PersonsTableModel::data(const QModelIndex& index, int role) const
{
	if (role==Qt::DisplayRole || role==Qt::EditRole)
	{
		QString name = mCostSplitter->getPersons()[index.row()];

		if (index.column()==0)
		{
			return QVariant(name);
		}
		if (index.column()==1)
		{
			return QVariant::fromValue<double>(mCostSplitter->getWeight(name));
		}
		if (index.column()==2)
		{
			QString val = QString::number(mCostSplitter->getBalance(name), 'f', 2);
			return val;
//			return QVariant::fromValue<double>(mCostSplitter->getBalance(name));
		}
		return QVariant();
	}
	return QVariant();
}

bool PersonsTableModel::setData(const QModelIndex& index, const QVariant& value, int role)
{
	if (role==Qt::EditRole)
	{
		if (index.column()==1)
		{
			QString name = mCostSplitter->getPersons()[index.row()];
			mCostSplitter->addWeight(name, value.toDouble());
			return true;
		}
	}
	return false;
}

Qt::ItemFlags PersonsTableModel::flags(const QModelIndex& index) const
{
	if (index.column()==1)
		return Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsEditable;
	return Qt::ItemIsEnabled | Qt::ItemIsSelectable;
}

void PersonsTableModel::deleteRows(const std::set<int>& rows)
{
	QStringList persons = mCostSplitter->getPersons();
	for (std::set<int>::const_iterator iter=rows.begin(); iter!=rows.end(); ++iter)
	{
		mCostSplitter->removePerson(persons[*iter]);
	}
}

void PersonsTableModel::onPasteFromClipboard()
{
	std::cout << "void PersonsTableModel::onPasteFromClipboard()" << std::endl;

	QString clipText = QApplication::clipboard()->text();

	QStringList lines = clipText.split(QRegExp("[\\n|\\r]"));

	for (int i=0; i< lines.size(); ++i)
	{
		this->insertLineFromClipboard(lines[i]);
	}
}

void PersonsTableModel::insertLineFromClipboard(QString line)
{
	QStringList elements = line.split(QRegExp("\t"));

	// name, weight,
	Person person;
	person.mName = elements[0];
	if (elements.size()>1)
		person.mWeight = elements[1].toDouble();

	mCostSplitter->addPerson(person.mName);
	mCostSplitter->addWeight(person.mName, person.mWeight);
}


} // namespace bb
