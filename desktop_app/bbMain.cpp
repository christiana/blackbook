
#include <QApplication>
#include <iostream>
#include "bbMainWindow.h"

int main(int argc, char *argv[])
{
//  Q_INIT_RESOURCE(cxResources);
  
  QApplication app(argc, argv);
  app.setApplicationName("BlackBook");
//  app.setWindowIcon(QIcon(":/icons/CustusX.png"));
  app.setAttribute(Qt::AA_DontShowIconsInMenus, false);

  bb::MainWindow* mainWin = new bb::MainWindow;

#ifdef __APPLE__ // needed on mac for bringing to front: does the opposite on linux
  mainWin->activateWindow();
#endif
  mainWin->raise();

  int retVal = app.exec();

  delete mainWin;
  return retVal;  
}
