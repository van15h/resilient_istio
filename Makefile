start-cameras:
	curl http://localhost:35060/production?toggle=on

stop-cameras:
	curl http://localhost:35060/production?toggle=off