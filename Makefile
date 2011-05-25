
clean:
	find . -name "*.pyc" |xargs rm || true

test: clean
	py.test -x test
