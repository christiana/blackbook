#ifndef BBCOSTSPLITCALCULATOR_H
#define BBCOSTSPLITCALCULATOR_H

#include <vector>
#include <map>
#include <QStringList>
#include <QDate>
#include "boost/shared_ptr.hpp"
#include <QObject>
#include "bbPersonList.h"
#include "bbPayment.h"
#include "bbPaymentEntry.h"
#include "bbDebtEntry.h"

class QDomElement;

namespace bb
{

typedef boost::shared_ptr<class CostSplitCalculator> CostSplitCalculatorPtr;

/**
 *
 *
 * \date 30 july 2013
 * \author christiana
 */
class CostSplitCalculator : public QObject
{
	Q_OBJECT
public:

public:
	CostSplitCalculator();

	void addPerson(QString name);
	void removePerson(QString name);
	void addWeight(QString name, double weight);
	double getWeight(QString name) const;
	QStringList getPersons() const;
	double getBalance(QString name) const;
	bool verifyCalculations() const;

	void addPayment(Payment payment);
	void setPayment(int index, Payment payment);
	Payment getPayment(int index) const;
	void removePayment(int index);
	int getPaymentsCount() const;

	void addDebt(Debt debt);
	void setDebt(int index, Debt debt);
	Debt getDebt(int index) const;
	void removeDebt(int index);
	int getDebtsCount() const;

	std::vector<EntryPtr> getEntries();
	void remove(EntryPtr entry);
	std::vector<DebtEntryPtr> getDebts() const; // downcasted and filtered on NULL
	std::vector<PaymentEntryPtr> getPayments() const; // downcasted and filtered on NULL
	// set is included by modding the pointers
	// count directly on the lists
	// get on the lists
	// requirement: each entry emits signals when changed (set)

	template<class ENTRY_TYPE>
	std::vector<boost::shared_ptr<ENTRY_TYPE> > getEntriesOfType() const;

	void save(QString filename);
	void load(QString filename);

	bool operator==(const CostSplitCalculator &other) const;
	bool operator!=(const CostSplitCalculator &other) const;

signals:
	void calculatorChanged();

private:
	PersonListPtr mPersons;
	std::vector<EntryPtr> mEntries;
	void addXml(QDomElement node);
	void parseXml(QDomElement node);
	EntryPtr createEntry(QString type, PersonListPtr persons);
};

} // namespace bb

#endif // BBCOSTSPLITCALCULATOR_H
