/**
 * @file Processors.h
 * @author Oumar NIANG
 * @brief This file contains the tokenizers, processing functions and helpers.
 * @version 0.1
 * @date 2026-01-24
 *
 * @copyright Copyright (c) 2026
 *
 */

#pragma once
#include <unordered_set>
#include <string>
#include <fstream>
#include <string>
#include <stdexcept>
#include <cstdint>
#include <iostream>


/**
 * @brief This is a helper function that checks the text and confirms whether it's
 * Pulaar or not.
 * @tparam char32 (for UTF-32)
 * @param character
 * @return true
 * @return false
 */
bool isPulaarLetter(char32_t character);

/**
 * @brief This converts a UTF-8 encored string to UTF-32 it is crossplatform
 * @tparam string& (we won't copy the string)
 * @param str
 * @return std::u32string (A UTF-32 string)
 */

std::u32string convertToUTF32(const std::string&);


/**
 * @brief This function is a crossplatform utf32 to utf8 converter
 * 
 * @param u32str 
 * @return std::string (A UTF-8 string)
 */
std::string convertFromUTF32(const std::u32string&);

/**
 * @brief This function tranforms every Capital letter to minuscule
 *
 * @param c
 * @return char32_t
 */
char32_t pulaar_tolower(char32_t c);

/**
 * @brief This will extract words from a .txt file written in pulaar.
 * @tparam char*
 * @param filename
 * @tparam *Function pointer.
 * @param func
 */

template <class F>
void ExtractWordsPulaar(const char *filename, F &&func)
{

    std::ifstream file(filename);
    if (!file)
    {
        std::cerr << "Could not open file: " << filename << std::endl;
        return;
    }

    std::string line;
    int line_number = 1;

    while (std::getline(file, line))
    {
        std::u32string uline = convertToUTF32(line);
        std::u32string word;
        int word_number = 0;

        for (char32_t c : uline)
        {
            if (isPulaarLetter(c))
            {
                word.push_back(c);
            }
            else if (!word.empty())
            {
                ++word_number;
                func(line_number, word_number, word);
                word.clear();
            }
        }

        // Emit last word if line ends with a letter
        if (!word.empty())
        {
            ++word_number;
            func(line_number, word_number, word);
        }

        ++line_number;
    }
}
