#include "bbXmlFile.h"

#include <QFile>
#include <QTextStream>
#include <iostream>

namespace bb
{

XmlFile::XmlFile()
{
	mDocument.appendChild(mDocument.createProcessingInstruction("xml version =", "'1.0'"));
	QDomElement rootNode = mDocument.createElement("root");
	mDocument.appendChild(rootNode);
}

QDomDocument XmlFile::document()
{
	return mDocument;
}

void XmlFile::save(QString filename)
{
//	this->addXml(rootNode);

	QFile file(filename);
	if (file.open(QIODevice::WriteOnly | QIODevice::Truncate))
	{
		QTextStream stream(&file);
		stream << mDocument.toString(4);
		file.close();
	}
	else
	{
		std::cout << "Save error: Could not open " + file.fileName().toStdString() << std::endl;
	}
}

bool XmlFile::load(QString filename)
{
	QFile file(filename);
	if (file.open(QIODevice::ReadOnly))
	{
//		QDomDocument doc;
		QString emsg;
		int eline, ecolumn;
		if (mDocument.setContent(&file, false, &emsg, &eline, &ecolumn))
		{
			return true;
//			QDomNode rootNode = mDocument.namedItem("root");
//			this->parseXml(rootNode.toElement());
		}
		else
		{
			std::cout << QString("Could not parse XML file :" + file.fileName() + " because: " + emsg + "").toStdString() << std::endl;
		}
	}
	return false;
}

} // namespace bb


