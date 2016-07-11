#ifndef BBPAYMENT_H
#define BBPAYMENT_H

#include <QStringList>
#include <QDate>
#include <QObject>
class QDomElement;

namespace bb
{

class Payment
{
public:
	Payment() {}
	Payment(QString person, double value, QString description="", QStringList participants=QStringList(), QDate date=QDate::currentDate()) :
		mPerson(person), mValue(value), mDescription(description), mParticipants(participants), mDate(date) {}

	QString mPerson;
	double mValue;
	QString mDescription;
	QStringList mParticipants; // empty list means all parties
	QDate mDate;

	bool operator==(const Payment &other) const;
	bool operator!=(const Payment &other) const;
	void addXml(QDomElement node);
	void parseXml(QDomElement node);
};

class Debt
{
public:
	Debt() {}
	Debt(QString creditor, Payment payment) :
		mCreditor(creditor), mPayment(payment) {}

	QString mCreditor;
	Payment mPayment;

	bool operator==(const Debt &other) const;
	bool operator!=(const Debt &other) const;
	void addXml(QDomElement node);
	void parseXml(QDomElement node);
};

} // namespace cx

#endif // BBPAYMENT_H
