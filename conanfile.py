from conans import ConanFile, CMake

class App2(ConanFile):
    name = "App2"
    version = "1.0"

    settings = "os", "arch", "compiler", "build_type"

    generators = "cmake"

    scm = {"type": "git",
           "url": "/git_server/App2.git",
           "revision": "auto"}

    def requirements(self):
        self.requires("libC/1.0@mycompany/stable")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE", dst="licenses")
