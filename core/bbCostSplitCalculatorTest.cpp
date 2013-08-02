#include "catch.hpp"
#include "bbCostSplitCalculator.h"

using namespace bb;

TEST_CASE("CostSplitCalculator: Add 3 persons, get list of those people", "[unit]")
{
	CostSplitCalculator calculator;
	calculator.addPerson("CA");
	calculator.addPerson("SAH");
	calculator.addPerson("HEA");

	QStringList persons = calculator.getPersons();

	CHECK(persons.size()==3);
	CHECK(persons.contains("CA"));
	CHECK(persons.contains("SAH"));
	CHECK(persons.contains("HEA"));
}

class CostSplitCalculatorTestFixture
{
public:
	CostSplitCalculatorTestFixture()
	{
		persons.push_back("CA");
		persons.push_back("SAH");
		persons.push_back("HEA");

		payments.push_back(Payment("CA", 300, "Test payment of 300€.", QStringList(), QDate(2013, 07, 29)));
		payments.push_back(Payment("SAH", 600, "Test payment of 600€.", QStringList(), QDate(2013, 07, 30)));
	}

	void addPersons()
	{
		for (unsigned i=0; i<this->persons.size(); ++i)
			calculator.addPerson(this->persons[i]);
	}

	void addPayments()
	{
		for (unsigned i=0; i<this->payments.size(); ++i)
			calculator.addPayment(this->payments[i].mPerson, this->payments[i].mValue, this->payments[i].mDescription, this->payments[i].mDate);
	}

	void checkPaymentEqual(Payment lhs, Payment rhs)
	{
		CHECK(lhs.mPerson == rhs.mPerson);
		CHECK(lhs.mValue == Approx(rhs.mValue));
		CHECK(lhs.mDescription == rhs.mDescription);
		CHECK(lhs.mDate == rhs.mDate);
	}

	CostSplitCalculator calculator;
	QStringList persons;
	std::vector<Payment> payments;
};

TEST_CASE("CostSplitCalculator: Add 2 payments, get list of those payments", "[unit]")
{
	CostSplitCalculatorTestFixture fixture;
	fixture.addPersons();
	fixture.addPayments();

	std::vector<Payment> payments = fixture.calculator.getPayments();
	fixture.checkPaymentEqual(fixture.payments[0], payments[0]);
}

TEST_CASE("CostSplitCalculator: Add payment, get balance for each person", "[unit]")
{
	CostSplitCalculator calculator;
	calculator.addPerson("CA");
	calculator.addPerson("SAH");
	calculator.addPerson("HEA");
	calculator.addPayment("CA", 300, "Test payment of 300€.", QDate(2013, 07, 30));

	CHECK(calculator.getBalance("CA") == 200);
	CHECK(calculator.getBalance("SAH") == -100);
	CHECK(calculator.getBalance("HEA") == -100);
}

TEST_CASE("CostSplitCalculator: Add person-person transaction, get balance for each person", "[unit]")
{
	CostSplitCalculator calculator;
	calculator.addPerson("CA");
	calculator.addPerson("SAH");
	calculator.addPerson("HEA");
	calculator.addDebtFromDebitorToCreditor(300, "CA", "HEA", "Test CA owing 300€ to HEA.", QDate(2013, 8, 1));

	CHECK(calculator.getBalance("CA") == -300);
	CHECK(calculator.getBalance("SAH") == 0);
	CHECK(calculator.getBalance("HEA") == 300);
}

TEST_CASE("CostSplitCalculator: Add payment and person-person transaction, get balance for each person", "[unit]")
{
	CostSplitCalculator calculator;
	calculator.addPerson("CA");
	calculator.addPerson("SAH");
	calculator.addPerson("HEA");
	calculator.addPayment("CA", 300, "Test payment of 300€.", QDate(2013, 07, 30));
	calculator.addDebtFromDebitorToCreditor(300, "CA", "HEA", "Test CA owing 300€ to HEA.", QDate(2013, 8, 1));

	CHECK(calculator.getBalance("CA") == -100);
	CHECK(calculator.getBalance("SAH") == -100);
	CHECK(calculator.getBalance("HEA") == 200);
}

TEST_CASE("CostSplitCalculator: Add weighted persons, add payment, get balance for each person", "[unit]")
{
	CostSplitCalculator calculator;
	calculator.addPerson("CA");
	calculator.addPerson("SAH");
	calculator.addPerson("HEA");
	calculator.addWeight("CA", 2);
	calculator.addPayment("CA", 300, "Test payment of 300€.", QDate(2013, 07, 30));

	CHECK(calculator.getBalance("CA") == 150);
	CHECK(calculator.getBalance("SAH") == -75);
	CHECK(calculator.getBalance("HEA") == -75);
}

TEST_CASE("CostSplitCalculator: Add payment with fewer participants than all persons, get balance for each person", "[unit]")
{
	CostSplitCalculatorTestFixture fixture;
	fixture.addPersons();
//	fixture.calculator.addPayment(Payment("CA", 300));
	fixture.calculator.addPayment(Payment("SAH", 600, "description", QStringList() << "CA" << "SAH"));

	CHECK(fixture.calculator.getBalance("CA") == -300);  // -300      = -300
	CHECK(fixture.calculator.getBalance("SAH") == 300);  // -300 +600 =  300
	CHECK(fixture.calculator.getBalance("HEA") ==   0); //           = 0
}

TEST_CASE("CostSplitCalculator: Add 2 payments with differing participants, get balance for each person", "[unit]")
{
	CostSplitCalculatorTestFixture fixture;
	fixture.addPersons();
	fixture.calculator.addPayment(Payment("CA", 300));
	fixture.calculator.addPayment(Payment("SAH", 600, "description", QStringList() << "CA" << "SAH"));

	CHECK(fixture.calculator.getBalance("CA") == -100);  // -100 +300 -300      = -100
	CHECK(fixture.calculator.getBalance("SAH") == 200);  // -100      -300 +600 =  200
	CHECK(fixture.calculator.getBalance("HEA") == -100); // -100                = -100
}

TEST_CASE("CostSplitCalculator: Create 2 identical instances of calculator, check for equality", "[unit]")
{
	CostSplitCalculatorTestFixture fixture;
	fixture.addPersons();
	fixture.addPayments();

	CostSplitCalculatorTestFixture fixture2;
	fixture2.addPersons();
	fixture2.addPayments();

	CHECK(fixture.calculator == fixture2.calculator);
}

TEST_CASE("CostSplitCalculator: Create 2 different instances of calculator, check for nonequality", "[unit]")
{
	CostSplitCalculatorTestFixture fixture;
	fixture.addPersons();
	fixture.addPayments();
	fixture.calculator.addPayment(Payment("SAH", 300, "description", QStringList() << "CA" << "SAH"));

	CostSplitCalculatorTestFixture fixture2;
	fixture2.addPersons();
	fixture2.addPayments();

	CHECK(fixture.calculator != fixture2.calculator);
}

TEST_CASE("CostSplitCalculator: Save and load instance, check for identity", "[unit]")
{
	CostSplitCalculatorTestFixture fixture;
	fixture.addPersons();
//	fixture.addPayments();
	fixture.calculator.addPayment(Payment("SAH", 300, "description"));

	QString filename = "CostSplitCalculator_test.xml";
	fixture.calculator.save(filename);

	CostSplitCalculator loadedCalculator;
	loadedCalculator.load(filename);
	loadedCalculator.save("CostSplitCalculator_test_resaved.xml");

	CHECK(fixture.calculator == loadedCalculator);
}

