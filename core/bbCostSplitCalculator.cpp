#include "bbCostSplitCalculator.h"

#include <map>

CostSplitCalculator::CostSplitCalculator()
{
}

void CostSplitCalculator::addPerson(QString name)
{
	mPersons.push_back(Person(name));
}

void CostSplitCalculator::addWeight(QString name, double weight)
{
	for (unsigned i=0; i<mPersons.size(); ++i)
	{
		if (mPersons[i].mName!=name)
			continue;
		mPersons[i].mWeight = weight;
	}
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
	std::map<QString, double> paymentPerPerson = this->getPaymentPerPerson();
	double totalPayment = this->getTotalPayment(paymentPerPerson);
	double fraction = this->getFractionForPerson(name);
	double perPerson = fraction * totalPayment;

	return paymentPerPerson[name] - perPerson;
}

double CostSplitCalculator::getFractionForPerson(QString name) const
{
	double totalWeight = this->getTotalWeight();
	double weight = this->getWeight(name);
	return weight/totalWeight;
}

double CostSplitCalculator::getTotalWeight() const
{
	double retval = 0;
	for (unsigned i=0; i<mPersons.size(); ++i)
		retval += mPersons[i].mWeight;
	return retval;
}

std::map<QString, double> CostSplitCalculator::getPaymentPerPerson() const
{
	std::map<QString, double> paymentPerPerson;
	for (unsigned i=0; i<mPayments.size(); ++i)
	{
		Payment current = mPayments[i];
		if (paymentPerPerson.count(current.mPerson))
			paymentPerPerson[current.mPerson] = 0;
		paymentPerPerson[current.mPerson] += current.mValue;
	}
	return paymentPerPerson;
}

double CostSplitCalculator::getCreditAndDebitForPerson(QString name) const
{
	double retval = 0;

	for (unsigned i=0; i<mDebts.size(); ++i)
	{
		QString creditor = mDebts[i].first;
		QString debitor = mDebts[i].second.mPerson;
		double value =  mDebts[i].second.mValue;

		if (name==creditor)
			retval += value;
		if (name==debitor)
			retval -= value;
	}

	return retval;
}

double CostSplitCalculator::getTotalPayment(const std::map<QString, double>& paymentPerPerson) const
{
	double totalPayment = 0;
	for (std::map<QString, double>::const_iterator iter=paymentPerPerson.begin(); iter!=paymentPerPerson.end(); ++iter)
		totalPayment += iter->second;
	return totalPayment;
}

std::vector<Payment> CostSplitCalculator::getPayments() const
{
	return mPayments;
}

void CostSplitCalculator::addDebtFromDebitorToCreditor(double value, QString debitor, QString creditor, QString description, QDate date)
{
	mDebts.push_back(std::make_pair(creditor, Payment(debitor, value, description, QStringList(), date)));
}
