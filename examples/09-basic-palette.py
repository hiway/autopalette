from autopalette import af

print(af("No formatting."))

print(af("Hello, world!").id)
print(af("Hello, world!").id256)

print(af("Plain text.").p)
print(af("Light text.").light)
print(af("Dark text.").dark)

print(af("Header One").h1)
print(af("Header Two").h2.b)
print(af("Header Three").h3.i)
print(af("Header Four").h4.u)

print(af("List element").li)

print(af("An error!").err)
print(af("A warning.").warn)
print(af("Some information.").info)
print(af("All is good.").ok)

print(af("Bold").b)
print(af("Muted").m)
print(af("Italic").i)
print(af("Reversed").r)
print(af("Underline").u)
