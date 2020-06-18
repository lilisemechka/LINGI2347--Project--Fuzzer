I found 6 crashes:

1) success_comment_size.img : crashes the tool by using length = 1650.

2) success_height.img : crashes the tool by using height = 1650.

3) success_pixels.img : crashes the tool when there are bytes 75 in the pixels as it is the number of the header.

4) success_version.img : crashes the tool with the version 81

5) success_width_height.img : crashes the tool by using the width = 257 and height = 257

6) success_author_name.img : the crash does not depend on the length. I tested is with large and small numbers. It occurs for different length (minimum length is two) and with different numbers. So I suppose that there is some combination of bits in the name that can crash the program. 
