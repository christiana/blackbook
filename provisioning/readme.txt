

Setup amazon server manually:
	ssh-add test_aws_server.pem (local on cas-box)
	ssh ubuntu@cas.guttab.no
	sudo apt-get install -y python-pip
	sudo pip install flask
	git clone https://github.com/christiana/blackbook.git
	cd blackbook/pyserver
	screen
	./runserver.sh
	CTRL-A, CTRL-D
	logout
	(screen -r to get back in)
