from PIL import Image
import sys
import os.path

def do_file( file, lengths, set_height ):
    directory = os.path.dirname( file )
    localfile = os.path.splitext( os.path.basename( file ) )
    basename = localfile[ 0 ]
    extension = localfile[ 1 ]
    image = Image.open( file )
    sizes_directory = f"{directory}/sizes"
    size = image.size
    root_width = size[ 0 ]
    root_height = size[ 1 ]
    if os.path.exists( sizes_directory ):
        if not os.path.isdir( sizes_directory ):
            return f"{sizes_directory} already exists & is not a directory."
    else:
        try:
            os.mkdir( sizes_directory )
        except OSError:
            return f"Could not make directory {sizes_directory}"
    first = True
    aspect_ratio = 0
    if set_height:
        aspect_ratio = root_width / root_height
    else:
        aspect_ratio = root_height / root_width
    for length in lengths:
        width = 0
        height = 0
        if set_height:
            height = int( length )
            width = int( aspect_ratio * float( height ) )
        else:
            width = int( length )
            height = int( aspect_ratio * float( width ) )
        new_filename = f"{basename}{extension}"
        if first:
            first = False
        else:
            new_filename = f"{basename}-{width}x{height}{extension}"
        thumbnail = image.resize( ( width, height ), Image.ANTIALIAS )
        thumbnail.save( f"{sizes_directory}/{new_filename}" )
    return True

def get_arguments():
    file = None
    widths = []
    set_height = False
    first = True
    for i in range( 0, len( sys.argv ) ):
        if i is 0:
            pass
        else:
            arg = sys.argv[ i ]
            if arg == "--height" or arg == "--h":
                set_height = True
            else:
                if file == None:
                    file = arg
                else:
                    widths.append( arg )
    return ( file, widths, set_height )

def run():
    ( file, widths, set_height ) = get_arguments()
    if os.path.isdir( file ):
        for f in os.listdir( file ):
            full_filename = f"{file}/{f}"
            if os.path.isfile( full_filename ):
                message = do_file( full_filename, widths, set_height )
                if type( message ) is str:
                    return message
    else:
        return do_file( file, widths, set_height )
    return True

message = run()
if type( message ) is str:
    print( message )