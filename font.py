#!/usr/bin/env python

#
# font.py
#
# Exports icon fonts as PNG images.
#
# Copyright (c) 2012-2014 Michal Wojciechowski (http://odyniec.net/)
#
# Font Awesome - http://fortawesome.github.com/Font-Awesome
#

import sys, argparse, re
from os import path, access, R_OK
from PIL import Image, ImageFont, ImageDraw

# Support Unicode literals with both Python 2 and 3
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]

    def uchr(x):
        return unichr(x)
else:
    def u(x):
        return x

    def uchr(x):
        return chr(x)

# Mapping of font awesome icon names to character codes
icons = {
    "adjust": u("\uf042"),
    "adn": u("\uf170"),
    "align-center": u("\uf037"),
    "align-justify": u("\uf039"),
    "align-left": u("\uf036"),
    "align-right": u("\uf038"),
    "ambulance": u("\uf0f9"),
    "anchor": u("\uf13d"),
    "android": u("\uf17b"),
    "angle-double-down": u("\uf103"),
    "angle-double-left": u("\uf100"),
    "angle-double-right": u("\uf101"),
    "angle-double-up": u("\uf102"),
    "angle-down": u("\uf107"),
    "angle-left": u("\uf104"),
    "angle-right": u("\uf105"),
    "angle-up": u("\uf106"),
    "apple": u("\uf179"),
    "archive": u("\uf187"),
    "arrow-circle-down": u("\uf0ab"),
    "arrow-circle-left": u("\uf0a8"),
    "arrow-circle-o-down": u("\uf01a"),
    "arrow-circle-o-left": u("\uf190"),
    "arrow-circle-o-right": u("\uf18e"),
    "arrow-circle-o-up": u("\uf01b"),
    "arrow-circle-right": u("\uf0a9"),
    "arrow-circle-up": u("\uf0aa"),
    "arrow-down": u("\uf063"),
    "arrow-left": u("\uf060"),
    "arrow-right": u("\uf061"),
    "arrow-up": u("\uf062"),
    "arrows": u("\uf047"),
    "arrows-alt": u("\uf0b2"),
    "arrows-h": u("\uf07e"),
    "arrows-v": u("\uf07d"),
    "asterisk": u("\uf069"),
    "backward": u("\uf04a"),
    "ban": u("\uf05e"),
    "bar-chart-o": u("\uf080"),
    "barcode": u("\uf02a"),
    "bars": u("\uf0c9"),
    "beer": u("\uf0fc"),
    "bell": u("\uf0f3"),
    "bell-o": u("\uf0a2"),
    "bitbucket": u("\uf171"),
    "bitbucket-square": u("\uf172"),
    "bitcoin": u("\uf15a"),
    "bold": u("\uf032"),
    "bolt": u("\uf0e7"),
    "book": u("\uf02d"),
    "bookmark": u("\uf02e"),
    "bookmark-o": u("\uf097"),
    "briefcase": u("\uf0b1"),
    "btc": u("\uf15a"),
    "bug": u("\uf188"),
    "building-o": u("\uf0f7"),
    "bullhorn": u("\uf0a1"),
    "bullseye": u("\uf140"),
    "calendar": u("\uf073"),
    "calendar-o": u("\uf133"),
    "camera": u("\uf030"),
    "camera-retro": u("\uf083"),
    "caret-down": u("\uf0d7"),
    "caret-left": u("\uf0d9"),
    "caret-right": u("\uf0da"),
    "caret-square-o-down": u("\uf150"),
    "caret-square-o-left": u("\uf191"),
    "caret-square-o-right": u("\uf152"),
    "caret-square-o-up": u("\uf151"),
    "caret-up": u("\uf0d8"),
    "certificate": u("\uf0a3"),
    "chain": u("\uf0c1"),
    "chain-broken": u("\uf127"),
    "check": u("\uf00c"),
    "check-circle": u("\uf058"),
    "check-circle-o": u("\uf05d"),
    "check-square": u("\uf14a"),
    "check-square-o": u("\uf046"),
    "chevron-circle-down": u("\uf13a"),
    "chevron-circle-left": u("\uf137"),
    "chevron-circle-right": u("\uf138"),
    "chevron-circle-up": u("\uf139"),
    "chevron-down": u("\uf078"),
    "chevron-left": u("\uf053"),
    "chevron-right": u("\uf054"),
    "chevron-up": u("\uf077"),
    "circle": u("\uf111"),
    "circle-o": u("\uf10c"),
    "clipboard": u("\uf0ea"),
    "clock-o": u("\uf017"),
    "cloud": u("\uf0c2"),
    "cloud-download": u("\uf0ed"),
    "cloud-upload": u("\uf0ee"),
    "cny": u("\uf157"),
    "code": u("\uf121"),
    "code-fork": u("\uf126"),
    "coffee": u("\uf0f4"),
    "cog": u("\uf013"),
    "cogs": u("\uf085"),
    "columns": u("\uf0db"),
    "comment": u("\uf075"),
    "comment-o": u("\uf0e5"),
    "comments": u("\uf086"),
    "comments-o": u("\uf0e6"),
    "compass": u("\uf14e"),
    "compress": u("\uf066"),
    "copy": u("\uf0c5"),
    "credit-card": u("\uf09d"),
    "crop": u("\uf125"),
    "crosshairs": u("\uf05b"),
    "css3": u("\uf13c"),
    "cut": u("\uf0c4"),
    "cutlery": u("\uf0f5"),
    "dashboard": u("\uf0e4"),
    "dedent": u("\uf03b"),
    "desktop": u("\uf108"),
    "dollar": u("\uf155"),
    "dot-circle-o": u("\uf192"),
    "download": u("\uf019"),
    "dribbble": u("\uf17d"),
    "dropbox": u("\uf16b"),
    "edit": u("\uf044"),
    "eject": u("\uf052"),
    "ellipsis-h": u("\uf141"),
    "ellipsis-v": u("\uf142"),
    "envelope": u("\uf0e0"),
    "envelope-o": u("\uf003"),
    "eraser": u("\uf12d"),
    "eur": u("\uf153"),
    "euro": u("\uf153"),
    "exchange": u("\uf0ec"),
    "exclamation": u("\uf12a"),
    "exclamation-circle": u("\uf06a"),
    "exclamation-triangle": u("\uf071"),
    "expand": u("\uf065"),
    "external-link": u("\uf08e"),
    "external-link-square": u("\uf14c"),
    "eye": u("\uf06e"),
    "eye-slash": u("\uf070"),
    "facebook": u("\uf09a"),
    "facebook-square": u("\uf082"),
    "fast-backward": u("\uf049"),
    "fast-forward": u("\uf050"),
    "female": u("\uf182"),
    "fighter-jet": u("\uf0fb"),
    "file": u("\uf15b"),
    "file-o": u("\uf016"),
    "file-text": u("\uf15c"),
    "file-text-o": u("\uf0f6"),
    "files-o": u("\uf0c5"),
    "film": u("\uf008"),
    "filter": u("\uf0b0"),
    "fire": u("\uf06d"),
    "fire-extinguisher": u("\uf134"),
    "flag": u("\uf024"),
    "flag-checkered": u("\uf11e"),
    "flag-o": u("\uf11d"),
    "flash": u("\uf0e7"),
    "flask": u("\uf0c3"),
    "flickr": u("\uf16e"),
    "floppy-o": u("\uf0c7"),
    "folder": u("\uf07b"),
    "folder-o": u("\uf114"),
    "folder-open": u("\uf07c"),
    "folder-open-o": u("\uf115"),
    "font": u("\uf031"),
    "forward": u("\uf04e"),
    "foursquare": u("\uf180"),
    "frown-o": u("\uf119"),
    "gamepad": u("\uf11b"),
    "gavel": u("\uf0e3"),
    "gbp": u("\uf154"),
    "gear": u("\uf013"),
    "gears": u("\uf085"),
    "gift": u("\uf06b"),
    "github": u("\uf09b"),
    "github-alt": u("\uf113"),
    "github-square": u("\uf092"),
    "gittip": u("\uf184"),
    "glass": u("\uf000"),
    "globe": u("\uf0ac"),
    "google-plus": u("\uf0d5"),
    "google-plus-square": u("\uf0d4"),
    "group": u("\uf0c0"),
    "h-square": u("\uf0fd"),
    "hand-o-down": u("\uf0a7"),
    "hand-o-left": u("\uf0a5"),
    "hand-o-right": u("\uf0a4"),
    "hand-o-up": u("\uf0a6"),
    "hdd-o": u("\uf0a0"),
    "headphones": u("\uf025"),
    "heart": u("\uf004"),
    "heart-o": u("\uf08a"),
    "home": u("\uf015"),
    "hospital-o": u("\uf0f8"),
    "html5": u("\uf13b"),
    "inbox": u("\uf01c"),
    "indent": u("\uf03c"),
    "info": u("\uf129"),
    "info-circle": u("\uf05a"),
    "inr": u("\uf156"),
    "instagram": u("\uf16d"),
    "italic": u("\uf033"),
    "jpy": u("\uf157"),
    "key": u("\uf084"),
    "keyboard-o": u("\uf11c"),
    "krw": u("\uf159"),
    "laptop": u("\uf109"),
    "leaf": u("\uf06c"),
    "legal": u("\uf0e3"),
    "lemon-o": u("\uf094"),
    "level-down": u("\uf149"),
    "level-up": u("\uf148"),
    "lightbulb-o": u("\uf0eb"),
    "link": u("\uf0c1"),
    "linkedin": u("\uf0e1"),
    "linkedin-square": u("\uf08c"),
    "linux": u("\uf17c"),
    "list": u("\uf03a"),
    "list-alt": u("\uf022"),
    "list-ol": u("\uf0cb"),
    "list-ul": u("\uf0ca"),
    "location-arrow": u("\uf124"),
    "lock": u("\uf023"),
    "long-arrow-down": u("\uf175"),
    "long-arrow-left": u("\uf177"),
    "long-arrow-right": u("\uf178"),
    "long-arrow-up": u("\uf176"),
    "magic": u("\uf0d0"),
    "magnet": u("\uf076"),
    "mail-forward": u("\uf064"),
    "mail-reply": u("\uf112"),
    "mail-reply-all": u("\uf122"),
    "male": u("\uf183"),
    "map-marker": u("\uf041"),
    "maxcdn": u("\uf136"),
    "medkit": u("\uf0fa"),
    "meh-o": u("\uf11a"),
    "microphone": u("\uf130"),
    "microphone-slash": u("\uf131"),
    "minus": u("\uf068"),
    "minus-circle": u("\uf056"),
    "minus-square": u("\uf146"),
    "minus-square-o": u("\uf147"),
    "mobile": u("\uf10b"),
    "mobile-phone": u("\uf10b"),
    "money": u("\uf0d6"),
    "moon-o": u("\uf186"),
    "music": u("\uf001"),
    "outdent": u("\uf03b"),
    "pagelines": u("\uf18c"),
    "paperclip": u("\uf0c6"),
    "paste": u("\uf0ea"),
    "pause": u("\uf04c"),
    "pencil": u("\uf040"),
    "pencil-square": u("\uf14b"),
    "pencil-square-o": u("\uf044"),
    "phone": u("\uf095"),
    "phone-square": u("\uf098"),
    "picture-o": u("\uf03e"),
    "pinterest": u("\uf0d2"),
    "pinterest-square": u("\uf0d3"),
    "plane": u("\uf072"),
    "play": u("\uf04b"),
    "play-circle": u("\uf144"),
    "play-circle-o": u("\uf01d"),
    "plus": u("\uf067"),
    "plus-circle": u("\uf055"),
    "plus-square": u("\uf0fe"),
    "plus-square-o": u("\uf196"),
    "power-off": u("\uf011"),
    "print": u("\uf02f"),
    "puzzle-piece": u("\uf12e"),
    "qrcode": u("\uf029"),
    "question": u("\uf128"),
    "question-circle": u("\uf059"),
    "quote-left": u("\uf10d"),
    "quote-right": u("\uf10e"),
    "random": u("\uf074"),
    "refresh": u("\uf021"),
    "renren": u("\uf18b"),
    "repeat": u("\uf01e"),
    "reply": u("\uf112"),
    "reply-all": u("\uf122"),
    "retweet": u("\uf079"),
    "rmb": u("\uf157"),
    "road": u("\uf018"),
    "rocket": u("\uf135"),
    "rotate-left": u("\uf0e2"),
    "rotate-right": u("\uf01e"),
    "rouble": u("\uf158"),
    "rss": u("\uf09e"),
    "rss-square": u("\uf143"),
    "rub": u("\uf158"),
    "ruble": u("\uf158"),
    "rupee": u("\uf156"),
    "save": u("\uf0c7"),
    "scissors": u("\uf0c4"),
    "search": u("\uf002"),
    "search-minus": u("\uf010"),
    "search-plus": u("\uf00e"),
    "share": u("\uf064"),
    "share-square": u("\uf14d"),
    "share-square-o": u("\uf045"),
    "shield": u("\uf132"),
    "shopping-cart": u("\uf07a"),
    "sign-in": u("\uf090"),
    "sign-out": u("\uf08b"),
    "signal": u("\uf012"),
    "sitemap": u("\uf0e8"),
    "skype": u("\uf17e"),
    "smile-o": u("\uf118"),
    "sort": u("\uf0dc"),
    "sort-alpha-asc": u("\uf15d"),
    "sort-alpha-desc": u("\uf15e"),
    "sort-amount-asc": u("\uf160"),
    "sort-amount-desc": u("\uf161"),
    "sort-asc": u("\uf0dd"),
    "sort-desc": u("\uf0de"),
    "sort-down": u("\uf0dd"),
    "sort-numeric-asc": u("\uf162"),
    "sort-numeric-desc": u("\uf163"),
    "sort-up": u("\uf0de"),
    "spinner": u("\uf110"),
    "square": u("\uf0c8"),
    "square-o": u("\uf096"),
    "stack-exchange": u("\uf18d"),
    "stack-overflow": u("\uf16c"),
    "star": u("\uf005"),
    "star-half": u("\uf089"),
    "star-half-empty": u("\uf123"),
    "star-half-full": u("\uf123"),
    "star-half-o": u("\uf123"),
    "star-o": u("\uf006"),
    "step-backward": u("\uf048"),
    "step-forward": u("\uf051"),
    "stethoscope": u("\uf0f1"),
    "stop": u("\uf04d"),
    "strikethrough": u("\uf0cc"),
    "subscript": u("\uf12c"),
    "suitcase": u("\uf0f2"),
    "sun-o": u("\uf185"),
    "superscript": u("\uf12b"),
    "table": u("\uf0ce"),
    "tablet": u("\uf10a"),
    "tachometer": u("\uf0e4"),
    "tag": u("\uf02b"),
    "tags": u("\uf02c"),
    "tasks": u("\uf0ae"),
    "terminal": u("\uf120"),
    "text-height": u("\uf034"),
    "text-width": u("\uf035"),
    "th": u("\uf00a"),
    "th-large": u("\uf009"),
    "th-list": u("\uf00b"),
    "thumb-tack": u("\uf08d"),
    "thumbs-down": u("\uf165"),
    "thumbs-o-down": u("\uf088"),
    "thumbs-o-up": u("\uf087"),
    "thumbs-up": u("\uf164"),
    "ticket": u("\uf145"),
    "times": u("\uf00d"),
    "times-circle": u("\uf057"),
    "times-circle-o": u("\uf05c"),
    "tint": u("\uf043"),
    "toggle-down": u("\uf150"),
    "toggle-left": u("\uf191"),
    "toggle-right": u("\uf152"),
    "toggle-up": u("\uf151"),
    "trash-o": u("\uf014"),
    "trello": u("\uf181"),
    "trophy": u("\uf091"),
    "truck": u("\uf0d1"),
    "try": u("\uf195"),
    "tumblr": u("\uf173"),
    "tumblr-square": u("\uf174"),
    "turkish-lira": u("\uf195"),
    "twitter": u("\uf099"),
    "twitter-square": u("\uf081"),
    "umbrella": u("\uf0e9"),
    "underline": u("\uf0cd"),
    "undo": u("\uf0e2"),
    "unlink": u("\uf127"),
    "unlock": u("\uf09c"),
    "unlock-alt": u("\uf13e"),
    "unsorted": u("\uf0dc"),
    "upload": u("\uf093"),
    "usd": u("\uf155"),
    "user": u("\uf007"),
    "user-md": u("\uf0f0"),
    "users": u("\uf0c0"),
    "video-camera": u("\uf03d"),
    "vimeo-square": u("\uf194"),
    "vk": u("\uf189"),
    "volume-down": u("\uf027"),
    "volume-off": u("\uf026"),
    "volume-up": u("\uf028"),
    "warning": u("\uf071"),
    "weibo": u("\uf18a"),
    "wheelchair": u("\uf193"),
    "windows": u("\uf17a"),
    "won": u("\uf159"),
    "wrench": u("\uf0ad"),
    "xing": u("\uf168"),
    "xing-square": u("\uf169"),
    "yen": u("\uf157"),
    "youtube": u("\uf167"),
    "youtube-play": u("\uf16a"),
    "youtube-square": u("\uf166"),
}


class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for icon in sorted(icons.keys()):
            print(icon)
        exit(0)


class ListUpdateAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print("icons = {")
        for icon in sorted(icons.keys()):
            print(u'    "%s": u("\\u%x"),' % (icon, ord(icons[icon])))
        print("}")
        exit(0)


def export_icon(icon, size, filename, font, color, xy):
    image = Image.new("RGBA", (size, size), color=(0,0,0,0))

    draw = ImageDraw.Draw(image)

    # Initialize font
    font = ImageFont.truetype(font, size)

    # Determine the dimensions of the icon
    width,height = draw.textsize(icons[icon], font=font)

    xy = ((size - width) / 2 if xy[0] is None else xy[0],
          (size - height) / 2 if xy[1] is None else xy[1])
    draw.text(xy, icons[icon], font=font, fill=color)

    # Get bounding box
    bbox = image.getbbox()

    if bbox:
        image = image.crop(bbox)

    borderw = int((size - (bbox[2] - bbox[0])) / 2)
    borderh = int((size - (bbox[3] - bbox[1])) / 2)

    # Create background image
    bg = Image.new("RGBA", (size, size), (0,0,0,0))

    bg.paste(image, (borderw,borderh))

    # Save file
    bg.save(filename)


class LoadCSSAction():
    def __init__(self, filename, font_class_prefix):
        import tinycss
        global icons
        new_icons = {}
        parser = tinycss.make_parser("page3")
        stylesheet = parser.parse_stylesheet_file(filename)
        is_icon = re.compile(u("\.%s(.*):before,?" % font_class_prefix))
        for rule in stylesheet.rules:
            selector = rule.selector.as_css()
            for match in is_icon.finditer(selector):
                name = match.groups()[0]
                for declaration in rule.declarations:
                    if declaration.name == u"content":
                        val = declaration.value.as_css()
                        if val.startswith('"') and val.endswith('"'):
                            val = val[1:-1]
                        try:
                            new_icons[name] = uchr(int(val[1:], 16))
                        except UnicodeEncodeError:
                            new_icons[name] = val[1:]
                        except ValueError:
                            new_icons[name] = u(val[1:])
                        except:
                            pass
        icons = new_icons


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="Exports icon fonts as PNG images.")

    parser.add_argument("icon", type=str, nargs="+",
            help="The name(s) of the icon(s) to export (or \"ALL\" for all icons)")
    parser.add_argument("--color", type=str, default="black",
            help="Color (HTML color code or name, default: black)")
    parser.add_argument("--filename", type=str,
            help="The name of the output file (it must end with \".png\"). If " +
            "all files are exported, it is used as a prefix.")
    parser.add_argument("--font", type=str, default="fontawesome-webfont.ttf",
            help="Font file to use (default: fontawesome-webfont.ttf)")
    parser.add_argument("--font-class-prefix", type=str, default="fa-",
            help="The prefix of the CSS font class (default: fa-)")
    parser.add_argument("--css", type=str, default="",
            help="Path to the CSS file defining icon names (instead of the " +
            "predefined list)")
    parser.add_argument("--list", nargs=0, action=ListAction,
            help="List available icon names and exit")
    parser.add_argument("--list-update", nargs=0, action=ListUpdateAction,
            help=argparse.SUPPRESS)
    parser.add_argument("--size", type=int, default=16,
            help="Icon size in pixels (default: 16)")
    parser.add_argument("--x", type=int, default=None,
            help="x offset of the font image")
    parser.add_argument("--y", type=int, default=None,
            help="y offset of the font image")

    args = parser.parse_args()
    icon = args.icon
    size = args.size
    font = args.font
    css = args.css
    color = args.color
    xy = (args.x, args.y)
    
    if css:
        LoadCSSAction(css, args.font_class_prefix)

    if args.font:
        if not path.isfile(args.font) or not access(args.font, R_OK):
            print >> sys.stderr, ("Error: Font file (%s) can't be opened"
                    % (args.font))
            exit(1)

    if args.icon == [ "ALL" ]:
        # Export all icons
        selected_icons = sorted(icons.keys())
    else:
        selected_icons = []

        # Icon name was given
        for icon in args.icon:
            # Strip the "icon-" prefix, if present
            if icon.startswith("icon-"):
                icon = icon[5:]

            if icon in icons:
                selected_icons.append(icon)
            else:
                print >> sys.stderr, "Error: Unknown icon name (%s)" % (icon)
                sys.exit(1)

    for icon in selected_icons:
        if len(selected_icons) > 1:
            # Exporting multiple icons -- treat the filename option as name prefix
            filename = (args.filename or "") + icon + ".png"
        else:
            # Exporting one icon
            if args.filename:
                filename = args.filename
            else:
                filename = icon + ".png"

        print("Exporting icon \"%s\" as %s (%ix%i pixels)" %
                (icon, filename, size, size))

        export_icon(icon, size, filename, font, color, xy)
