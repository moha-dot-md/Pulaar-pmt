/**
 * @file Fileshandler.h
 * @author Oumar NIANG
 * @brief This file contains the main function that iterates on a given directory and processes the files.
 * @version 0.1
 * @date 2026-01-24
 * 
 * @copyright Copyright (c) 2026
 * 
 */
#pragma once
#include <filesystem>
#include <iostream>

namespace fs = std::filesystem;



/**
 * @brief This function browses a given directory and processes the files(.txt)
 *
 * @tparam
 * @tparam char*
 * @tparam F
 * @param baseDirectory
 * @param processor
 */
template <int I=0, int Limit=0, class F>
void IterOnDir(const char *baseDirectory, F &&processor)
{

    if (!fs::exists(baseDirectory) || !fs::is_directory(baseDirectory))
        throw std::runtime_error("Invalid directory");

    int i = 0;

    for (const auto &entry : fs::recursive_directory_iterator(baseDirectory))
    {
        if (entry.is_regular_file())
            processor(entry.path().string());

        ++i;

        if (I != 0 && i % I == 0)
        {
            std::cout << i << " file"
                      << (i > 1 ? "s" : "")
                      << (i > 1 ? "are" : "is") << " processed"
                      << "\n";
        }

        if (Limit != 0 && i >= Limit)
            break;
    }
}