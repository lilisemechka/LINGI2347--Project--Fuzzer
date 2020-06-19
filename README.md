I found 6 crashes:

1) success_comment_size.img: crashes the tool by using length = 1650.

2) success_height.img: crashes the tool by using height = 130.

3) success_pixels.img: crashes the tool when the list of pixels contains “75” in the first place (in this file the pixels are : 75 2e 6e 7a). Therefore, 75 is the header that crashes the program. Even if we put, for example, 75 instead of the header 02 that indicates the author name, it will also crash the program. 

4) success_version.img: crashes the tool by setting the version number to 81.

5) success_width_height.img: crashes the tool by using width = 257 and height = 257.

6) success_author_name.img: crashes the tool by setting author name ")gY9{Z2-W%$dNs7rhBiOl;3E8"NKj`)ta6.Fo<Q,@T..Oi!n'VoKEbYfaKi8tKbk". The crash does not depend on the length. I tested it with both small and larger values of the length. It occurs for different lengths (minimum length is two) and with different bytes. Therefore I suppose that there is some combination of bytes in the name that can crash the program. 
