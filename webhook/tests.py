from django.test import TestCase

# Create your tests here.
hook1 = 'ref/heads/master'
hook2 = 'ref/heads/release/4.9.0'

hook3 = 'master'
hook4 = 'release/*'.replace('*', '')

print(hook4)

print(hook4 in hook2)