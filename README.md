I found 6 crashes:

1) success_comment_size.img: crashes the tool by using length = 1650.

2) success_height.img: crashes the tool by using height = 1650.

3) success_pixels.img: crashes the tool when the list of pixels contains “75” in the first place. Therefore, 75 is the header that crashes the program. Even if we put, for example, 75 instead of the header 02 that indicates the author name, it will also crash the program.

4) success_version.img: crashes the tool by setting the version number to 81.

5) success_width_height.img: crashes the tool by using width = 257 and height = 257.

6) success_author_name.img: crashes the tool by setting author name "-]". The crash does not depend on the length. I tested it with both small and larger values of the length. It occurs for different lengths (minimum length is two) and with different bytes. Therefore I suppose that there is some combination of bytes in the name that can crash the program. 
