#
# This script generates a 3D galaxy from a number of parameters and stores
# it in an array. You can modify this script to store the data in a database
# or whatever your purpose is. THIS script uses the data only to generate a
# PNG with a 2D view from top of the galaxy.
#
# The algorithm used to generate the galaxy is borrowed from Ben Motz
# <motzb@hotmail.com>. The original C source code for DOS (including a 3D
# viewer) can be downloaded here:
#
# http://bits.bristol.ac.uk/motz/tep/galaxy.html
#
# Unfortunately, the original python code has been lost to time and a lack of wanting-to- search-through-several-hundred-webpages-for-one-webarchive-page. Sorry, original python guy.
#
# A fair portion of the revisions and code is from /u/_Foxtrot_ on reddit. They are much better with the python-fu than I!
#

from PIL import Image
from PIL import ImageDraw
import random
import math
import sys
# Generation parameters:

# raw_input the user's desired values
# Background color of the created PNG
PNGBGCOLOR = (0, 0, 0)

# Foreground color of the created PNG
PNGCOLOR = (255, 255, 255)

# Quick Filename
RAND = random.randrange(0, 999999)

#Parts from the Spiral generator, but uneditable
NUMARMS   = 12

ARMROTS   = 0

ARMWIDTH   = 65

FUZZ   = 15

# ---------------------------------------------------------------------------

NUMHUB = int(raw_input('Number of Core Stars <Default:2000>:') or "2000")

NUMDISK = int(raw_input('Number of Disk Stars <Default:4000>:') or "4000")

HUBRAD = float(raw_input('Radius of Core <Default:90.0>:') or "90.0")

DISKRAD = float(raw_input('Radius of Disk <Default:45.0>:') or "45.0")

MAXHUBZ = float(raw_input('Maximum Depth of Core <Default:16.0>:') or "16.0")

MAXDISKZ = float(raw_input('Maximum Depth of Arms <Default:2.0>:') or "2.0")

PNGSIZE = float(raw_input('X and Y Size of PNG <Default:1200>:') or "1200")

PNGFRAME = float(raw_input('PNG Frame Size <Default:50>:') or "50")

stars = []

def generateStars():
    # omega is the separation (in degrees) between each arm
    # Prevent div by zero error:
    if NUMARMS:
        omega = 360.0 / NUMARMS
    else:
        omega = 0.0
    i = 0
    while i < NUMDISK:
        # Choose a random distance from center
        dist = HUBRAD + random.random() * DISKRAD

        # This is the 'clever' bit, that puts a star at a given distance
        # into an arm: First, it wraps the star round by the number of
        # rotations specified.  By multiplying the distance by the number of
        # rotations the rotation is proportional to the distance from the
        # center, to give curvature
        theta = ( ( 360.0 * ARMROTS * ( dist / DISKRAD ) )
        
            # Then move the point further around by a random factor up to
            # ARMWIDTH
                + random.random() * ARMWIDTH
                
            # Then multiply the angle by a factor of omega, putting the
            # point into one of the arms
                #+ (omega * random.random() * NUMARMS )
                + omega * random.randrange( 0, NUMARMS )
                
            # Then add a further random factor, 'fuzzin' the edge of the arms
                + random.random() * FUZZ * 2.0 - FUZZ
                #+ random.randrange( -FUZZ, FUZZ )
            )
            
        # Convert to cartesian
        x = math.cos( theta * math.pi / 180.0 ) * dist
        y = math.sin( theta * math.pi / 180.0 ) * dist
        z = random.random() * MAXDISKZ * 2.0 - MAXDISKZ

        # Add star to the stars array            
        stars.append( ( x, y ,z ) )

        # Process next star
        i = i + 1
    
    # Now generate the Hub. This places a point on or under the curve
    # maxHubZ - s d^2 where s is a scale factor calculated so that z = 0 is
    # at maxHubR (s = maxHubZ / maxHubR^2) AND so that minimum hub Z is at
    # maximum disk Z. (Avoids edge of hub being below edge of disk)
    
    scale = MAXHUBZ / ( HUBRAD * HUBRAD )
    i = 0
    while i < NUMHUB:
        # Choose a random distance from center
        dist = random.random() * HUBRAD
      
        # Any rotation (points are not on arms)
        theta = random.random() * 360
        
        # Convert to cartesian
        x = math.cos( theta * math.pi / 180.0) * dist
        y = math.sin( theta * math.pi / 180.0) * dist
        z = ( random.random() * 2 - 1 ) * ( MAXHUBZ - scale * dist * dist )
        
        # Add star to the stars array
        stars.append( ( x, y, z ) )
    
        # Process next star
        i = i + 1

def drawToPNG( filename ):
    image = Image.new( "RGB", ( PNGSIZE, PNGSIZE ), PNGBGCOLOR )
    draw = ImageDraw.Draw( image )
    
    # Find maximal star distance
    max = 0
    for ( x, y, z ) in stars:
        if abs(x) > max: max = x
        if abs(y) > max: max = y
        if abs(z) > max: max = z
    
    # Calculate zoom factor to fit the galaxy to the PNG size
    factor = float( PNGSIZE - PNGFRAME * 2 ) / ( max * 2 )
    for ( x, y, z ) in stars:
        sx = factor * x + PNGSIZE / 2
        sy = factor * y + PNGSIZE / 2
        draw.point( ( sx, sy ), fill = PNGCOLOR )
      
    # Save the PNG
    image.save( filename )
          
# Generate the galaxy          
generateStars()

# Save the galaxy as PNG to galaxy.png
drawToPNG( "ringgalaxy " + str(RAND) + ".png")
