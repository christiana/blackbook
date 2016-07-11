#ifndef BBDEBTENTRY_H
#define BBDEBTENTRY_H

#include "bbEntry.h"
#include "bbPayment.h"
#include "bbPersonList.h"

namespace bb
{

typedef boost::shared_ptr<class DebtEntry> DebtEntryPtr;

/**
 *
 * \date 04.08.2013
 * \author christiana
 */
class DebtEntry : public Entry
{
public:
	static DebtEntryPtr create(const Debt& debt, PersonListPtr personList);

	virtual double getBalanceForPerson(QString name) const;
	Debt getDebt() const;
	void setDebt(Debt debt);
	virtual void addXml(QDomElement node);
	virtual void parseXml(QDomElement node);
	virtual bool equal(const EntryPtr other) const;
	virtual QString getType() const { return "debt"; }
private:
	DebtEntry();
	Debt mDebt;
	PersonListPtr mPersonList;
};

} // namespace bb

#endif // BBDEBTENTRY_H
