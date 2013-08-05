#ifndef BBENTRY_H
#define BBENTRY_H

#include "boost/shared_ptr.hpp"
#include <QDomElement>
#include <QString>

namespace bb
{

typedef boost::shared_ptr<class Entry> EntryPtr;

/**
 *
 *
 * \date 04.08.2013
 * \author christiana
 */
class Entry
{
public:
	Entry() {}
	virtual ~Entry() {}
	virtual double getBalanceForPerson(QString name) const = 0;
	virtual void addXml(QDomElement node) = 0;
	virtual void parseXml(QDomElement node) = 0;
	virtual bool equal(const EntryPtr other) const = 0;
	virtual QString getType() const = 0;
};

} // namespace bb

#endif // BBENTRY_H
