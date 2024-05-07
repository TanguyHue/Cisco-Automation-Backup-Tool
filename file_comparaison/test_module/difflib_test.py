from difflib import unified_diff, ndiff

a = """The cat is sleeping on the red sofa."""
b = """The cat is sleeping on a blue sofa..."""

diff = unified_diff(a.splitlines(), b.splitlines(), lineterm='')
print('\n'.join(list(diff)))

c = '''1
2
3
4
5'''

d = '''1
3
4
5
6'''

diff = ndiff(c.splitlines(),d.splitlines())

print('\n'.join(list(diff)))