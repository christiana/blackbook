#ifndef BBPAYMENTENTRY_H
#define BBPAYMENTENTRY_H

#include "bbEntry.h"
#include "bbPayment.h"
#include "bbPersonList.h"

namespace bb
{

typedef boost::shared_ptr<class PaymentEntry> PaymentEntryPtr;

/**
 *
 *
 * \date 04.08.2013
 * \author christiana
 */
class PaymentEntry : public Entry
{
public:
	static PaymentEntryPtr create(const Payment& payment, PersonListPtr personList);

	virtual double getBalanceForPerson(QString name) const;
	Payment getPayment() const;
	void setPayment(Payment payment);
	virtual void addXml(QDomElement node);
	virtual void parseXml(QDomElement node);
	virtual bool equal(const EntryPtr other) const;
	virtual QString getType() const { return "payment"; }
private:
	PaymentEntry();
	double getFractionForPerson(QString name) const;
	Payment mPayment;
	PersonListPtr mPersonList;
};

} // namespace bb

#endif // BBPAYMENTENTRY_H
