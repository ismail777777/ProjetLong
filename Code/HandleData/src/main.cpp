#include <iostream>
#include <vector>
#include <filesystem>
#include <cstdlib>
#include <sys/wait.h>
#include <unistd.h>

namespace fs = std::filesystem;

// Function to execute ASTConsumer with the .c/.h file as an argument
void execute_astconsumer(const fs::path& file_path) {
   //std::string outputDirName = file_path.extension() == ".c" ? "i_ext_c" : "i_ext_h";
    //fs::path outputDir = file_path.parent_path() / outputDirName;
    //fs::create_directories(outputDir);

    pid_t pid = fork();
    if (pid == 0) { // Child process
        // Construct the output file path
        //std::string outputPath = (outputDir / file_path.filename()).string();
        execl("../build/ASTConsumer", "ASTConsumer", file_path.c_str(), /*outputPath.c_str(),*/ (char*)NULL);
        // If execl returns, it must have failed
        std::cerr << "Failed to execute ASTConsumer" << std::endl;
        exit(EXIT_FAILURE);
    } else if (pid > 0) { // Parent process
        int status;
        waitpid(pid, &status, 0); // Wait for the child process to finish
    } else { // Fork failed
        std::cerr << "Fork failed" << std::endl;
    }
}

int main() {
    // Directories to search for .c and .h files
/*     std::vector<fs::path> directories = {
        "/mnt/d/1GenAI/EN_embedded_networking",
        "/mnt/d/1GenAI/DSP_digital_signal_processing_embedded_systems",
        "/mnt/d/1GenAI/EG_embedded_graphics",
        "/mnt/d/1GenAI/EH_embedded_hardware",
        "/mnt/d/1GenAI/M1_microcontroller_architecture",
        "RS_raltime_systems"
    }; */
    std::vector<fs::path> directories = {
        "/mnt/d/1GenAI/out-c",
    };
    for (const auto& dir : directories) {
        for (const auto& entry : fs::directory_iterator(dir)) {
            if (entry.is_regular_file() && (entry.path().extension() == ".c")) {
                execute_astconsumer(entry.path());
            }
        }
    }

    return 0;
}
