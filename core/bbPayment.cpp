#include "bbPayment.h"
#include "bbUtilities.h"
#include <QDomElement>
#include "bbXmlFile.h"

namespace bb
{

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

bool Debt::operator==(const Debt &other) const
{
	return (mCreditor==other.mCreditor) &&
			(mPayment==other.mPayment);
}

bool Debt::operator!=(const Debt &other) const
{
	return !(*this==other);
}

void Debt::addXml(QDomElement node)
{
	QDomElement creditorNode = XmlFile::addChild(node, "creditor");
	creditorNode.setAttribute("name", mCreditor);

	QDomElement debitorNode = XmlFile::addChild(node, "debitor");
	mPayment.addXml(debitorNode);
}

void Debt::parseXml(QDomElement node)
{
	mCreditor = node.namedItem("creditor").toElement().attribute("name");
	mPayment.parseXml(node.namedItem("debitor").toElement());
}

} // namespace bb
