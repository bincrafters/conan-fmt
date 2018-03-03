#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class FmtConan(ConanFile):
    name = "fmt"
    version = "4.0.0"
    homepage = "https://github.com/fmtlib/fmt"
    description = "A safe and fast alternative to printf and IOStreams."
    url = "https://github.com/bincrafters/conan-fmt"
    license = "MIT"
    exports = ['LICENSE.md']
    exports_sources = ['CMakeLists.txt']
    generators = 'cmake'
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "header_only": [True, False]}
    default_options = "shared=False", "header_only=False"
    source_subfolder = "source_subfolder"
    
    def config_options(self):
        if self.options.header_only:
            self.settings.clear()
            self.options.remove("shared")

    def source(self):
        source_url = "https://github.com/fmtlib/fmt"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        
    def build(self):
        if not self.options.header_only:
            cmake = CMake(self)
            cmake.definitions["FMT_TEST"] = False
            cmake.definitions["FMT_INSTALL"] = True
            cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
            cmake.definitions["FMT_LIB_DIR"] = "lib"
            cmake.configure()
            cmake.build()
            cmake.install()

    def package(self):
        src_dir = os.path.join(self.source_subfolder, "fmt")
        dst_dir = os.path.join("include", "fmt")
        
        self.copy("LICENSE.rst", dst="license", src=self.source_subfolder, keep_path=False)
        if self.options.header_only:
            self.copy("*.h", dst=dst_dir, src=src_dir)
            self.copy("*.cc", dst=dst_dir, src=src_dir)

    def package_info(self):
        if self.options.header_only:
            self.info.header_only()
            self.cpp_info.defines = ["FMT_HEADER_ONLY"]
        else:
            self.cpp_info.libs = ["fmt"]

        if self.options.shared and not self.options.header_only:
            self.cpp_info.bindirs.append("lib")
