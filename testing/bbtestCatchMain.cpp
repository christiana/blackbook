// Warning:
//
// This main function is intended to be included by the cmake macro
// cx_catch_add_lib_and_exe(). Do not add to any libs!

#include "bbtestCatchImpl.h"

int main (int argc, char* argv[])
{
	return bbtest::CatchImpl().run(argc, argv);
}

