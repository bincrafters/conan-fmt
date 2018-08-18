#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class FmtConan(ConanFile):
    name = "fmt"
    version = "5.1.0"
    homepage = "https://github.com/fmtlib/fmt"
    description = "A safe and fast alternative to printf and IOStreams."
    url = "https://github.com/bincrafters/conan-fmt"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ['LICENSE.md']
    exports_sources = ['CMakeLists.txt']
    generators = 'cmake'
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "header_only": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "header_only=False", "fPIC=True"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if self.options.header_only:
            self.settings.clear()
            self.options.remove("shared")
            self.options.remove("fPIC")

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["FMT_DOC"] = False
        cmake.definitions["FMT_TEST"] = False
        cmake.definitions["FMT_INSTALL"] = True
        cmake.definitions["FMT_LIB_DIR"] = "lib"
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        if not self.options.header_only:
            cmake = self.configure_cmake()
            cmake.build()

    def package(self):
        self.copy("LICENSE.rst", dst="licenses", src=self.source_subfolder, keep_path=False)
        if self.options.header_only:
            src_dir = os.path.join(self.source_subfolder, "src")
            header_dir = os.path.join(self.source_subfolder, "include")
            dst_dir = os.path.join("include", "fmt")
            self.copy("*.h", dst="include", src=header_dir)
            self.copy("*.cc", dst=dst_dir, src=src_dir)
        else:
            cmake = self.configure_cmake()
            cmake.install()

    def package_info(self):
        if self.options.header_only:
            self.info.header_only()
            self.cpp_info.defines = ["FMT_HEADER_ONLY"]
        else:
            self.cpp_info.libs = tools.collect_libs(self)
            if self.options.shared:
                self.cpp_info.defines.append('FMT_SHARED')
                self.cpp_info.bindirs.append("lib")
