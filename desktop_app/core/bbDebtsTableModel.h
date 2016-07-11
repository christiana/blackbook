#ifndef BBDEBTSTABLEMODEL_H
#define BBDEBTSTABLEMODEL_H

#include "bbTableModel.h"
#include "boost/shared_ptr.hpp"
#include <set>

namespace bb
{
typedef boost::shared_ptr<class CostSplitCalculator> CostSplitCalculatorPtr;

/**
 *
 * A QAbstractModel for a list of debts.
 *
 * \date 31.07.2013
 * \author christiana
 */
class DebtsTableModel : public TableModel
{
	Q_OBJECT
public:
	explicit DebtsTableModel(QObject *parent, CostSplitCalculatorPtr costSplitter);
	virtual QString getTitle() { return "Debts"; }

	virtual int rowCount(const QModelIndex& parent) const;
	virtual int columnCount(const QModelIndex& parent) const;
	virtual QVariant data(const QModelIndex& index, int role) const;
	virtual QVariant headerData(int section, Qt::Orientation orientation, int role) const;
	virtual Qt::ItemFlags flags(const QModelIndex& index) const;
	virtual bool setData(const QModelIndex& index, const QVariant& value, int role);

	void deleteRows(const std::set<int>& rows);

signals:
public slots:
	virtual void onPasteFromClipboard();
private:
	enum COLUMN_INDEX
	{
		ciDATE = 0,
		ciDEBITOR,
		ciVALUE,
		ciCREDITOR,
		ciDESCRIPTION,
		ciCOUNT
	};

	void insertLineFromClipboard(QString line);


};

} // namespace bb


#endif // BBDEBTSTABLEMODEL_H
