Font to PNG
===================

This program allows you to extract any icon font as PNG images of the specified 
size and color.

### Usage

    font-to-png.py [-h] [--color COLOR] [--filename FILENAME]
                        [--font FONT] [--font-class-prefix FONTCLASSPREFIX]
                        [--css CSS] [--list] [--size SIZE] [--x X] [--y Y]
                        icon [icon ...]

    positional arguments:
      icon                                 The name(s) of the icon(s) to export
                                           (or "ALL" for all icons)

    optional arguments:
      --color COLOR                        Color (HTML color code or name,
                                           default: black)
      --filename FILENAME                  The name of the output file (it must
                                           end with ".png"). If all files are
                                           exported, it is used as a prefix.
      --font FONT                          Font file to use (default:
                                           fontawesome-webfont.ttf)
      --font-class-prefix FONTCLASSPREFIX  The prefix of the CSS font class
                                           (default: fa-)
      --css CSS                            Path to the CSS file defining icon
                                           names (instead of the predefined list)
      --list                               List available icon names and exit
      --size SIZE                          Icon size in pixels (default: 16)
      --x X                                x offset of the font image
      --y Y                                y offset of the font image

    hidden optional arguments:
     --list-update         List available icon names and codes in format suitable
                           for updating the program source.

To use the program, you need the TTF file for a font icon. The default is Font
Awesome, which is available in
[Font Awesome Github repository](https://github.com/FortAwesome/Font-Awesome).

The following Python libraries are needed (install them by running
"pip install -r requirements.txt"):
* Pillow (or the Python Imaging Library)
* tinycss (optional: only needed if you are using the --css option)

The internal icon list is matched to Font Awesome 4.0.3.  To use a later/different
version, use font-awesome.css from the Font Awesome GitHub repository.

### Examples

Export the "play" and "stop" icons as 24x24 pixels images:

    font-to-png.py --size 24 play stop

Export the asterisk icon as 32x32 pixels image, in blue:

    font-to-png.py --size 32 --color blue asterisk

Export all icons as 16x16 pixels images:

    font-to-png.py ALL

Export all icons in the [Pika](https://symbolset.com/icons/pika) font:

    font-to-png.py --font ss-pika.ttf --css ss-pika.css --font-class-prefix "ss-" --x 0 --y -1 ALL
