#include "bbDebtEntry.h"

namespace bb
{

DebtEntryPtr DebtEntry::create(const Debt& debt, PersonListPtr personList)
{
	DebtEntryPtr retval(new DebtEntry());
	retval->mDebt = debt;
	retval->mPersonList = personList;
	return retval;
}

DebtEntry::DebtEntry()
{

}

Debt DebtEntry::getDebt() const
{
	return mDebt;
}

void DebtEntry::setDebt(Debt debt)
{
	mDebt = debt;
}

void DebtEntry::addXml(QDomElement node)
{
	mDebt.addXml(node);
}

void DebtEntry::parseXml(QDomElement node)
{
	mDebt.parseXml(node);
}

double DebtEntry::getBalanceForPerson(QString name) const
{
	double retval = 0;
	if (name==mDebt.mCreditor)
		retval += mDebt.mPayment.mValue;
	if (name==mDebt.mPayment.mPerson)
		retval -= mDebt.mPayment.mValue;
	return retval;
}

bool DebtEntry::equal(const EntryPtr other) const
{
	DebtEntryPtr rhs = boost::dynamic_pointer_cast<DebtEntry>(other);
	return rhs && (mDebt==rhs->getDebt());
}


} // namespace bb

