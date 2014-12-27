#ifndef BBTABLEMODEL_H
#define BBTABLEMODEL_H

#include <QAbstractTableModel>
#include "boost/shared_ptr.hpp"
#include <set>

namespace bb
{
typedef boost::shared_ptr<class CostSplitCalculator> CostSplitCalculatorPtr;

/**
 *
 * A QAbstractModel for this project.
 *
 * \date 2014-12-27
 * \author christiana
 */
class TableModel : public QAbstractTableModel
{
	Q_OBJECT
public:
	explicit TableModel(QObject *parent, CostSplitCalculatorPtr costSplitter);
	virtual QString getTitle() = 0;
signals:

public slots:
	virtual void costSplitterChangedSlot();
	virtual void onCopyToClipboard();
	virtual void onPasteFromClipboard();
protected:
	CostSplitCalculatorPtr mCostSplitter;
	QDate parseDateString(QString raw) const;
};


} // namespace bb

#endif // BBTABLEMODEL_H
