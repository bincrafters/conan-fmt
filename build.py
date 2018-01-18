#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default

if __name__ == "__main__":

    builder = build_template_default.get_builder()

    # Add one extra build to create a header-only version
    if platform.system() == "Linux" and os.getenv("CONAN_GCC_VERSIONS", False) == "6.3":
        builder.add({}, {"fmt:header_only" : True}, {}, {})
    
    builder.run()

    