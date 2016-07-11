#include "bbUtilities.h"
#include <cmath>

namespace bb
{

bool near_equal(double a, double b)
{
	return fabs(a-b) < 1.0E-3;
}
QString dateFormatString()
{
	return "yyyy-MM-dd";
}

} // namespace bb


