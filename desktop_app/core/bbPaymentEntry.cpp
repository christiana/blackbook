#include "bbPaymentEntry.h"

namespace bb
{

PaymentEntryPtr PaymentEntry::create(const Payment& payment, PersonListPtr personList)
{
	PaymentEntryPtr retval(new PaymentEntry());
	retval->mPayment = payment;
	retval->mPersonList = personList;
	return retval;
}

PaymentEntry::PaymentEntry()
{

}

Payment PaymentEntry::getPayment() const
{
	return mPayment;
}

void PaymentEntry::setPayment(Payment payment)
{
	mPayment = payment;
}

void PaymentEntry::addXml(QDomElement node)
{
	mPayment.addXml(node);
}

void PaymentEntry::parseXml(QDomElement node)
{
	mPayment.parseXml(node);
}

double PaymentEntry::getBalanceForPerson(QString name) const
{
	double retval = 0;
	if (mPayment.mPerson==name)
		retval += mPayment.mValue;
	double fraction = this->getFractionForPerson(name);
	retval -= fraction * mPayment.mValue;
	return retval;
}

double PaymentEntry::getFractionForPerson(QString name) const
{
	QStringList participants = mPayment.mParticipants;
	if (participants.empty())
		participants = mPersonList->getPersons();

	if (!participants.contains(name))
		return 0;

	double totalWeight = 0;
	for (unsigned i=0; i<participants.size(); ++i)
		totalWeight += mPersonList->getWeight(participants[i]);

	double weight = mPersonList->getWeight(name);
	return weight/totalWeight;
}

bool PaymentEntry::equal(const EntryPtr other) const
{
	PaymentEntryPtr rhs = boost::dynamic_pointer_cast<PaymentEntry>(other);
	return rhs && (mPayment==rhs->getPayment());
//	return mPayment==other.mPayment;
}

} // namespace bb

