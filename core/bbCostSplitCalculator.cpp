#include "bbCostSplitCalculator.h"

#include <map>
#include <iostream>

namespace bb
{

CostSplitCalculator::CostSplitCalculator()
{
}

void CostSplitCalculator::addPerson(QString name)
{
	mPersons.push_back(Person(name));
	emit calculatorChanged();
//	std::cout << "added person " << name.toStdString() << std::endl;
}

void CostSplitCalculator::addWeight(QString name, double weight)
{
	for (unsigned i=0; i<mPersons.size(); ++i)
	{
		if (mPersons[i].mName!=name)
			continue;
		mPersons[i].mWeight = weight;
	}
	emit calculatorChanged();
}

double CostSplitCalculator::getWeight(QString name) const
{
	for (unsigned i=0; i<mPersons.size(); ++i)
	{
		if (mPersons[i].mName!=name)
			continue;
		return mPersons[i].mWeight;
	}
	return 0;
}

QStringList CostSplitCalculator::getPersons() const
{
	QStringList retval;
	for (unsigned i=0; i<mPersons.size(); ++i)
		retval << mPersons[i].mName;
	return retval;
}

void CostSplitCalculator::addPayment(Payment payment)
{
	mPayments.push_back(payment);
	emit calculatorChanged();
}

void CostSplitCalculator::setPayment(int index, Payment payment)
{
	mPayments[index] = payment;
	emit calculatorChanged();
}

void CostSplitCalculator::addPayment(QString name, double value, QString description, QDate date)
{
	this->addPayment(Payment(name, value, description, QStringList(), date));
}

double CostSplitCalculator::getBalance(QString name) const
{
	double balance = 0;
	balance += this->getPartOfPaymentForPerson(name);
	balance += this->getCreditAndDebitForPerson(name);
	return balance;
}

double CostSplitCalculator::getPartOfPaymentForPerson(QString name) const
{
	double retval = 0;
	for (unsigned i=0; i<mPayments.size(); ++i)
		retval += this->getPartOfPaymentForPerson(mPayments[i], name);
	return retval;
}

double CostSplitCalculator::getPartOfPaymentForPerson(Payment payment, QString name) const
{
	double retval = 0;
	if (payment.mPerson==name)
		retval += payment.mValue;
	double fraction = this->getFractionForPerson(name, payment.mParticipants);
	retval -= fraction * payment.mValue;
	return retval;
}

double CostSplitCalculator::getFractionForPerson(QString name, QStringList participants) const
{
	if (participants.empty())
		participants = this->getPersons();

	if (!participants.contains(name))
		return 0;

	double totalWeight = 0;
	for (unsigned i=0; i<participants.size(); ++i)
		totalWeight += this->getWeight(participants[i]);

	double weight = this->getWeight(name);
	return weight/totalWeight;
}

double CostSplitCalculator::getCreditAndDebitForPerson(QString name) const
{
	double retval = 0;
	for (unsigned i=0; i<mDebts.size(); ++i)
		retval += this->getCreditAndDebitForPerson(name, mDebts[i].first, mDebts[i].second);
	return retval;
}

double CostSplitCalculator::getCreditAndDebitForPerson(QString name, QString creditor, Payment debit) const
{
	double retval = 0;
	if (name==creditor)
		retval += debit.mValue;
	if (name==debit.mPerson)
		retval -= debit.mValue;
	return retval;
}

std::vector<Payment> CostSplitCalculator::getPayments() const
{
	return mPayments;
}

void CostSplitCalculator::addDebtFromDebitorToCreditor(double value, QString debitor, QString creditor, QString description, QDate date)
{
	mDebts.push_back(std::make_pair(creditor, Payment(debitor, value, description, QStringList(), date)));
	emit calculatorChanged();
}

} // namespace bb
