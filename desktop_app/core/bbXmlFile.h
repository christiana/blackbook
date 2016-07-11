#ifndef BBXMLFILE_H
#define BBXMLFILE_H

#include <QDomDocument>

namespace bb
{

/**
 *
 *
 * \date 04.08.2013
 * \author christiana
 */
class XmlFile
{
public:
	XmlFile();
	void save(QString filename);
	bool load(QString filename);
	QDomDocument document();
	static QDomElement addChild(QDomElement node, QString name);
private:
	QDomDocument mDocument;
};

} // namespace bb

#endif // BBXMLFILE_H
