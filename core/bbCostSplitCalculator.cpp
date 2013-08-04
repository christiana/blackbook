#include "bbCostSplitCalculator.h"

#include <map>
#include <iostream>
#include <cmath>
#include <QDomElement>
#include <QFile>
#include <QTextStream>
#include "bbXmlFile.h"

namespace bb
{

namespace
{
bool near_equal(double a, double b)
{
	return fabs(a-b) < 1.0E-3;
}
QString dateFormatString()
{
	return "yyyy-MM-dd";
}
}

bool Payment::operator==(const Payment &other) const
{
	return (this->mPerson==other.mPerson) &&
			near_equal(this->mValue, other.mValue) &&
			(this->mDescription==other.mDescription) &&
			(this->mParticipants==other.mParticipants) &&
			(this->mDate==other.mDate);
}

bool Payment::operator!=(const Payment &other) const
{
  return !(*this == other);
}

void Payment::addXml(QDomElement node)
{
	node.setAttribute("person", mPerson);
	node.setAttribute("value", mValue);
	node.setAttribute("description", mDescription);
	node.setAttribute("participants", mParticipants.join(";"));
	node.setAttribute("date", mDate.toString(dateFormatString()));
}

void Payment::parseXml(QDomElement node)
{
	mPerson = node.attribute("person");
	mValue = node.attribute("value").toDouble();
	mDescription = node.attribute("description");
	mParticipants = node.attribute("participants").split(";");
	mParticipants.removeAll("");
	mDate = QDate::fromString(node.attribute("date"), dateFormatString());
}

///--------------------------------------------------------
///--------------------------------------------------------
///--------------------------------------------------------

bool CostSplitCalculator::Person::operator==(const Person &other) const
{
	return (this->mName==other.mName) &&
		   near_equal(this->mWeight, other.mWeight);
}
bool CostSplitCalculator::Person::operator!=(const Person &other) const
{
	return !(*this==other);
}
void CostSplitCalculator::Person::addXml(QDomElement node)
{
	node.setAttribute("name", mName);
	node.setAttribute("weight", mWeight);
}
void CostSplitCalculator::Person::parseXml(QDomElement node)
{
	mName = node.attribute("name");
	mWeight = node.attribute("weight").toDouble();
}
///--------------------------------------------------------
///--------------------------------------------------------
///--------------------------------------------------------

CostSplitCalculator::CostSplitCalculator()
{
}

void CostSplitCalculator::addPerson(QString name)
{
	mPersons.push_back(Person(name));
	emit calculatorChanged();
//	std::cout << "added person " << name.toStdString() << std::endl;
}

void CostSplitCalculator::addWeight(QString name, double weight)
{
	int pos = this->findIndexOfPerson(name);
	if (pos<0)
		return;
	mPersons[pos].mWeight = weight;
	emit calculatorChanged();
}

int CostSplitCalculator::findIndexOfPerson(QString name) const
{
	for (unsigned i=0; i<mPersons.size(); ++i)
		if (mPersons[i].mName==name)
			return i;
	return -1;
}

double CostSplitCalculator::getWeight(QString name) const
{
	for (unsigned i=0; i<mPersons.size(); ++i)
	{
		if (mPersons[i].mName!=name)
			continue;
		return mPersons[i].mWeight;
	}
	return 0;
}

QStringList CostSplitCalculator::getPersons() const
{
	QStringList retval;
	for (unsigned i=0; i<mPersons.size(); ++i)
		retval << mPersons[i].mName;
	return retval;
}

void CostSplitCalculator::addPayment(Payment payment)
{
	mPayments.push_back(payment);
	emit calculatorChanged();
}

void CostSplitCalculator::setPayment(int index, Payment payment)
{
	mPayments[index] = payment;
	emit calculatorChanged();
}

void CostSplitCalculator::addPayment(QString name, double value, QString description, QDate date)
{
	this->addPayment(Payment(name, value, description, QStringList(), date));
}

double CostSplitCalculator::getBalance(QString name) const
{
	double balance = 0;
	balance += this->getPartOfPaymentForPerson(name);
	balance += this->getCreditAndDebitForPerson(name);
	return balance;
}

double CostSplitCalculator::getPartOfPaymentForPerson(QString name) const
{
	double retval = 0;
	for (unsigned i=0; i<mPayments.size(); ++i)
		retval += this->getPartOfPaymentForPerson(mPayments[i], name);
	return retval;
}

double CostSplitCalculator::getPartOfPaymentForPerson(Payment payment, QString name) const
{
	double retval = 0;
	if (payment.mPerson==name)
		retval += payment.mValue;
	double fraction = this->getFractionForPerson(name, payment.mParticipants);
	retval -= fraction * payment.mValue;
	return retval;
}

double CostSplitCalculator::getFractionForPerson(QString name, QStringList participants) const
{
	if (participants.empty())
		participants = this->getPersons();

	if (!participants.contains(name))
		return 0;

	double totalWeight = 0;
	for (unsigned i=0; i<participants.size(); ++i)
		totalWeight += this->getWeight(participants[i]);

	double weight = this->getWeight(name);
	return weight/totalWeight;
}

double CostSplitCalculator::getCreditAndDebitForPerson(QString name) const
{
	double retval = 0;
	for (unsigned i=0; i<mDebts.size(); ++i)
		retval += this->getCreditAndDebitForPerson(name, mDebts[i].first, mDebts[i].second);
	return retval;
}

double CostSplitCalculator::getCreditAndDebitForPerson(QString name, QString creditor, Payment debit) const
{
	double retval = 0;
	if (name==creditor)
		retval += debit.mValue;
	if (name==debit.mPerson)
		retval -= debit.mValue;
	return retval;
}

std::vector<Payment> CostSplitCalculator::getPayments() const
{
	return mPayments;
}

void CostSplitCalculator::addDebtFromDebitorToCreditor(double value, QString debitor, QString creditor, QString description, QDate date)
{
	mDebts.push_back(std::make_pair(creditor, Payment(debitor, value, description, QStringList(), date)));
	emit calculatorChanged();
}

void CostSplitCalculator::save(QString filename)
{
	XmlFile file;
	this->addXml(file.document().documentElement());
	file.save(filename);
}

QDomElement CostSplitCalculator::addChild(QDomElement node, QString name)
{
	QDomDocument doc = node.ownerDocument();
	QDomElement childNode = doc.createElement(name);
	node.appendChild(childNode);
	return childNode;
}

void CostSplitCalculator::addXml(QDomElement node)
{
	QDomDocument doc = node.ownerDocument();
	QDomElement personsNode = this->addChild(node, "persons");
	for (unsigned i=0; i<mPersons.size(); ++i)
	{
		QDomElement personNode = this->addChild(personsNode, "person");
		mPersons[i].addXml(personNode);
	}

	QDomElement paymentsNode = this->addChild(node, "payments");
	for (unsigned i=0; i<mPayments.size(); ++i)
	{
		QDomElement paymentNode = this->addChild(paymentsNode, "payment");
		mPayments[i].addXml(paymentNode);
	}

	QDomElement debtsNode = this->addChild(node, "debts");
	for (unsigned i=0; i<mDebts.size(); ++i)
	{
		QDomElement debtNode = this->addChild(debtsNode, "debt");
		QDomElement creditorNode = this->addChild(debtNode, "creditor");
		creditorNode.setAttribute("name", mDebts[i].first);

		QDomElement debitorNode = this->addChild(debtNode, "debitor");
		mDebts[i].second.addXml(debitorNode);
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
	QDomNode personsNode = node.namedItem("persons");
	QDomElement personNode = personsNode.firstChildElement("person");
	for (; !personNode.isNull(); personNode = personNode.nextSiblingElement("person"))
	{
		Person person;
		person.parseXml(personNode);
		mPersons.push_back(person);
	}

	QDomNode paymentsNode = node.namedItem("payments");
	QDomElement paymentNode = paymentsNode.firstChildElement("payment");
	for (; !paymentNode.isNull(); paymentNode = paymentNode.nextSiblingElement("payment"))
	{
		Payment payment;
		payment.parseXml(paymentNode);
		mPayments.push_back(payment);
	}

	QDomNode debtsNode = node.namedItem("debts");
	QDomElement debtNode = debtsNode.firstChildElement("debt");
	for (; !debtNode.isNull(); debtNode = debtNode.nextSiblingElement("debt"))
	{
		QString creditor = debtNode.namedItem("creditor").toElement().attribute("creditor");
		Payment payment;
		payment.parseXml(debtNode.namedItem("debitor").toElement());
		mDebts.push_back(std::make_pair(creditor, payment));
	}
}

bool CostSplitCalculator::operator==(const CostSplitCalculator &other) const
{
		return (this->mPersons==other.mPersons) &&
				(this->mPayments==other.mPayments) &&
				(this->mDebts==other.mDebts);
}

bool CostSplitCalculator::operator!=(const CostSplitCalculator &other) const
{
  return !(*this == other);
}

void CostSplitCalculator::removePerson(QString name)
{
	int pos = this->findIndexOfPerson(name);
	if (pos<0)
		return;
	mPersons.erase(mPersons.begin()+pos);
	emit calculatorChanged();
}

void CostSplitCalculator::removePayment(int index)
{
	mPayments.erase(mPayments.begin()+index);
	emit calculatorChanged();
}

} // namespace bb
