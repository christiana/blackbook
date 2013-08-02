#ifndef BBPERSONSTABLEMODEL_H
#define BBPERSONSTABLEMODEL_H

#include <QAbstractTableModel>
#include "boost/shared_ptr.hpp"
#include <set>

namespace bb
{
typedef boost::shared_ptr<class CostSplitCalculator> CostSplitCalculatorPtr;

/**
 * A QAbstractModel for a list of persons with properties.
 *
 * \date 31.07.2013
 * \author christiana
 */
class PersonsTableModel : public QAbstractTableModel
{
	Q_OBJECT
public:
	explicit PersonsTableModel(QObject *parent, CostSplitCalculatorPtr costSplitter);
	
	virtual int rowCount(const QModelIndex& parent) const;
	virtual int columnCount(const QModelIndex& parent) const;
	virtual QVariant data(const QModelIndex& index, int role) const;
	virtual QVariant headerData(int section, Qt::Orientation orientation, int role) const;
	virtual Qt::ItemFlags flags(const QModelIndex& index) const;
	virtual bool setData(const QModelIndex& index, const QVariant& value, int role);

	void deleteRows(const std::set<int>& rows);

signals:
	
public slots:
	void costSplitterChangedSlot();
private:
	CostSplitCalculatorPtr mCostSplitter;
};

} // namespace bb

#endif // BBPERSONSTABLEMODEL_H
