#ifndef BBPERSONLIST_H
#define BBPERSONLIST_H

#include <QDomElement>
#include "boost/shared_ptr.hpp"
#include <vector>
#include <QStringList>

namespace bb
{

class Person
{
public:
	Person() : mWeight(1) {}
	explicit Person(QString name) : mName(name), mWeight(1) {}
	QString mName;
	double mWeight;

	bool operator==(const Person &other) const;
	bool operator!=(const Person &other) const;
	void addXml(QDomElement node);
	void parseXml(QDomElement node);
};

typedef boost::shared_ptr<class PersonList> PersonListPtr;

/** 
 *
 * \date 04.08.2013
 * \author christiana
 */
class PersonList
{
public:
//	PersonList();
	bool operator==(const PersonList &other) const;
	bool operator!=(const PersonList &other) const;

	void addPerson(QString name);
	bool removePerson(QString name);
	void addWeight(QString name, double weight);
	double getWeight(QString name) const;
	QStringList getPersons() const;

	void addXml(QDomElement node);
	void parseXml(QDomElement node);

private:
	int findIndexOfPerson(QString name) const;
	std::vector<Person> mPersons;
};


} // namespace bb

#endif // BBPERSONLIST_H
