# autopalette

Terminal palettes and themes, without tears.

**Status: Alpha; being developed.**

Do you write python scripts that `print()` text 
on the command-line terminal? 
Do you feel the interface could convey a bit more meaning, 
but the effort needed to get it right has kept you away 
from using ANSI colors?
These things should be easy, right?

Here's a regular Python program that prints a word:

```python
print("Tring!")
```

![01-regular-print](https://user-images.githubusercontent.com/23116/40859649-0da89ab0-65d2-11e8-8026-19ba6a2ad003.png)


Here is what it looks like with autopalette,
using a shortcut called `AutoFormat` or in short: `af`.

```python
from autopalette import af

print(af("Tring!"))
```

![02-autoformat-wrapped-print](https://user-images.githubusercontent.com/23116/40859706-3b61f3c0-65d2-11e8-996b-da4e218e192c.png)


We added one line to import, 
and four characters around the string.

And it does nothing - autopalette is non-intrusive that way.
You can leave your `af`-wrapped strings around 
and they will not run unnecessary code until you ask for more.

What's more?

```python
from autopalette import af

print(af("Hello, world!").id)
print(af("Hello, world!").id256)
```

![03-id-deterministic-color](https://user-images.githubusercontent.com/23116/40859765-63bec9b0-65d2-11e8-886c-82011ea96f8b.png)

If your terminal / emulator reports that it supports color,
you should see the second line formatted in fuschia/ magenta. 
Try changing the text and observe that 
the color changes when the text changes,
but it stays fixed for the same text.
Across function calls, across program runs, 
across machines, across time itself!
Okay maybe that was too dramatic, 
but it is kind of true because, mathematics.    

Autopalette's `id` feature hashes the supplied text and generates
a color unique to the text within 
the range of colors reported by the terminal.
`id256` generates a color within the ANSI 256 palette.
`id256` is not portable, but feel free to use it 
for your personal scripts where color limits are known.

Why is this useful?

It helps to identify unique names 
that your program may output, such as:
 
  - hostnames, when working with remote machines.
  - usernames, for logs of multi-user environments.
  - you know better what matters to your program's output :)

Sometimes you want a little more...

```python
from autopalette import af

print(af("Hello again!").h1)
```

![04-header-one](https://user-images.githubusercontent.com/23116/40859801-858c3ef6-65d2-11e8-90d7-69a80fc57c57.png)


And we have a nicely decorated header, just like that.
You can use one of the several pre-defined styles,
or read further below how you can design your own.

Here are the various styles built into autopalette.

 - `p`: plain-text, or paragraph - as you like to read it.
 - `light`: where color range allows it, lighter text.
 - `dark`: darker text if terminal supports enough colors within palette.
 - `h1`: highlighted text style 1, or header-1.
 - `h2`: 
 - `h3`
 - `h4`
 - `li`: list element.
 - `err`: an error 
 - `warn`: a warning 
 - `info`: a warning 
 - `ok`: a warning 
 - `b`: bold.
 - `i`: italic.
 - `u`: underline.
 - `r`: reversed colors.
 - `raw`: useful to debug, displays the ANSI code instead of applying it.

Let us try superimposing two styles.

```python
from autopalette import af

print(af("Hey! We've met before!?").info.b)
```

![05-superimpose-styles](https://user-images.githubusercontent.com/23116/40859850-abe90afc-65d2-11e8-905d-d8a875d0f021.png)


You get the idea, tack the names of styles you want 
at the end-bracket of the call to `af`. 

If you are wondering, "Wait, what's with that weird syntax?",
in Python's spirit of quick protoyping, 
autopalette encourages experimenting with 
minimal mental and physical effort to tweak knobs.
Your program's actual task matters more,
but you care enough about your future self and users using the app
to style it well and be a delight to use.
Autopalette's syntax is an expriment to help manage this dilemma.

While you compose and read your code, 
this syntax separates the styling from rest of the function calls.
You don't have to think about styling unless you want to,
and when you do, which is often as you look at the string
you just put together to print - assuming you started with `af("`,
close the quote and bracket, type out a style shortcut 
and you are done.

Although, few times you want a bit more than that...

```python
from autopalette import af, GameBoyGreenPalette

af.init(palette=GameBoyGreenPalette)

print(af("There you are!").h1)
```

![06-select-palette](https://user-images.githubusercontent.com/23116/40860027-550d2046-65d3-11e8-9fbe-b0ecdf3ec50c.png)

Look at that! Yummy.

Autopalette goes the length to support a handful of palettes.

 - GameBoyChocolate
 - GameBoyOriginal
 - Grayscale
 - Oil
 - Arcade
 - CLRS
 
If this is exciting to you too, read further below how to create your own!

How does this look on a terminal with only 16 colors?

![06-select-palette-16-color](https://user-images.githubusercontent.com/23116/40860055-74e898aa-65d3-11e8-8bfc-3873c1ea4a4b.png)

Not too shabby, eh?

How do you test how your app will look on terminals  with limited colors?
Try these as prefix to your script invocation for a temporary change:

 - `env TERM=vt100 `
 - `env TERM=rxvt-16color `
 - `env TERM=xterm `
 - `env TERM=xterm-256color `
 - `env TERM=RGB `
 - `env NO_COLOR `

like so:

`$ env TERM=xterm-256color python app.py`

To save a setting permanently, put `export TERM=...` 
in your `~/.bash_profile` or your default shell's configuration.

If the environment variable NO_COLOR is set,
autopalette honors the configuration and disables all color.
Same with redirected output and pipes - 
autopalette will handle it fully automatically,
if it fails to do so, please open an issue in the tracker
and I'll do my best to fix it. 
In case you can fix the issue yourself, a pull request will be awesome!

And we would be essentially done, except, 
there's this little voice in the head that's saying something mojibªke something,
but it's all garbled up.

```python
from autopalette import af 

af.init(fix_text=True)

print(af("&macr;\\_(ã\x83\x84)_/&macr;").info)
```

![07-fix-text](https://user-images.githubusercontent.com/23116/40860106-abf343f4-65d3-11e8-9272-89733b0790bd.png)


Neat, with the `fix_text` option set,
autopalette transparently passes your text 
through `ftfy`'s `fix_text()` function call,
ensuring your application does not output garbage 
when badly encoded strings find their way 
to your app's print statement. 

There's more, not all terminal and emulators support unicode,
and will still produce garbage if we feed them strings 
that they do not know how to display. Use the `fix_all` option
to let autopalette and the terminal it is running on figure out the rest.

```python
from autopalette import af 

af.init(fix_all=True)

print(af("I 💛 Unicode!"))
```

Try this example with `env TERM=vt100` for the full cleanup!

![08-fix-all](https://user-images.githubusercontent.com/23116/40860125-c4f0343e-65d3-11e8-9bfe-d92f177c5852.png)

Note that fixing text and emoji requires additional libraries 
to be loaded and can slow down startup time.
If your program does not output strings generated by other programs,
(which includes strings received from http APIs!) 
and the program is invoked repeatedly instead of running for a while, 
you may want to skip `fix_...` options.

And that's about it for three-line examples!

You can start your scripts with `af.init(fix_all=True)` 
and use `af()` to wrap your strings, even if you ignore colors and styles,
your program will display text correctly
on most popular (and many obscure) terminals.

Here's the basic theme:

![09-basic-palette](https://user-images.githubusercontent.com/23116/40860445-e69d057a-65d4-11e8-9926-228beaf3c429.png)

But there's more!

Your users have the ability to define their own themes,
and autopalette will automatically* recolor your application
to their preferences or needs. 
(*mostly automatically, or with a little help.)

```text
# ~/.autopalette

palette = Dutron
render = Truecolor
```

![10-restricted-color-palette](https://user-images.githubusercontent.com/23116/40860487-0589dd50-65d5-11e8-9360-2fb29a2d213e.png)


Your terminal applications look beautiful as you intend,
to everyone, as they expect.

It is almost two decades since Y2K! 
And with over 50 years of the terminal technology behind us,
this should be a thing we expect as a norm.

Autopalette is another attempt at fixing some of these gaps
by making it near trivial to style terminal apps 
and do the right thing for the various terminals it runs on...
without the complexity often involved as a result 
of the rich legacy of the technology.

Autopalette would not dare exist without the libraries 
published by these generous individuals who made it possible 
to think and write code in simple mental models 
that are just right for the task:

 - `colorhash`: Felix Krull (https://pypi.org/project/colorhash/)
 - `colortrans.py`: Micah Elliott (https://gist.github.com/MicahElliott/719710/)
 - `colour`: Valentin LAB (https://pypi.org/project/colour/)
 - `emoji2text`: Sam CB (https://pypi.org/project/emoji2text/)
 - `ftfy`: Rob Speer / Luminoso (https://pypi.org/project/ftfy/)
 - `kdtree`: Stefan Kögl (https://pypi.org/project/kdtree/)
 - `sty`: Felix Meyer-Wolters (https://pypi.org/project/sty/)

