#ifndef BBCOSTSPLITCALCULATOR_H
#define BBCOSTSPLITCALCULATOR_H

#include <vector>
#include <map>
#include <QStringList>
#include <QDate>

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
};

/**
 *
 *
 * \date 30 july 2013
 * \author christiana
 */
class CostSplitCalculator
{
public:
	class Person
	{
	public:
		Person() : mWeight(1) {}
		explicit Person(QString name) : mName(name), mWeight(1) {}
		QString mName;
		double mWeight;
	};

public:
	CostSplitCalculator();
	void addPerson(QString name);
	void addWeight(QString name, double weight);
	QStringList getPersons() const;
	void addPayment(Payment payment);
	void addPayment(QString name, double value, QString description, QDate date);
	void addDebtFromDebitorToCreditor(double value, QString debitor, QString creditor, QString description, QDate date);
	double getBalance(QString name) const;
	std::vector<Payment> getPayments() const;

private:
	std::vector<Person> mPersons;
	std::vector<Payment> mPayments;
	std::vector<std::pair<QString, Payment> > mDebts; ///< map of (creditor,debitor)

	double getCreditAndDebitForPerson(QString name) const;
	double getCreditAndDebitForPerson(QString name, QString creditor, Payment debit) const;
	double getWeight(QString name) const;
	double getFractionForPerson(QString name, QStringList participants) const;
	double getPartOfPaymentForPerson(QString name) const;
	double getPartOfPaymentForPerson(Payment payment, QString name) const;
};

#endif // BBCOSTSPLITCALCULATOR_H
