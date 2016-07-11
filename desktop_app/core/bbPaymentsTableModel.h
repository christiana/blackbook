#ifndef BBPAYMENTSTABLEMODEL_H
#define BBPAYMENTSTABLEMODEL_H

#include "bbTableModel.h"
#include "boost/shared_ptr.hpp"
#include <set>

namespace bb
{
typedef boost::shared_ptr<class CostSplitCalculator> CostSplitCalculatorPtr;

/**
 *
 * A QAbstractModel for a list of payments.
 *
 * \date 31.07.2013
 * \author christiana
 */
class PaymentsTableModel : public TableModel
{
	Q_OBJECT
public:
	explicit PaymentsTableModel(QObject *parent, CostSplitCalculatorPtr costSplitter);
	virtual QString getTitle() { return "Payments"; }

	virtual int rowCount(const QModelIndex& parent) const;
	virtual int columnCount(const QModelIndex& parent) const;
	virtual QVariant data(const QModelIndex& index, int role) const;
	virtual QVariant headerData(int section, Qt::Orientation orientation, int role) const;
	virtual Qt::ItemFlags flags(const QModelIndex& index) const;
	virtual bool setData(const QModelIndex& index, const QVariant& value, int role);

	void deleteRows(const std::set<int>& rows);

signals:

public slots:
//	virtual void costSplitterChangedSlot();
	virtual void onCopyToClipboard();
	virtual void onPasteFromClipboard();
private:
//	CostSplitCalculatorPtr mCostSplitter;
	int columnCount() const;
	QString getParticipantForColumn(int column) const;
	void insertLineFromClipboard(QString line);

	enum COLUMN_INDEX
	{
		ciDATE = 0,
		ciPERSON,
		ciVALUE,
		ciDESCRIPTION,
		ciPARTICIPANT_START
	};
};


} // namespace bb

#endif // BBPAYMENTSTABLEMODEL_H
