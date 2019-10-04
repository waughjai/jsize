from PIL import Image
import sys
import os.path

def get_arguments():
    file = None
    widths = []
    flags = { "set_height": False, "gen_info": False, "info_only": False }
    first = True
    for i in range( 0, len( sys.argv ) ):
        if i is 0:
            pass
        else:
            arg = sys.argv[ i ]
            if arg == "--height" or arg == "-h":
                flags[ "set_height" ] = True
            elif arg == "--info" or arg == "-i":
                flags[ "gen_info" ] = True
            elif arg == "--info-only" or arg == "-I":
                flags[ "info_only" ] = True
                flags[ "gen_info" ] = True
            else:
                if file == None:
                    file = arg
                else:
                    widths.append( arg )
    return ( file, widths, flags )

def setup_new_directory( directory, local ):
    full_directory = f"{directory}/{local}"
    if os.path.exists( full_directory ):
        if not os.path.isdir( full_directory ):
            return ( None, f"{full_directory} already exists & is not a directory." )
    else:
        try:
            os.mkdir( full_directory )
        except OSError:
            return ( None, f"Could not make directory {full_directory}" )
    return ( full_directory, None )

def calculate_aspect_ratio( set_height, root_width, root_height ):
    return root_width / root_height if set_height else root_height / root_width

def generate_width_and_height( set_height, length, root_width, root_height ):
    aspect_ratio = calculate_aspect_ratio( set_height, root_width, root_height )
    return ( int( aspect_ratio * float( length ) ), int( length ) ) if set_height else ( int( length ), int( aspect_ratio * float( length ) ) )

def do_file( file, lengths, flags ):
    directory = os.path.dirname( file )
    localfile = os.path.splitext( os.path.basename( file ) )
    basename = localfile[ 0 ]
    extension = localfile[ 1 ]
    image = Image.open( file )
    size = image.size
    root_width = size[ 0 ]
    root_height = size[ 1 ]
    sizes_directory, sizes_directory_error = setup_new_directory( directory, "sizes" )
    if sizes_directory_error:
        return sizes_directory_error
    info_directory = None
    if ( flags[ "gen_info" ] ):
        info_directory, info_directory_error = setup_new_directory( directory, "info" )
        if info_directory_error:
            return info_directory_error
    first = True
    length_strings = [ f"{root_width}w" ]
    for length in lengths:
        width, height = generate_width_and_height( flags[ "set_height" ], length, root_width, root_height )
        if first:
            first = False
        if not flags[ "gen_info" ]:
            new_filename = f"{basename}{extension}" if first else f"{basename}-{width}x{height}{extension}"
            thumbnail = image.resize( ( width, height ), Image.ANTIALIAS )
            thumbnail.save( f"{sizes_directory}/{new_filename}" )
        length_strings.append( f"{width}w {height}h" )
    if info_directory:
        length_strings.reverse() # Python loves mutation in-place :(
        full_length_string = ", ".join( length_strings )
        info_file = open( f"{info_directory}/{basename}.txt", "w+" )
        info_file.write( full_length_string )
        info_file.close()
    return True

def run():
    ( file, widths, flags ) = get_arguments()
    if os.path.isdir( file ):
        for f in os.listdir( file ):
            full_filename = f"{file}/{f}"
            if os.path.isfile( full_filename ):
                message = do_file( full_filename, widths, flags )
                if type( message ) is str:
                    return message
    else:
        return do_file( file, widths, flags )
    return True

message = run()
if type( message ) is str:
    print( message )