#ifndef BBPAYMENTSTABLEMODEL_H
#define BBPAYMENTSTABLEMODEL_H

#include <QAbstractTableModel>
#include "boost/shared_ptr.hpp"

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
class PaymentsTableModel : public QAbstractTableModel
{
	Q_OBJECT
public:
	explicit PaymentsTableModel(QObject *parent, CostSplitCalculatorPtr costSplitter);

	virtual int rowCount(const QModelIndex& parent) const;
	virtual int columnCount(const QModelIndex& parent) const;
	virtual QVariant data(const QModelIndex& index, int role) const;
	virtual QVariant headerData(int section, Qt::Orientation orientation, int role) const;
	virtual Qt::ItemFlags flags(const QModelIndex& index) const;
	virtual bool setData(const QModelIndex& index, const QVariant& value, int role);
signals:

public slots:
	void costSplitterChangedSlot();
private:
	CostSplitCalculatorPtr mCostSplitter;
	int columnCount() const;
	QString getParticipantForColumn(int column) const;

	enum COLUMN_INDEX
	{
		ciPERSON = 0,
		ciVALUE,
		ciDESCRIPTION,
		ciDATE,
		ciPARTICIPANT_START
	};
};


} // namespace bb

#endif // BBPAYMENTSTABLEMODEL_H
