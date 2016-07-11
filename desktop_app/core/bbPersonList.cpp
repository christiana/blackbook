#include "bbPersonList.h"
#include "bbUtilities.h"
#include "bbXmlFile.h"

namespace bb
{

bool Person::operator==(const Person &other) const
{
	return (this->mName==other.mName) &&
		   near_equal(this->mWeight, other.mWeight);
}
bool Person::operator!=(const Person &other) const
{
	return !(*this==other);
}
void Person::addXml(QDomElement node)
{
	node.setAttribute("name", mName);
	node.setAttribute("weight", mWeight);
}
void Person::parseXml(QDomElement node)
{
	mName = node.attribute("name");
	mWeight = node.attribute("weight").toDouble();
}
///--------------------------------------------------------
///--------------------------------------------------------
///--------------------------------------------------------

bool PersonList::operator==(const PersonList &other) const
{
	return (this->mPersons==other.mPersons);
}

bool PersonList::operator!=(const PersonList &other) const
{
  return !(*this == other);
}

void PersonList::addPerson(QString name)
{
	mPersons.push_back(Person(name));
//	emit calculatorChanged();
//	std::cout << "added person " << name.toStdString() << std::endl;
}

void PersonList::addWeight(QString name, double weight)
{
	int pos = this->findIndexOfPerson(name);
	if (pos<0)
		return;
	mPersons[pos].mWeight = weight;
}

int PersonList::findIndexOfPerson(QString name) const
{
	for (unsigned i=0; i<mPersons.size(); ++i)
		if (mPersons[i].mName==name)
			return i;
	return -1;
}

double PersonList::getWeight(QString name) const
{
	for (unsigned i=0; i<mPersons.size(); ++i)
	{
		if (mPersons[i].mName!=name)
			continue;
		return mPersons[i].mWeight;
	}
	return 0;
}

QStringList PersonList::getPersons() const
{
	QStringList retval;
	for (unsigned i=0; i<mPersons.size(); ++i)
		retval << mPersons[i].mName;
	return retval;
}

bool PersonList::removePerson(QString name)
{
	int pos = this->findIndexOfPerson(name);
	if (pos<0)
		return false;
	mPersons.erase(mPersons.begin()+pos);
	return true;
}

void PersonList::addXml(QDomElement node)
{
//	QDomDocument doc = node.ownerDocument();
	for (unsigned i=0; i<mPersons.size(); ++i)
	{
		QDomElement personNode = XmlFile::addChild(node, "person");
		mPersons[i].addXml(personNode);
	}
}

void PersonList::parseXml(QDomElement node)
{
	mPersons.clear();

	//QDomNode personsNode = node.namedItem("persons");
	QDomElement personNode = node.firstChildElement("person");
	for (; !personNode.isNull(); personNode = personNode.nextSiblingElement("person"))
	{
		Person person;
		person.parseXml(personNode);
		mPersons.push_back(person);
	}
}

} // namespace bb


