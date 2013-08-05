#include "bbCostSplitCalculator.h"

#include <map>
#include <iostream>
#include <cmath>
#include <QDomElement>
#include <QFile>
#include <QTextStream>
#include "bbXmlFile.h"
#include "bbUtilities.h"
#include "bbDebtEntry.h"

namespace bb
{

CostSplitCalculator::CostSplitCalculator()
{
	mPersons.reset(new PersonList);
}

void CostSplitCalculator::addPerson(QString name)
{
	mPersons->addPerson(name);
	emit calculatorChanged();
}

void CostSplitCalculator::addWeight(QString name, double weight)
{
	mPersons->addWeight(name, weight);
	emit calculatorChanged();
}

double CostSplitCalculator::getWeight(QString name) const
{
	return mPersons->getWeight(name);
}

QStringList CostSplitCalculator::getPersons() const
{
	return mPersons->getPersons();
}
void CostSplitCalculator::removePerson(QString name)
{
	if (mPersons->removePerson(name))
		emit calculatorChanged();
}

double CostSplitCalculator::getBalance(QString name) const
{
	double retval = 0;
	for (unsigned i=0; i<mEntries.size(); ++i)
		retval += mEntries[i]->getBalanceForPerson(name);
	return retval;
}

void CostSplitCalculator::save(QString filename)
{
	XmlFile file;
	this->addXml(file.document().documentElement());
	file.save(filename);
}

void CostSplitCalculator::addXml(QDomElement node)
{
	QDomDocument doc = node.ownerDocument();
	QDomElement personsNode = XmlFile::addChild(node, "persons");
	mPersons->addXml(personsNode);

	QDomElement paymentsNode = XmlFile::addChild(node, "payments");
	for (unsigned i=0; i<mEntries.size(); ++i)
	{
		QDomElement paymentNode = XmlFile::addChild(paymentsNode, "payment");
		paymentNode.setAttribute("type", mEntries[i]->getType());
		mEntries[i]->addXml(paymentNode);
	}
}

void CostSplitCalculator::load(QString filename)
{
	XmlFile file;
	if (!file.load(filename))
		return;

	QDomNode rootNode = file.document().namedItem("root");
	this->parseXml(rootNode.toElement());
}

void CostSplitCalculator::parseXml(QDomElement node)
{
	QDomElement personsNode = node.namedItem("persons").toElement();
	mPersons->parseXml(personsNode);

	QDomNode paymentsNode = node.namedItem("payments");
	QDomElement paymentNode = paymentsNode.firstChildElement("payment");
	for (; !paymentNode.isNull(); paymentNode = paymentNode.nextSiblingElement("payment"))
	{
		QString type = paymentNode.attribute("type");
		EntryPtr entry = this->createEntry(type, mPersons);
		entry->parseXml(paymentNode);
		mEntries.push_back(entry);
	}
}

EntryPtr CostSplitCalculator::createEntry(QString type, PersonListPtr persons)
{
	if (type=="payment")
		return PaymentEntry::create(Payment(), persons);
	else if (type=="debt")
		return DebtEntry::create(Debt(), persons);
	return EntryPtr();
}

bool CostSplitCalculator::operator==(const CostSplitCalculator &other) const
{
	if (this->mEntries.size()!=other.mEntries.size())
		return false;
	for (unsigned i=0; i<mEntries.size(); ++i)
		if (!this->mEntries[i]->equal(other.mEntries[i]))
			return false;
	return (*this->mPersons==*other.mPersons);
}

bool CostSplitCalculator::operator!=(const CostSplitCalculator &other) const
{
	return !(*this == other);
}


void CostSplitCalculator::addPayment(Payment payment)
{
	mEntries.push_back(PaymentEntry::create(payment, mPersons));
	emit calculatorChanged();
}
Payment CostSplitCalculator::getPayment(int index) const
{
	return this->getPayments()[index]->getPayment();
}
int CostSplitCalculator::getPaymentsCount() const
{
	return this->getPayments().size();
}
void CostSplitCalculator::removePayment(int index)
{
	this->remove(this->getPayments()[index]);
}
void CostSplitCalculator::setPayment(int index, Payment payment)
{
	this->getPayments()[index]->setPayment(payment);
	emit calculatorChanged();
}

void CostSplitCalculator::addDebt(Debt debt)
{
	mEntries.push_back(DebtEntry::create(debt, mPersons));
	emit calculatorChanged();
}
void CostSplitCalculator::setDebt(int index, Debt debt)
{
	this->getDebts()[index]->setDebt(debt);
	emit calculatorChanged();
}
Debt CostSplitCalculator::getDebt(int index) const
{
	return this->getDebts()[index]->getDebt();
}
void CostSplitCalculator::removeDebt(int index)
{
	this->remove(this->getDebts()[index]);
}
int CostSplitCalculator::getDebtsCount() const
{
	return this->getDebts().size();
}

std::vector<EntryPtr> CostSplitCalculator::getEntries()
{
	return mEntries;
}

void CostSplitCalculator::remove(EntryPtr entry)
{
	mEntries.erase(std::find(mEntries.begin(), mEntries.end(), entry));
}

std::vector<PaymentEntryPtr> CostSplitCalculator::getPayments() const
{
	return this->getEntriesOfType<PaymentEntry>();
}

std::vector<DebtEntryPtr> CostSplitCalculator::getDebts() const
{
	return this->getEntriesOfType<DebtEntry>();
}

template<class ENTRY_TYPE>
std::vector<boost::shared_ptr<ENTRY_TYPE> > CostSplitCalculator::getEntriesOfType() const
{
	typedef boost::shared_ptr<ENTRY_TYPE> ENTRY_TYPE_PTR;
	std::vector<ENTRY_TYPE_PTR> retval;
	for (unsigned i=0; i<mEntries.size(); ++i)
	{
		ENTRY_TYPE_PTR current = boost::dynamic_pointer_cast<ENTRY_TYPE>(mEntries[i]);
		if (current)
			retval.push_back(current);
	}
	return retval;
}

} // namespace bb
