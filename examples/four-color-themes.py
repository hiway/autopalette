from autopalette import (

    # Renderers
    AnsiTruecolorRenderer,
    Ansi256Renderer,
    Ansi16Renderer,
    Ansi8Renderer,
    AnsiNoColorRenderer,

    # Palettes
    FourColorTheme,
    Gray4Palette,
    GameBoyGreenPalette,
    GameBoyChocolatePalette,
    Oil6Palette,
)

for palette in [Gray4Palette,
                GameBoyGreenPalette,
                GameBoyChocolatePalette,
                Oil6Palette]:
    print()
    print('Using palette: ', palette.__name__)

    for renderer in [AnsiTruecolorRenderer,
                     Ansi256Renderer,
                     Ansi16Renderer,
                     Ansi8Renderer,
                     AnsiNoColorRenderer]:
        print('\twith renderer: ', renderer.__name__, end='\n\t\t')

        th = FourColorTheme(
                palette=palette,
                renderer=renderer,
        )

        print(th.base('base'), end='  ')
        print(th.light('light'), end='  ')
        print(th.dark('dark'), end='  ')
        print(th.h1('header1'), end='  ')
        print(th.h2('header2'), end='  ')
        print(th.h3('header3'), end='  ')
        print('\n')
