#ifndef BBTESTCATCHIMPL_H_
#define BBTESTCATCHIMPL_H_

#include "boost/shared_ptr.hpp"
#include "catch.hpp"

namespace Catch
{
class Session;
}

namespace bbtest
{

/**
 * Wrapper for Catch framework.
 *
 * Contains a few addons:
 * - if "--list-tests" AND "--reporter xml" is input,
 *   override normal behaviour to output a xml-formatted name list.
 *   (used in scripting - the default list format is not parse-friendly)
 * - if no tests are run, return failure.
 *   (required by ctest: a config error in ctest-catch should give a failure)
 *
 * \author christiana
 * \date Jun 28, 2013
 */
class CatchImpl
{
public:
	CatchImpl();
	int run(int argc, char* argv[]);
private:
	bool shouldListTestsInCustomXml();
	void listTestsAsXml();
	int countTests();
	std::vector<Catch::TestCase> getMatchingTests();

	boost::shared_ptr<Catch::Session> mSession;
};

} /* namespace bbtest */
#endif /* BBTESTCATCHIMPL_H_ */
