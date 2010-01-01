#!/usr/bin/env python
# encoding: latin1

class A(object):
    def foo(self):
        print 'Foo'
        x=2
        y=3
    	return x, y


    def bar(self, an_argument):
        print 'Bar', an_argument

ble= A()
y=ble.foo()
print y

