# ***Getting your webpages live on the Web***

""" Hosting = You can pay a hosting company who will let you store your files live on their server. Even with hosting, you will need a domain name (ex. amazon.com, google.com). It has to be uniqued compared to any out there. DNS registers your domain name system. You must purchase a domain name as well. (Just Host, iPage, HostGator, Google Cloud, Amazon Web Service AWS)"""

# FTP - File Transfer Protocol - Transfering your files to a server (Can use application like fileZilla)

# ***Using comments in our code***

""" Comments are notes in your code which will not be interpreted by the browser and will not show up on the webpage. Makes understanding your code easier to follow and find stuff later."""

# HTML: <!-- the comment text here -->
# CSS: /* comment here */

# ***CSS Syntax, Precedence & Inheritance"***
"""CSS rules how the content will be displayed """
# how to apply more than one CSS rule per page:
    #padding, background-color, font-family, color, font-size, margin-bottom, text-align, text-decoration, border, background-image, width, etc.
    # curly braces show the declaration block that goes with each selector
    # inline > embedded > external

# ***FONTS!!!***
    #Web safe fonts - fonts recognized by any browser and do not need to be installed on a users computer or imported from another server.

    #Downloaded fonts will need to be embedded into your CSS code to specify the pathway where the fonts are taken.

    #The at-import and at-font face rules should be at the very top of your css files before any other. Similar to calling functions from modules in python.

    # Rule to make a font the same across the page is "font-family:"

    # you can add additional fonts in case the user did not have access to a certain font, example: 
        # font-family: Arial, Verdana, sans-serif;

    # ONLY USE VERY READABLE FONTS FOR LARGE GROUPS OF TEXTS. DO NOT USE MORE THAN 2 DIFFERENT FONTS ON YOUR PAGE.

# ***COLORS***
    # 3 Different ways color values can used in CSS:
        # Color names
        # Hexadecimal codes
        # RGB values

    # When every pixel is all the way on, it is all F's or all the way on. If a pixel is off it is black or 0's

    # with rgb values they are represented from a range of 0 to 255 ex:
        # black = rgb(0,0,0)
        # white = rgb(255,255,255)
        # yellow = rgb(255,255,0)
    # you can add an alpha value, a, which specifies opactiy
        # 0.0 = invisible
        # 1.0 = totally visible
        # rgb(0,0,0,0.5) = black is at 50% opactiy