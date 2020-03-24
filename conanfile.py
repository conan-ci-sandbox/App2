from conans import ConanFile, CMake

class App2(ConanFile):
    name = "App2"
    version = "1.0"

    settings = "os", "arch", "compiler", "build_type"

    generators = "cmake"

    scm = {"type": "git",
           "url": "https://github.com/conan-ci-cd-training/App2.git",
           "revision": "auto"}

    exports_sources = "LICENSE" # to avoid build info bug

    def requirements(self):
        self.requires("libC/1.0@mycompany/stable")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE", dst="licenses")
