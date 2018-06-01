from autopalette import af, DutronPalette

af.init()
af.init(palette=DutronPalette)

print(af("No formatting."))

print(af("Hashed color.").id)

print(af("Plain text, colored within palette.").p)
print(af("Light text.").light)
print(af("Dark text.").dark)

print(af("Header One").h1)
print(af("Header Two").h2)
print(af("Header Three").h3)
print(af("Header Four").h4)

print(af("List element").li)

print(af("An error!").err)
print(af("A warning.").warn)
print(af("Some information.").info)
print(af("All is good.").ok)

print(af("Bold").b)
print(af("Muted").m)
print(af("Italic").i)
print(af("Underline").u)
print(af("Reversed").r)
